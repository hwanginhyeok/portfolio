# DESIGN_SYSTEM.md — B4 디자인 시스템

> 최종 수정: 2026-04-26 (B4-01 초안 — 사용자 입력 필요 5건 명시)
> 위치: `docs/blocks/04-design/DESIGN_SYSTEM.md`
> 의존: B3-01 (LAYOUT.md 5섹션 확정 후 §9 우선순위 적용)
> 입력: `tailwind.config.mjs` · `src/components/*.astro` 7종 · `src/styles/global.css` · `EXPERT_REVIEW_20260426.md` · `THEME_MAP_V3.md`

---

## §0. 본 문서의 역할

이 문서는 포트폴리오 사이트의 **시각·구조 SSOT**다. 색상·타이포·간격·컴포넌트 규약이 여기서만 정의되고, 코드(`tailwind.config.mjs` / `global.css` / 각 `*.astro`)는 본 문서의 결정을 따른다. 결정이 본 문서와 어긋나면 코드가 틀린 것이다.

**스코프**:
- 톤 결정 (도메인별 인상, 보수성/모던성 균형)
- 토큰 정의 (color / type / spacing / radius / shadow)
- 컴포넌트 일관성 규약 (현 7종 + 신규 9종 후보)
- 반응형·접근성 게이트

**스코프 외**:
- 콘텐츠(B1)·메시지(B2)·섹션 배치(B3) — 별도 SSOT
- 마케팅 카피 — `EXPERT_REVIEW_20260426.md` 참조

---

## §1. 디자인 원칙 (Design Principles)

### 1-1. 채용 포트폴리오 톤

> 채용 포트폴리오는 **내용 신뢰도가 디자인보다 우선**한다. 과한 인터랙션·애니메이션·트렌드 추종은 "기술자가 아닌 마케터" 시그널을 줄 수 있다.

| 축 | 결정 | 근거 |
|---|---|---|
| 보수적 ↔ 모던 | **보수 60 / 모던 40** | 1차 타깃이 자동차·로봇·중공업 양산 직군. ATS·시니어 면접관 가독성 우선. |
| 정보 밀도 | **중간** (white space 충분) | 시험 데이터·DFMEA·CAN 다이어그램이 많아 밀도가 자연 상승. 패딩으로 호흡 확보. |
| 모바일 우선 | **데스크톱 우선 + 모바일 견고** | 채용 1차 검토는 PC. 단 모바일 깨짐은 신뢰도 직격이라 회피만 보장. |
| 인터랙션 | **최소** | hover 색 변화·smooth scroll만. 스크롤 페어링·패럴랙스 금지. |
| 애니메이션 | **거의 없음** | transition 150ms 이내. 진입 애니메이션 0. |

### 1-2. 도메인별 인상 (EXPERT_REVIEW 반영)

| 도메인 | 1차 인상 키워드 | 디자인 단서 |
|---|---|---|
| Physical AI | "Sim2Real / Co-simulation" | 다이어그램(노드그래프 풍) + 코드 폰트. 차가운 회색 톤. |
| 로보틱스 | "Systems Integration · Functional Safety" | CAN 노드 컬러분리 + ISO 매핑 표. |
| 제품 PM | "APQP · RACI · QCD" | 표(table) 가독성 + 게이트차트 친화. |
| 스타트업 | "0→1 Builder · AI-Augmented" | 정량 임팩트 카드 + GitHub 위젯. 더 따뜻한 톤 허용. |

→ **결론**: 한 사이트로 4 도메인 커버. 도메인 분기 헤더는 B5에서 검토(영문 부제만 가변). 본 문서는 **공통 베이스라인**만 정의.

---

## §2. 색상 시스템 (Color Tokens)

### 2-1. 현재 토큰 점검 (`tailwind.config.mjs`)

```js
primary: '#1a1a2e'   // 거의-검정 네이비 — 헤더·본문·Hero 배경
accent:  '#0066ff'   // 채도 높은 블루 — CTA·하이라이트·메트릭
surface: '#f8f9fa'   // 거의-흰 회색 — 섹션 배경 분할용
muted:   '#6b7280'   // 중성 회색 — 보조 텍스트
```

**문제 1**: Neutral 스케일 부재 → 컴포넌트가 `gray-50/100/200/300/400/500/700` 자유 사용. (예: `CaseCard.astro:34` `border-gray-200`, `Hero.astro:18` `text-gray-300`)
**문제 2**: 시맨틱 색상(success/warning/error/info) 미정의 → `StateMachine.astro`에서 인라인 `green/blue/orange/red/amber-50/300/500` 혼재.
**문제 3**: 테마 컬러(T-1~T-7)가 `CaseCard.astro:17~25`에 하드코딩 → 토큰화 필요.

### 2-2. 제안 토큰 (확정 시 tailwind.config 반영)

```js
colors: {
  primary: '#1a1a2e',          // 유지
  accent:  '#0066ff',          // 유지
  surface: '#f8f9fa',          // 유지
  muted:   '#6b7280',          // 유지
  // 신규 — Neutral scale (gray-* 직접 사용 줄이기)
  ink: {
    900: '#0f172a',  // 본문 (Hero 외)
    700: '#334155',  // 본문 강조
    500: '#64748b',  // 보조 텍스트 (= muted 대체 가능)
    300: '#cbd5e1',  // 구분선
    100: '#f1f5f9',  // 카드 배경
    50:  '#f8fafc',  // 섹션 분할 배경
  },
  // 신규 — Semantic
  success: '#16a34a',  // 정량 임팩트(+57%, 0.082m 등)
  warning: '#d97706',  // 트레이드오프·주의
  error:   '#dc2626',  // E-Stop·실패 케이스
  info:    '#0284c7',  // 보조 정보
}
```

### 2-3. 다크모드 ✅ 확정 (2026-05-04)

**라이트 전용** — 채용 PDF 인쇄 호환·복잡도 최소. 다크모드 토큰 미구현.

### 2-4. WCAG 대비 검증 (B4 완료 게이트)

- 본문 `ink-700 on white` → 대비비 9.7:1 ✅
- `muted (#6b7280) on white` → 대비비 4.6:1 (AA pass, AAA fail) — 본문 외만 허용
- `accent (#0066ff) on white` → 대비비 5.1:1 (AA Large pass) — 14px 이상만

---

## §3. 타이포그래피

### 3-1. 현재 상태 (`global.css` / `tailwind.config`)

```
font-sans:    Noto Sans KR · Apple SD Gothic Neo
font-display: Outfit · Noto Sans KR
@import:      Google Fonts (Noto KR 300/400/500/700/900 + Outfit 700/900)
```

**문제**: 코드(`mono`) 폰트 미지정 → 브라우저 기본(`Courier New`)으로 떨어짐. `StateMachine.astro:131` `font-mono` 사용 중인데 토큰 없음.

### 3-2. 폰트 결정 ✅ 확정 (2026-05-04)

| 슬롯 | 결정 |
|---|---|
| 한글 본문 | **Pretendard** — Noto Sans KR에서 전환 (CDN 1줄) |
| 영문 헤딩 | **Outfit** — 현행 유지 |
| 코드/수치 | **JetBrains Mono** (한글 fallback: Pretendard) |

### 3-3. 타입 스케일 (px @ desktop / mobile)

| 토큰 | 데스크톱 | 모바일 | weight | line-height | 용도 |
|---|---|---|---|---|---|
| `display-xl` | 56 / 4xl | 36 / 3xl | 900 | 1.1 | Hero H1 |
| `display-lg` | 40 / 4xl | 30 / 3xl | 800 | 1.15 | 섹션 H1 |
| `h2` | 28 / 3xl | 22 / 2xl | 700 | 1.25 | 테마 타이틀 |
| `h3` | 22 / 2xl | 18 / xl | 700 | 1.3 | 케이스 카드 제목 |
| `h4` | 18 / lg | 16 / base | 600 | 1.4 | 표 헤더·서브섹션 |
| `body` | 16 / base | 16 / base | 400 | 1.65 | 본문 |
| `body-sm` | 14 / sm | 14 / sm | 400 | 1.6 | 보조 |
| `caption` | 12 / xs | 12 / xs | 500 | 1.5 | 표 캡션·메타 |
| `mono` | 14 / sm | 13 | 400 | 1.55 | 코드·CAN ID·수치 |

**규칙**:
- 본문 폰트크기 16px 미만 금지 (모바일 가독성)
- H1~H4는 `tracking-tight` 유지(`global.css:19,22`)
- 한글 weight 700↑ 사용 시 hinting 깨짐 검증 필요

---

## §4. Spacing & Layout

### 4-1. Spacing scale (4px / 8px 기반 — Tailwind 기본 유지)

```
0.5(2px) · 1(4) · 2(8) · 3(12) · 4(16) · 6(24) · 8(32) · 12(48) · 16(64) · 20(80) · 24(96)
```

표준 사용:
- 카드 내부 패딩: `p-5 md:p-6` (= 20/24px)
- 섹션 세로 간격: `py-16 md:py-24`
- 요소 사이: `space-y-3` 본문 / `space-y-6` 블록

### 4-2. 컨테이너 max-width — **현재 혼용** (점검 필요)

| 페이지 | 현재 값 | 위치 |
|---|---|---|
| `index.astro` | `max-w-5xl` | `src/pages/index.astro:17` |
| `Hero.astro` | `max-w-5xl` | `src/components/Hero.astro:7` |
| `cases/eop-400w/index.astro` | **`max-w-3xl`** | line 7 |
| `cases/patent/index.astro` | **`max-w-3xl`** | line 7 |
| `cases/ss500-state-machine/index.astro` | **`max-w-3xl`** | line 9 |
| `cases/test-engineering/index.astro` | **`max-w-3xl`** | line 85 |

**제안 표준**:
- **홈·랜딩**: `max-w-5xl` (1024px) — 카드 그리드 2~3열 수용
- **케이스 상세**: `max-w-3xl` (768px) — 본문 가독성 우선 (현재 일관 ✅)
- **Hero/Footer**: `max-w-5xl` 외곽 + 내부 wrap 자유

→ **결정**: 현 정책 유지. 단 본 문서에 명시되어 있어야 일관성 보장.

### 4-3. 그리드

- Hero 5col 분할(`grid md:grid-cols-5` `Hero.astro:8`) → 텍스트 3 / 이미지 2 — **유지**.
- 카드 그리드: 모바일 1열 / md 2열 / lg 3열 (`grid md:grid-cols-2 lg:grid-cols-3 gap-4`)

---

## §5. 컴포넌트 통일 규칙

### 5-1. 현 7종 점검표

| 컴포넌트 | 파일 | radius | border | shadow | bg | 일관성 |
|---|---|---|---|---|---|---|
| Hero | `Hero.astro` | `rounded-lg` (이미지) | — | `shadow-2xl` | `bg-primary` | ✅ |
| CaseCard | `CaseCard.astro:34` | `rounded-lg` | `border-gray-200` | `hover:shadow-md` | `bg-white` | ✅ |
| Timeline | `Timeline.astro` | `rounded-full`(점) | — | — | `bg-surface` 태그 | ✅ |
| SystemArchitecture | `SystemArchitecture.astro:10` | **`rounded-xl`** | `border` | `shadow-lg`(헤더) | `bg-white` | ⚠️ radius 불일치 |
| StateMachine | `StateMachine.astro:6` | **`rounded-xl`** | `border` | — | `bg-white` | ⚠️ radius 불일치 |
| CanNetworkDiagram | `CanNetworkDiagram.astro:7` | **`rounded-xl`** | `border` | `shadow-md`(헤더) | `bg-white` | ⚠️ radius 불일치 |
| ThemeHeatmap | `ThemeHeatmap.astro` | `rounded`(셀) | `border` | — | 파레트 별 | ✅ (단 v3에서 교체 예정) |

### 5-2. 통일 규칙 (제안)

```
카드(card):       rounded-lg   border border-ink-300/50  hover:shadow-md
다이어그램 박스:  rounded-xl   border border-ink-300       (외곽만 xl, 내부 셀은 lg)
배지(badge):      rounded-full px-2 py-0.5  text-xs font-medium
표(table):        rounded-lg overflow-hidden border border-ink-300
이미지 figure:    rounded-lg shadow-sm border border-ink-100  + caption text-xs muted
```

**근거**: 다이어그램은 큰 외곽 컨테이너(=`xl`), 내부 카드는 표준 카드(=`lg`). 시각 무게 위계 유지.

### 5-3. figure / caption 표준화

```html
<figure class="my-6">
  <img class="rounded-lg border border-ink-100 w-full" loading="lazy" />
  <figcaption class="text-xs text-muted mt-2 text-center">캡션</figcaption>
</figure>
```

`global.css:12` 의 `figure img { cursor-zoom-in }` — **유지 확정 (2026-05-04)**. `BaseLayout.astro`에 라이트박스 구현 확인됨. 커서가 클릭 가능성 안내.

### 5-4. 표(table) 통일

```html
<div class="rounded-lg overflow-hidden border border-ink-300 my-4">
  <table class="w-full text-sm">
    <thead class="bg-ink-50">
      <tr><th class="text-left p-3 font-semibold">열</th>...</tr>
    </thead>
    <tbody class="divide-y divide-ink-100">
      <tr><td class="p-3">셀</td>...</tr>
    </tbody>
  </table>
</div>
```

모바일: `<div class="overflow-x-auto">` 래핑 필수 (현 `StateMachine.astro:6` 패턴 차용).

### 5-5. 카드(card) 3종 — variant 분리

| variant | 용도 | 차별점 |
|---|---|---|
| `case` | 5섹션 카드 (CaseCard.astro 현행) | 메트릭 + T-tag + "자세히 →" |
| `paper` | 논문/특허 카드 | 저자·게재지·연도 메타 + 외부 링크 |
| `test` | 시험·DFMEA 카드 | 4줄 프레임(고장모드/원인/설계/검증) |

**구현**: 단일 `<Card>` 컴포넌트 + `variant` prop. 현 `CaseCard.astro`는 `variant="case"` 기본값으로 리팩토링 권장.

### 5-6. "조건/효과 표" — B1-14 신규 패턴

PAPERS/시험 케이스에서 도입한 "조건 → 효과" 2열 표. 표준화:

```html
<div class="grid md:grid-cols-2 gap-4 my-4">
  <div class="rounded-lg bg-ink-50 p-4 border-l-4 border-info">
    <h4 class="text-sm font-semibold text-info mb-2">조건</h4>
    <p class="text-sm text-ink-700">...</p>
  </div>
  <div class="rounded-lg bg-ink-50 p-4 border-l-4 border-success">
    <h4 class="text-sm font-semibold text-success mb-2">효과</h4>
    <p class="text-sm text-ink-700">...</p>
  </div>
</div>
```

→ 신규 컴포넌트 `<ConditionEffect>` 후보.

---

## §6. 시각 요소 가이드

### 6-1. 다이어그램 색상 통일

현재 3개 다이어그램이 **노드 의미 색**을 자체 매핑:

| 컴포넌트 | 색 → 의미 |
|---|---|
| `CanNetworkDiagram` | red=BMS, green=구동MC, amber=조향, purple=펌프, orange=ADT |
| `StateMachine` | green=RC, blue=LCD, orange=ADT, red=Emergency, amber=장애물 |
| `SystemArchitecture` | (검토 필요) |

**문제**: 같은 ADT가 한쪽 orange / 다른 쪽 orange — 우연히 일치. **green/blue/orange/red** 의미가 컴포넌트마다 다름 → 시청자 혼란.

**제안 (의미 색 SSOT)**:

| 색 | 의미 |
|---|---|
| accent (#0066ff) | 메인 노드(VCU) · 활성 경로 |
| success | 정상 상태 · 정량 임팩트 |
| warning (amber) | 주의·트레이드오프·장애물 감지 |
| error (red) | 비상정지·실패·BREAKING CHANGE |
| info (sky) | 보조 정보 |
| neutral (ink-500) | 외부·비활성 |

→ 노드별 의미 색 매핑은 컴포넌트 각자 정하되 **시맨틱 5색 + neutral**만 사용.

### 6-2. 이미지 처리 표준

```
rounded-lg + border border-ink-100 + bg-ink-50 (로딩 placeholder) + loading="lazy"
```

Hero 이미지만 `loading="eager"` (LCP).

### 6-3. 아이콘 정책

현재 사이트 **이모지 0개** (확인됨). 사용자 메모리 "이모지 명시 요청 시만" 정책과 일치 → **유지**.
필요 시 [Lucide React](https://lucide.dev/) 또는 SVG 인라인. 이모지 금지.

---

## §7. 모바일 반응형

### 7-1. 브레이크포인트 (Tailwind 기본 유지)

```
sm: 640  md: 768  lg: 1024  xl: 1280  2xl: 1536
```

주 사용: **md (768) / lg (1024)**. sm/xl은 fine-tune만.

### 7-2. 모바일 처리 정책

| 요소 | 정책 |
|---|---|
| 표(table) | `overflow-x-auto` 래퍼 필수. 첫 열 sticky 권장 |
| 다이어그램 | `overflow-x-auto` (현재 `StateMachine.astro:6` ✅, `SystemArchitecture.astro:10` ✅, `CanNetworkDiagram` 미적용 — **수정 필요**) |
| Hero 5col | md 미만에서 1열 전환(현 `grid md:grid-cols-5` ✅) |
| 카드 그리드 | `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` |
| 폰트 | 본문 16px 유지(축소 금지). 헤딩만 단계 축소 |

### 7-3. 점검 체크리스트

- [ ] iPhone SE (375px) 가로 스크롤 0
- [ ] 다이어그램 3종 모바일 가로 스크롤 동작
- [ ] Hero 텍스트·이미지 1열에서 순서 정상
- [ ] 표 3종 모바일 readability

---

## §8. 접근성 (Accessibility)

### 8-1. 필수

- 모든 `<img>` `alt` 텍스트 — 장식이면 `alt=""`. 현재 케이스 페이지 점검 필요.
- 본문 색상 대비 WCAG AA (4.5:1) 이상. §2-4 검증 표 통과.
- 포커스 인디케이터 유지(`:focus-visible` Tailwind 기본).
- 키보드 탐색: `<a>`/`<button>` 만 사용. div onClick 금지.

### 8-2. 권장

- `<section aria-labelledby="...">` 5섹션에 적용
- 다이어그램은 `role="img" aria-label="..."` + 본문 텍스트 동등물 제공
- 표는 `<caption>` 또는 `aria-describedby`

### 8-3. 폰트 크기 ✅ 확정 (2026-05-04)

**16px 유지** — 정보 밀도 유지 우선.

---

## §9. 우선 적용 항목 (B3 결정 후 재정렬)

> B3-01 (5섹션 와이어프레임)이 들어오면 본 절의 우선순위가 확정된다. 현재는 **잠정 P1~P3**.

**P1 (디자인 시스템 미적용 시 사이트 깨짐)**
1. 토큰 추가: `ink-*` neutral scale + semantic colors → `tailwind.config.mjs`
2. 컨테이너 max-width 정책 명시 (홈 5xl / 케이스 3xl)
3. 다이어그램 3종 radius 통일 (현 모두 `rounded-xl` 유지 — 본 문서에 명시만)
4. CaseCard `variant` 분리 + theme 색상 토큰화

**P2 (B3 5섹션 적용 시점)**
5. 신규 컴포넌트 9종 (THEME_MAP_V3 §3): DFMEAField, PerformanceFlow, TestProcess, CANDesign, NextGen, APQPSystem, Research, Patents, AINative
6. LifecycleHeatmap 신규 (ThemeHeatmap 대체)
7. ConditionEffect 컴포넌트 도입

**P3 (B5 영문판·이력서·성능)**
8. 다크모드 결정에 따라 토큰 확장
9. 폰트 전환 (Pretendard / JetBrains Mono) — 결정 후
10. Lighthouse 90+ 튜닝 (이미지 lazy / WebP / 폰트 서브셋)

---

## §10. 완료 게이트 체크리스트

### 토큰
- [ ] `tailwind.config.mjs`에 ink/semantic 토큰 추가
- [ ] `global.css`에 mono 폰트 패밀리 등록
- [ ] CaseCard 테마 색상이 토큰을 참조 (인라인 hex 0건)

### 컴포넌트
- [ ] 7종 컴포넌트 모두 §5 통일 규칙 통과
- [ ] 다이어그램 3종 시맨틱 색 SSOT (§6-1) 통과
- [ ] figure/caption / table / card 3 variant / ConditionEffect 표준 컴포넌트 존재

### 페이지
- [ ] 5개 페이지(index + 4 cases) max-width 정책 통과
- [ ] Hero loading="eager", 그 외 이미지 lazy
- [ ] 모든 `<img>` alt 텍스트 존재

### 접근성·성능
- [ ] WCAG AA 대비 검증 통과 (Lighthouse)
- [ ] iPhone SE (375px) 가로 스크롤 0
- [ ] Lighthouse Desktop 90+ / Mobile 85+
- [ ] LCP < 2.5s, CLS < 0.1

### 사용자 결정 (6건) ✅ 전체 확정 (2026-05-04)
- [x] **#1** 다크모드: **라이트 전용**
- [x] **#2-1** 한글 폰트: **Pretendard 전환**
- [x] **#2-2** 코드 폰트: **JetBrains Mono**
- [x] **#3** 본문 폰트크기: **16px 유지**
- [x] **#4** Hero 이미지 zoom: **cursor-zoom-in 유지** (BaseLayout 라이트박스 구현 확인)
- [x] **#5** 도메인별 헤더 분기: **단일 헤더** (H-A 유지, 분기 없음)

---

## 참고

- 입력 SSOT: `tailwind.config.mjs` · `src/styles/global.css` · `src/components/*.astro` 7종
- 콘텐츠 SSOT: `docs/포트폴리오/CONTENT_V2.md` · `THEME_MAP_V3.md` · `EXPERT_REVIEW_20260426.md`
- 글로벌 규칙: `global-rules/doc-size.md` (300~500줄) · `global-rules/test-first.md` (선검증)
- 다음 액션: B3-01 5섹션 와이어프레임 확정 → 본 문서 §9 우선순위 재배열 → P1 토큰 PR
