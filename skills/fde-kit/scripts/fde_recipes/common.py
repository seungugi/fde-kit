"""Strict contracts, bounded inputs, provenance and fresh output directories."""
import csv
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import html
import io
import json
import os
from pathlib import Path
import stat
import tempfile

from . import VERSION

MAX_FILE = 8 * 1024 * 1024
MAX_ROWS = 50000
MAX_COLUMNS = 200
MAX_CELLS = 250000


class RecipeError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise RecipeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def no_links(path):
    path = Path(os.path.abspath(path))
    for part in [path, *path.parents]:
        reparse = bool(getattr(part.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT) if part.exists() else False
        require(not part.is_symlink() and not reparse,
                f'Symlink/junction paths are not supported: {part}')
    return path


def read_bytes(path, limit=MAX_FILE):
    path = no_links(path)
    require(path.is_file(), f'Not a regular file: {path}')
    with path.open('rb') as source:
        data = source.read(limit + 1)
    require(len(data) <= limit, f'File exceeds {limit} bytes: {path}')
    return data


def decode(data):
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise RecipeError('Input must be UTF-8 (BOM is supported).') from exc
    require('\x00' not in text, 'NUL bytes are not supported.')
    return text


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def bad_constant(value):
    raise RecipeError(f'Non-finite JSON number: {value}')


def parse_json(text):
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant, parse_float=Decimal)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise RecipeError('Malformed or excessively nested JSON.') from exc


def load_json(path):
    data = read_bytes(path)
    return parse_json(decode(data)), {'path': str(path), 'sha256': sha(data)}


def keys(obj, allowed, required=()):
    require(isinstance(obj, dict), 'Expected an object in configuration.')
    require(not set(obj) - set(allowed), f'Unknown configuration keys: {sorted(set(obj) - set(allowed))}')
    require(set(required) <= set(obj), f'Missing configuration keys: {sorted(set(required) - set(obj))}')


def number(value):
    require(not isinstance(value, (bool, dict, list)), 'Expected a decimal number, not a boolean/object.')
    text = str(value).strip()
    require(len(text) <= 128, 'Numeric value is too long.')
    try:
        result = Decimal(text)
    except InvalidOperation as exc:
        raise RecipeError('Expected a decimal number.') from exc
    require(result.is_finite(), 'NaN and infinity are not valid numbers.')
    require(len(result.as_tuple().digits) <= 50 and abs(result.as_tuple().exponent) <= 50,
            'Number exceeds supported precision/range (50 digits/exponent).')
    return result


def decimal_text(value):
    if value == 0:
        return '0'
    result = format(value, 'f')
    return result.rstrip('0').rstrip('.') if '.' in result else result


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False,
                      default=lambda x: decimal_text(x) if isinstance(x, Decimal) else str(x)) + '\n'


def markdown(value):
    text = html.escape(str(value), quote=True).replace('\r', ' ').replace('\n', ' ')
    for char in ('\\', '`', '*', '_', '[', ']', '|', '<', '>'):
        text = text.replace(char, '\\' + char)
    return text


def csv_text(rows, columns, numeric=()):
    out = io.StringIO(newline='')
    writer = csv.writer(out, lineterminator='\n')
    def safe(value, is_numeric=False):
        if value is None:
            return ''
        text = decimal_text(value) if isinstance(value, Decimal) else str(value)
        # Spreadsheet-safe display export. JSON remains the canonical exact data.
        if not is_numeric and text.lstrip().startswith(('=', '+', '-', '@', '\t', '\r', '\n')):
            return "'" + text
        return text
    writer.writerow([safe(c) for c in columns])
    for row in rows:
        writer.writerow([safe(row.get(c), c in numeric) for c in columns])
    return out.getvalue()


def read_rows(path):
    data = read_bytes(path)
    text = decode(data)
    suffix = Path(path).suffix.lower()
    if suffix in ('.csv', '.tsv'):
        try:
            reader = csv.reader(io.StringIO(text, newline=''), delimiter='\t' if suffix == '.tsv' else ',', strict=True)
            header = next(reader, None)
            require(header and len(header) <= MAX_COLUMNS, 'Missing header or too many columns.')
            require(all(h and h.strip() == h for h in header) and len(set(header)) == len(header),
                    'Headers must be nonblank, unique and have no surrounding whitespace.')
            rows = []
            for values in reader:
                require(len(values) == len(header), f'Wrong column count at physical line {reader.line_num}.')
                rows.append(dict(zip(header, values)))
                require(len(rows) <= MAX_ROWS and len(rows) * len(header) <= MAX_CELLS, 'Too many rows/cells.')
        except csv.Error as exc:
            raise RecipeError(f'Malformed CSV/TSV: {exc}') from exc
    elif suffix == '.json':
        rows = parse_json(text)
        require(isinstance(rows, list) and len(rows) <= MAX_ROWS, 'JSON input must be a bounded array of objects.')
        require(all(isinstance(r, dict) for r in rows), 'Each JSON row must be an object.')
        header = list(rows[0]) if rows else []
        require(len(header) <= MAX_COLUMNS and all(isinstance(h, str) and h.strip() == h and h for h in header),
                'Invalid JSON column names.')
        require(all(set(r) == set(header) for r in rows), 'JSON rows must have identical columns.')
        require(len(rows) * len(header) <= MAX_CELLS, 'Too many cells.')
    else:
        raise RecipeError('Supported table formats: .csv, .tsv, .json array.')
    require(rows, 'Input has no data rows; an empty result is not a completed analysis.')
    return rows, header, {'path': str(path), 'sha256': sha(data), 'row_reference': '1-based data record, excluding CSV header'}


def validate_schema(schema):
    keys(schema, ('columns', 'id_column'), ('columns',))
    columns = schema['columns']
    require(isinstance(columns, dict) and 0 < len(columns) <= MAX_COLUMNS, 'Declare 1..200 columns.')
    for name, spec in columns.items():
        require(isinstance(name, str) and name and name.strip() == name, 'Invalid schema column name.')
        keys(spec, ('type', 'required', 'min', 'max', 'choices'), ('type',))
        require(spec['type'] in ('string', 'number'), f'Unknown type for {name}.')
        require(isinstance(spec.get('required', True), bool), 'required must be boolean.')
        if 'choices' in spec:
            choices = spec['choices']
            require(spec['type'] == 'string' and isinstance(choices, list) and choices
                    and all(isinstance(x, str) for x in choices), 'choices requires a nonempty string array.')
        for bound in ('min', 'max'):
            if bound in spec:
                require(spec['type'] == 'number', 'min/max are numeric only.')
                number(spec[bound])
        if 'min' in spec and 'max' in spec:
            require(number(spec['min']) <= number(spec['max']), 'min exceeds max.')
    if 'id_column' in schema:
        require(schema['id_column'] in columns and columns[schema['id_column']]['type'] == 'string'
                and columns[schema['id_column']].get('required', True), 'ID must name a required string column.')


def typed_rows(rows, header, schema):
    validate_schema(schema)
    columns = schema['columns']
    require(set(header) == set(columns), 'Input columns must match the declared schema exactly.')
    accepted, excluded = [], []
    ids = {}
    if 'id_column' in schema:
        for row in rows:
            value = row[schema['id_column']]
            if isinstance(value, str) and value.strip():
                ids[value] = ids.get(value, 0) + 1
    for index, row in enumerate(rows, 1):
        values, errors = {}, []
        for name, spec in columns.items():
            value = row[name]
            try:
                if value is None or isinstance(value, str) and not value.strip():
                    require(not spec.get('required', True), 'Missing required value.')
                    values[name] = None
                    continue
                if spec['type'] == 'number':
                    value = number(value)
                    require('min' not in spec or value >= number(spec['min']), 'Below minimum.')
                    require('max' not in spec or value <= number(spec['max']), 'Above maximum.')
                else:
                    require(isinstance(value, str), 'Expected a string (IDs must preserve leading zeros).')
                    require('choices' not in spec or value in spec['choices'], 'Value is outside choices.')
                values[name] = value
            except RecipeError as exc:
                errors.append({'column': name, 'reason': str(exc)})
        id_col = schema.get('id_column')
        if id_col and isinstance(row[id_col], str) and ids.get(row[id_col], 0) > 1:
            errors.append({'column': id_col, 'reason': 'Duplicate ID: all rows with this ID require review.'})
        item = {'source_row': index, 'values': values}
        if errors:
            excluded.append({'source_row': index, 'raw': row, 'errors': errors})
        else:
            accepted.append(item)
    return accepted, excluded


def publish(out, artifacts, sources, recipe, protected=()):
    out = no_links(out)
    require(not out.exists(), 'Output directory already exists; choose a new run directory (no overwrite).')
    for item in protected:
        source = no_links(item)
        require(out != source and not out.is_relative_to(source) and not source.is_relative_to(out),
                'Output must not contain or be nested inside an input/document directory.')
    encoded = {name: text.encode('utf-8') for name, text in artifacts.items()}
    manifest = {'version': VERSION, 'recipe': recipe, 'inputs': sources,
                'implementation': {p.name: sha(p.read_bytes()) for p in sorted(Path(__file__).parent.glob('*.py'))},
                'artifacts': {name: sha(data) for name, data in encoded.items()},
                'meaning': 'Byte provenance, not independent proof of business correctness.'}
    encoded['manifest.json'] = dump(manifest).encode('utf-8')
    out.parent.mkdir(parents=True, exist_ok=True)
    # Complete the staging files before publishing. Only a manifest-complete directory is a finished run.
    with tempfile.TemporaryDirectory(prefix='.fde-recipe-', dir=out.parent) as staging:
        stage = Path(staging)
        for name, data in encoded.items():
            (stage / name).write_bytes(data)
        out.mkdir()  # Exclusive reservation; never replace a pre-existing directory.
        for name in encoded:  # manifest is deliberately last
            os.replace(stage / name, out / name)
    return out
