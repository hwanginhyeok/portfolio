# B4 — 디자인 (HOW IT LOOKS)

> "배치가 확정된 뒤 실제 코드·비주얼을 완성한다."

## 목적

배치(B3)가 확정됐으므로, 톤앤매너·타이포·컬러·컴포넌트를 정하고 astro 페이지로 구현. **1인 엔지니어 브랜드**가 뚜렷하게 드러나야 함.

## 산출물

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) — 디자인 시스템
- `src/pages/*.astro` — 실제 구현
- `src/components/*.astro` — 재사용 컴포넌트

## 결정 영역

1. **디자인 시스템**
   - 컬러 팔레트 (primary/accent/neutral)
   - 타이포그래피 (본문/헤드라인/코드)
   - 간격·라운드·그림자 스케일
   - 모션 (hover/scroll/transition)

2. **컴포넌트 통일**
   - StateMachine
   - Diagram (Mermaid HTML)
   - Case Card
   - Impact Badge
   - Hero Block

3. **반응형**
   - 모바일 우선? 데스크톱 우선?
   - 브레이크포인트

4. **성능**
   - 이미지 lazy load
   - WebP/AVIF
   - 폰트 서브셋

## 완료 게이트

- [ ] 디자인 시스템 문서화
- [ ] 모든 페이지가 시스템 준수
- [ ] 컴포넌트 재사용 (중복 스타일 제거)
- [ ] Lighthouse 점수 90+ (데스크톱/모바일)
- [ ] 배포 가능 상태
