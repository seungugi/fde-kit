# 온담 — 월간 식단 편성·메뉴 관심 연습

FDE Web Starter의 실행 가능한 합성 예제다. 가상 구성원 120명, 2026년 11월 평일 점심 21회, 하루 한 세트와 1인 1식 8,000원 이하를 사용한다. 사용자에게 나머지 조건의 결정을 위임받아 아래 정책을 연습용으로 정했다. 실제 대회 문제·공식 평가표·건강/영양 처방이 아니다.

## 실행

Python 3.10+가 필요하며 검증한 환경은 Windows Python 3.12다. requirements.txt는 웹 프로젝트에만 필요한 정확한 버전 목록이다.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
DEMO_MODE=1 .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DEMO_MODE = "1"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

http://127.0.0.1:8765 에 접속한다. 종료는 Ctrl+C다. APP_DB로 SQLite 저장 위치를 지정할 수 있고 데이터는 재시작 후 유지된다. APP_SECRET을 설정하지 않으면 로컬 실행 때마다 임의 세션 키를 사용하므로 로그인 상태는 초기화될 수 있다. DEMO_MODE=1의 구성원/관리자 전환은 역할별 동작을 체험하는 장치이며 실제 사용자 인증이 아니다. 공개 운영 전에 제공 환경의 인증과 권한을 연동해야 한다. 기본 모드에서는 보호된 변경이 차단된다.

## 수행할 과제와 가정

- 구성원: 월간 확정 식단 조회, 메뉴 검색, 메뉴별 관심 표시·취소, 관심 현황 확인.
- 관리자: 관심 자료를 참고한 초안 생성, 날짜별 메뉴 교체, 조건 검사 후 확정. 수정 충돌은 덮어쓰지 않고 다시 읽게 한다.
- 관심은 회원·메뉴당 한 번 표시하는 선호다. 재요청으로 중복 증가하지 않고 취소 가능하다. 관심 수를 식사 예약·실이용 인원으로 해석하지 않는다.
- 월간 같은 메뉴는 최대 2회, 재등장 간격은 최소 5영업일 인덱스 차이다. 달력의 주말을 식사일로 세지 않는다. 법정 휴일이나 회사 휴무 데이터는 제공하지 않았으며 모든 평일을 식사일로 가정했다.
- 합성 현장 조건: 금요일에는 튀김 조리 설비를 사용할 수 없다. 이는 예제에서 명시한 테스트 조건이며 실제 담당자에게 질문해 새로 발견했다는 의미가 아니다.
- 각 식단의 단가는 8,000원 이하. 관심 우선의 결정적인 탐욕 방식으로 유효 초안을 제안하며 전역 최적성을 주장하지 않는다. 조건을 충족하는 회전 기준안과 비교한다. 비용·관심 지표의 정의는 화면과 검사 코드를 따른다.
- 실제 식수, 재고, 영양 적합성, 개인 알레르기 안전성, 회사 SSO는 미검증이다. 없는 사실이나 금액을 실제 관측처럼 표현하지 않는다.

## 검증과 설명

```text
python -m pytest tests -q --basetemp .test-tmp
```

관심 중복·취소, 역할·CSRF, 단가·요일·반복·간격, 오래된 수정 요청, 확정본 보호, 재시작 영속성, CSV 행을 검사한다. 브라우저에서는 관심 버튼의 부분 갱신, 관리자 편집/확정, 모바일 화면도 별도로 확인한다. 허용되지 않는 대회 UI 자동화는 수행하지 않는다.

`/about`은 실제 구현 구조와 선택 이유를 설명하는 화면이다. 데이터 입력→서버 검증→식단/관심 업무 함수→SQLite→Jinja2/HTMX 화면 반영으로 추적한다. 테스트 통과·에이전트 검토·사용자 검토를 구별해 기록한다.

이 예제는 공통 app/main.py·db.py·security.py를 사용하고, 업무 라우트 app/features.py·편성 로직 app/planner.py·화면만 식단용으로 바꾼 것이다. FDE Kit 지침은 .agents/skills/fde-kit, 작업 기록은 fde-notes에 설치된다. 원본 문제의 규칙이 달라지면 같은 BRIEF와 검사 조건부터 갱신한다.

HTMX 2.0.8은 공식 소스 https://github.com/bigskysoftware/htmx/tree/v2.0.8 에서 가져왔고 static/htmx.LICENSE를 함께 제공한다. 브라우저 실행에 외부 CDN이나 AI API 키가 필요하지 않다.
