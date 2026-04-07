# TASK 관리 규칙

## 파일 구조

| 파일 | 용도 |
|------|------|
| `TASK.md` | 인덱스 + 요약 카운트 + TODO |
| `CURRENT_TASK.md` | 진행 중 태스크 |
| `PREPARED_TASK.md` | 예정 태스크 |
| `FINISHED_TASK.md` | 완료 태스크 (당월) |
| `TASK_ARCHIVE/YYYY-MM.md` | 월별 아카이브 |

## 넘버링

- `{분야코드}-{순번}`
  - `1-x`: 기획
  - `2-x`: 프로젝트 케이스
  - `3-x`: 콘텐츠
  - `4-x`: 제작
  - `5-x`: 부가자료
  - `6-x`: 사진/미디어

## 실시간 갱신 (필수)

| 트리거 | 행동 |
|--------|------|
| 작업 착수 시 | PREPARED → CURRENT로 이동 + 시작일 기입 |
| 작업 완료 시 | CURRENT → FINISHED로 이동 + 완료일 기입 |
| 새 작업 발견 시 | PREPARED에 등록 |
| 월 교체 시 | 전월 FINISHED → `TASK_ARCHIVE/YYYY-MM.md`로 이동 |
| 변경 시마다 | TASK.md 요약 카운트 갱신 |
