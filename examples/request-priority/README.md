# 요청 우선순위 예제

FDE 키트 동작을 확인하는 가상 연습입니다. 대회 문제나 정답이 아닙니다.

규칙:
1. 같은 event_id와 같은 전체 내용은 한 번만 반영한다. 같은 event_id의 내용이 다르면 오류로 중단한다.
2. 요청별 가장 큰 정수 version을 현재 상태로 삼는다. 같은 요청/version의 다른 이벤트는 모호하므로 오류로 중단한다.
3. 현재 상태가 done이면 대기열에서 제외한다. 이후 더 큰 version의 open이 있으면 다시 포함한다.
4. priority 값이 작을수록 중요하다. 같으면 received_at이 빠른 순, 그것도 같으면 request_id 순이다. 시각은 이 예제에서 YYYY-MM-DD 형식을 사용한다.

샘플의 정답은 R3, R2, R1이다. R3와 R2는 중요도 1이며 R3의 접수가 빠르다. R1은 중요도 2이다. R4는 완료 상태라 제외한다. R3는 완료 후 재접수되었다.

실행: `python queue_requests.py events.json result.json`
단위/명령행 검사: `python -m unittest -v`
산출물 생성 후 최종 검증: `python check_delivery.py` (위 검사와 실제 result.json을 함께 확인)

범용 처리 규칙을 강제하는 예제가 아니다. 실제 과제의 상태·시각·동률 정책을 먼저 확인한다.
