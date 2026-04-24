# 디자인 시스템

> 최종 수정: 2026-04-24 (초안 — B3 완료 후 확정)

## 1. 브랜드 정체성

> TODO: 한 문장으로 정의 (예: "시험으로 증명하는 시스템 엔지니어")

## 2. 컬러

> 현재 tailwind 설정 기준. 확정 시 `tailwind.config.mjs`에 반영.

| 역할 | Hex | 용도 |
|------|-----|------|
| Primary | TODO | 본문 링크, CTA 버튼 |
| Accent | TODO | 강조 수치, Badge |
| Neutral 900 | TODO | 본문 텍스트 |
| Neutral 500 | TODO | 보조 텍스트 |
| Neutral 100 | TODO | 배경 |
| Success | TODO | 정량 임팩트 |

## 3. 타이포그래피

| 스타일 | 폰트 | 크기 | 용도 |
|--------|------|------|------|
| Headline | TODO | TODO | 섹션 타이틀 |
| Body | TODO | TODO | 본문 |
| Mono | TODO | TODO | 코드, 수치 |

## 4. 간격·라운드

- 간격 스케일: 4 / 8 / 16 / 24 / 48 / 96 (px)
- 라운드: sm / md / lg / full
- 그림자: soft / elevated

## 5. 컴포넌트 카탈로그

| 컴포넌트 | 위치 | 상태 | 비고 |
|---------|------|:----:|------|
| StateMachine | `src/components/StateMachine.astro` | ✅ | D3 케이스 완료 |
| 홈 아키텍처 다이어그램 | — | ✅ | 4-3 완료 |
| Case Card | TODO | ⬜ | |
| Impact Badge | TODO | ⬜ | |
| Hero Block | TODO | ⬜ | |

## 6. 모션

> TODO: hover / scroll / transition 정책

## 7. 반응형

- 모바일 우선: TODO
- 브레이크포인트: sm 640 / md 768 / lg 1024 / xl 1280

## 8. 성능 목표

- Lighthouse 90+
- LCP < 2.5s
- CLS < 0.1
- 초기 HTML < 30KB

## 9. 다음 액션

B4 완료 → **실제 사이트 배포**. B5 부가자료(이력서/GitHub/영문) 진행.
