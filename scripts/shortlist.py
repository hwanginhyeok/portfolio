"""Deterministic feasibility and profile-fit classification for job postings.

This module intentionally uses only text already collected into the portfolio
and the profile vocabulary already encoded in the collector configuration.
It does not call a model or an external service.
"""

from __future__ import annotations

import re
from typing import Iterable, Mapping


def _compile(patterns: Iterable[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)


TRACK_CORE = "core"
TRACK_AI_NATIVE = "ai-native"
TRACK_ENGINEERING_CONSULTING = "engineering-consulting"
TRACK_ORDER = (TRACK_CORE, TRACK_AI_NATIVE, TRACK_ENGINEERING_CONSULTING)
TRACK_LABELS = {
    TRACK_CORE: "Core manufacturing / test / electrical",
    TRACK_AI_NATIVE: "AI-native / Physical AI",
    TRACK_ENGINEERING_CONSULTING: "Engineering consulting",
}
TRACK_ALIASES = {
    "core": TRACK_CORE,
    "manufacturing": TRACK_CORE,
    "manufacturing-test-electrical": TRACK_CORE,
    "ai": TRACK_AI_NATIVE,
    "ai-native": TRACK_AI_NATIVE,
    "ai_native": TRACK_AI_NATIVE,
    "physical-ai": TRACK_AI_NATIVE,
    "physical_ai": TRACK_AI_NATIVE,
    "consulting": TRACK_ENGINEERING_CONSULTING,
    "engineering-consulting": TRACK_ENGINEERING_CONSULTING,
    "engineering_consulting": TRACK_ENGINEERING_CONSULTING,
    "technical-consulting": TRACK_ENGINEERING_CONSULTING,
    "technical_consulting": TRACK_ENGINEERING_CONSULTING,
}


def normalize_track(value: object) -> str:
    """Normalize persisted/configured track names without breaking old rows."""
    key = str(value or "").strip().casefold()
    return TRACK_ALIASES.get(key, TRACK_CORE)


def primary_track(values: Iterable[object] | object | None) -> str:
    """Choose a stable track when one posting matched multiple search lanes."""
    if isinstance(values, str) or values is None:
        candidates = [values]
    else:
        candidates = list(values)
    normalized = {normalize_track(value) for value in candidates if value}
    for track in (TRACK_ENGINEERING_CONSULTING, TRACK_AI_NATIVE, TRACK_CORE):
        if track in normalized:
            return track
    return TRACK_CORE


def track_label(value: object) -> str:
    return TRACK_LABELS.get(normalize_track(value), TRACK_LABELS[TRACK_CORE])


# These signals are intentionally narrower than a generic AI/software match.
# They are collected for the separate lanes, but actionability still requires
# a physical or industrial owner domain in the title/department.
TECHNICAL_AI_CONSULTING_RULES: tuple[
    tuple[str, tuple[re.Pattern[str], ...]], ...
] = (
    (
        "industrial-ai",
        _compile(
            (
                r"industrial\s+(?:ai|artificial intelligence)",
                r"physical\s+(?:ai|intelligence)",
                r"(?:ai|artificial intelligence)\s+(?:for\s+)?(?:manufacturing|industrial|factory|robotics?)",
                r"산업\s*AI",
                r"피지컬\s*AI",
                r"물리\s*AI",
                r"제조\s*AI",
            )
        ),
    ),
    (
        "robotics-automation",
        _compile(
            (
                r"\brobot(?:ics)?\b",
                r"\bindustrial\s+automation\b",
                r"\bautomation\s+(?:engineer|engineering|architect|consultant)",
                r"\bautonomous\s+(?:systems?|vehicles?|robotics?)\b",
                r"\bautonomy\b",
                r"로봇",
                r"자동화",
                r"자율\s*(?:주행|제조|시스템|로봇)",
            )
        ),
    ),
    (
        "digital-twin-simulation",
        _compile(
            (
                r"digital\s+twin",
                r"\bsimulation\b",
                r"simulink",
                r"model[- ]based\s+(?:design|engineering|simulation)",
                r"디지털\s*트윈",
                r"시뮬레이션",
            )
        ),
    ),
    (
        "forward-deployed-engineering",
        _compile(
            (
                r"forward[- ]deployed\s+(?:engineering|engineer|robotics?)",
                r"포워드[- ]?디플로이(?:드)?",
            )
        ),
    ),
    (
        "technical-consulting",
        _compile(
            (
                r"technical\s+consultant",
                r"engineering\s+consultant",
                r"solutions?\s+(?:architect|engineer)",
                r"technical\s+(?:solutions?|advisor|architect)",
                r"기술\s*컨설턴트",
                r"솔루션\s*(?:아키텍트|엔지니어)",
                r"엔지니어링\s*컨설턴트",
            )
        ),
    ),
    (
        "ai-product-technical-pm",
        _compile(
            (
                r"\bai\s+(?:product|technical|program|project)\s+manag",
                r"\b(?:technical|product)\s+(?:program|project|product)\s+manag[^\n]{0,30}\bai\b",
                r"ai\s*(?:product|기술)?\s*(?:pm|피엠)",
                r"AI\s*프로덕트\s*(?:매니저|PM|피엠)",
            )
        ),
    ),
    (
        "manufacturing-engineering-transformation",
        _compile(
            (
                r"(?:manufacturing|engineering|industrial)\s+transformation",
                r"transformation\s+(?:consultant|architect|engineer)",
                r"제조\s*(?:혁신|전환|트랜스포메이션)",
                r"엔지니어링\s*(?:혁신|전환|트랜스포메이션)",
            )
        ),
    ),
)


CONSULTING_SIGNAL_LABELS = frozenset(
    {"technical-consulting", "manufacturing-engineering-transformation"}
)


# These buckets mirror the owner's evidence in RESUME.md and the collector's
# global_targets.json profile: manufacturing/process, test/validation,
# reliability, quality/supplier, NPI, electrical/hardware, and technical PM.
# A rule contributes only when it appears in the title or department. Body
# mentions are useful raw evidence but never create an actionable fit.
FIT_RULES: tuple[tuple[str, int, tuple[re.Pattern[str], ...]], ...] = (
    (
        "technical-program",
        32,
        _compile(
            (
                r"technical\s+(program|project)\s+manag",
                r"hardware\s+program\s+manag",
                r"\btpm\b",
                r"기술\s*(프로그램|프로젝트|PM|피엠)",
            )
        ),
    ),
    (
        "ai-native-consulting",
        30,
        tuple(
            pattern
            for _, patterns in TECHNICAL_AI_CONSULTING_RULES
            for pattern in patterns
        ),
    ),
    (
        "manufacturing-process",
        30,
        _compile(
            (
                r"manufacturing",
                r"production\s+(engineer|engineering|technology|manager|supervisor|lead)",
                r"process\s+engineer",
                r"industriali[sz]ation",
                r"industrial\s+engineer",
                r"factory",
                r"제조",
                r"생산",
                r"공정",
                r"양산",
            )
        ),
    ),
    (
        "test-validation",
        30,
        _compile(
            (
                r"test\s+(engineer|engineering|infrastructure|lab|lead|specialist)",
                r"validation\s+engineer",
                r"verification\s+(engineer|engineering)",
                r"qualification\s+(test|testing|engineer|lab)",
                r"hardware[- ]in[- ]the[- ]loop",
                r"\bhil\b",
                r"시험",
                r"테스트",
                r"검증",
            )
        ),
    ),
    (
        "reliability-durability",
        30,
        _compile((r"\breliability\b", r"\bdurability\b", r"신뢰성", r"내구")),
    ),
    (
        "quality-supplier",
        28,
        _compile(
            (
                r"\bquality\b",
                r"\bsupplier\b",
                r"vendor\s+quality",
                r"apqp",
                r"ppap",
                r"dfmea",
                r"pfmea",
                r"품질",
                r"협력사",
                r"공급업체",
            )
        ),
    ),
    (
        "npi",
        28,
        _compile((r"\bnpi\b", r"new\s+product\s+introduction", r"선행\s*양산", r"신제품\s*도입")),
    ),
    (
        "electrical-hardware",
        26,
        _compile(
            (
                r"\belectrical\b",
                r"\belectronics\b",
                r"\bhardware\b",
                r"\bembedded\b",
                r"\bfirmware\b",
                r"motor\s+(control|drive|design)",
                r"power\s+electronics",
                r"\bactuator\b",
                r"\bsilicon\b",
                r"\bsemiconductor\b",
                r"\bsoc\b",
                r"system[- ]on[- ]chip",
                r"전기",
                r"전장",
                r"하드웨어",
                r"임베디드",
                r"모터",
                r"제어",
            )
        ),
    ),
)

MIN_PROFILE_FIT_SCORE = 26
DOMAIN_FIT_LABELS = frozenset(label for label, _, _ in FIT_RULES if label != "technical-program")

# A title/department fit keyword is not enough by itself. The owner-domain
# connection must also be visible in the title or department; body-only
# references remain raw evidence. These buckets describe physical products,
# their industrialization, and their test/quality lifecycle rather than a
# generic operations or software context.
OWNER_DOMAIN_RULES: tuple[tuple[str, tuple[re.Pattern[str], ...]], ...] = (
    (
        "automotive-mobility",
        _compile(
            (
                r"\bautomotive\b",
                r"\bvehicle(?:s)?\b",
                r"\bmobility\b",
                r"\belectric\s+vehicle(?:s)?\b",
                r"\be[- ]mobility\b",
                r"\bev\b",
                r"자동차",
                r"차량",
                r"모빌리티",
                r"전기차",
            )
        ),
    ),
    (
        "motor-power-electronics",
        _compile(
            (
                r"\bmotor(?:s)?\b",
                r"\bpower\s+electronics?\b",
                r"\bpowertrain\b",
                r"\binverter(?:s)?\b",
                r"\bbattery(?:\s+management)?\b",
                r"\bbms\b",
                r"모터",
                r"전력전자",
                r"파워트레인",
                r"인버터",
                r"배터리",
                r"전동화",
            )
        ),
    ),
    (
        "embedded-electrical-hardware",
        _compile(
            (
                r"\bembedded\b",
                r"\bfirmware\b",
                r"\belectrical\b",
                r"\belectronics?\b",
                r"\bhardware\b",
                r"\bpcb\b",
                r"\bcircuit(?:s)?\b",
                r"전기",
                r"전장",
                r"전자",
                r"하드웨어",
                r"임베디드",
                r"펌웨어",
            )
        ),
    ),
    (
        "robotics-industrial-automation",
        _compile(
            (
                r"\brobot(?:ics)?\b",
                r"\bindustrial\s+automation\b",
                r"\bautomation\b",
                r"\bmotion\s+control\b",
                r"\bmechatronics\b",
                r"로봇",
                r"자동화",
                r"메카트로닉스",
            )
        ),
    ),
    (
        "industrial-manufacturing-transformation",
        _compile(
            (
                r"\bindustrial\b",
                r"\bmanufacturing\b",
                r"\bsmart\s+factory\b",
                r"\bfactory\b",
                r"\bplant\b",
                r"\bproduction\b",
                r"\bprocess(?:es)?\b",
                r"\bphysical\s+(?:systems?|products?)\b",
                r"산업",
                r"제조",
                r"스마트\s*팩토리",
                r"공장",
                r"플랜트",
                r"생산",
                r"공정",
                r"물리\s*(?:시스템|제품)",
            )
        ),
    ),
    (
        "machinery-equipment",
        _compile(
            (
                r"\bmachinery\b",
                r"\bmachine(?:s)?\b",
                r"\bequipment\b",
                r"\btooling\b",
                r"\bfixture(?:s)?\b",
                r"\bmanufacturing\s+equipment\b",
                r"설비",
                r"장비",
                r"기계",
                r"치공구",
            )
        ),
    ),
    (
        "physical-product-test-validation-reliability-quality",
        _compile(
            (
                r"\btest\s+(?:lab|engineer(?:ing)?|validation|specialist|technician|infrastructure|lead)\b",
                r"\bvalidation\b",
                r"\bverification\b",
                r"\breliability\b",
                r"\bdurability\b",
                r"\bqualification\s+(?:test|testing|engineer|lab)\b",
                r"\b(?:product|hardware|supplier|process|manufacturing)\s+quality\b",
                r"\bquality\s+(?:engineer(?:ing)?|assurance|control|lab|test|specialist|manager|lead)\b",
                r"\bsupplier\s+quality\b",
                r"시험",
                r"테스트",
                r"검증",
                r"신뢰성",
                r"내구",
                r"품질",
            )
        ),
    ),
    (
        "technical-product-industrialization",
        _compile(
            (
                r"\bmanufacturing\s+(?:engineering|engineer|technology|process)\b",
                r"\bprocess\s+engineer(?:ing)?\b",
                r"\bproduction\s+engineer(?:ing)?\b",
                r"\bindustrial(?:ization|isation)\b",
                r"\bindustrial\s+engineer(?:ing)?\b",
                r"\bnew\s+product\s+introduction\b",
                r"\bnpi\b",
                r"\bproduct\s+industrialization\b",
                r"\bfactory\s+engineering\b",
                r"생산기술",
                r"제조기술",
                r"공정기술",
                r"양산기술",
                r"산업화",
                r"제품\s*양산",
                r"신제품\s*도입",
            )
        ),
    ),
)

CONSUMER_SECTOR_PATTERNS = _compile(
    (
        r"\bbeauty\b",
        r"\bcosmetic(?:s)?\b",
        r"\bfashion\b",
        r"\bapparel\b",
        r"\bgarment\b",
        r"\bclothing\b",
        r"\bunderwear\b",
        r"\bfood\b",
        r"\bbeverage\b",
        r"\be[- ]?commerce\b",
        r"\bconsumer\s+(?:goods|products?)\b",
        r"화장품",
        r"뷰티",
        r"패션",
        r"의류",
        r"언더웨어",
        r"식품",
        r"음료",
        r"이커머스",
        r"커머스",
    )
)

SUPPLY_CHAIN_PATTERNS = _compile(
    (
        r"\bscm\b",
        r"\bsupply\s+chain\b",
        r"\bsourcing\b",
        r"\bprocurement\b",
        r"\bpurchasing\b",
        r"\bbuyer\b",
        r"\bmaterials?\s+(?:sourcing|procurement|purchasing|planner|manager)\b",
        r"소싱",
        r"소재\s*(?:소싱|구매|조달|관리)",
        r"(?:원부자재|자재)\s*(?:소싱|구매|조달|관리|발주)",
        r"공급망",
    )
)

PRODUCTION_MANAGEMENT_PATTERNS = _compile(
    (
        r"\bproduction\s+(?:manager|management|supervisor|lead)\b",
        r"\bmanufacturing\s+(?:manager|management|supervisor|lead)\b",
        r"생산\s*(?:관리|매니저|팀장|책임자|감독)",
        r"제조\s*(?:관리|매니저|팀장|책임자)",
    )
)

# Generic role families are checked against title/department only. A body
# mentioning sales or software is not enough to reject an otherwise specific
# manufacturing role, just as a body mentioning manufacturing is not enough
# to make a generic role actionable.
GENERIC_ROLE_RULES: tuple[tuple[str, tuple[re.Pattern[str], ...]], ...] = (
    (
        "generic-order-management",
        _compile((r"\border\s+management\b", r"order\s+(operations|processing|administrator)")),
    ),
    (
        "generic-cloud-software",
        _compile(
            (
                r"\bcloud\s+(?:solutions?\s+)?(?:architect|engineer|developer)",
                r"\bcloud\s+platform\b",
            )
        ),
    ),
    (
        "generic-sales-marketing-cx",
        _compile(
            (
                r"\bsales?\b",
                r"business\s+development",
                r"account\s+(executive|manager)",
                r"marketing",
                r"growth",
                r"customer\s+(success|support|experience)",
                r"\bcx\b",
                r"public\s+relations",
                r"\bpr\s+manager\b",
                r"communications?\s+manager",
                r"partnerships?\s+manager",
                r"영업",
                r"세일즈",
                r"마케팅",
                r"사업개발",
                r"고객\s*(성공|지원|경험)",
                r"홍보",
                r"파트너십",
            )
        ),
    ),
    (
        "generic-ai-software",
        _compile(
            (
                r"(?<![A-Za-z])ai(?![A-Za-z])",
                r"artificial\s+intelligence",
                r"machine\s+learning",
                r"\bml\b",
                r"data\s+(scientist|analyst|engineer)",
                r"\bsoftware\b",
                r"backend",
                r"front[- ]?end",
                r"full[- ]?stack",
                r"web\s+(developer|engineer)",
                r"mobile\s+(developer|engineer)",
                r"devops",
                r"platform\s+(engineer|developer)",
                r"mlops",
                r"소프트웨어",
                r"개발자",
                r"백엔드",
                r"프론트엔드",
                r"풀스택",
                r"데이터\s*(엔지니어|사이언티스트|분석가)",
            )
        ),
    ),
)

UNRELATED_MANAGER_PATTERNS = _compile(
    (
        r"\b(manager|director|head)\b",
        r"\blead\b",
        r"매니저",
        r"리드",
        r"책임자",
        r"팀장",
    )
)

# A generic AI/software title may still be a physical/industrial AI role when
# the title or department says so explicitly. Test/quality/reliability alone
# are deliberately not exceptions: software QA and AI reliability are common
# false positives in the collected corpus.
PHYSICAL_AI_SOFTWARE_CONTEXT = _compile(
    (
        r"\bphysical\s+ai\b",
        r"\bindustrial\s+ai\b",
        r"\brobot(?:ics)?\b",
        r"\bautomation\b",
        r"\bdigital\s+twin\b",
        r"\bsimulation\b",
        r"\bvision\b",
        r"\bhardware\b",
        r"\bembedded\b",
        r"\bfirmware\b",
        r"\belectrical\b",
        r"\belectronics\b",
        r"manufacturing",
        r"production",
        r"process\s+engineer",
        r"factory",
        r"industrial",
        r"\bnpi\b",
        r"supplier",
        r"apqp|ppap|dfmea|pfmea",
        r"hardware[- ]in[- ]the[- ]loop",
        r"semiconductor|silicon|\bsoc\b|system[- ]on[- ]chip",
        r"vehicle|automotive|robot|motor|actuator",
        r"산업|피지컬\s*(?:AI|인공지능)?|로봇(?:틱스)?|자동화|디지털\s*트윈|시뮬레이션|비전",
        r"전기|전장|하드웨어|임베디드|제조|생산|공정|양산|협력사|공급업체|모터",
    )
)

# Kept as a compatibility surface for callers that used the old flat tuple.
GENERIC_EXCLUSION_PATTERNS = _compile(
    pattern.pattern
    for _, patterns in GENERIC_ROLE_RULES
    for pattern in patterns
)

ITAR_PATTERNS = _compile(
    (
        r"\bitar\b",
        r"international\s+traffic\s+in\s+arms",
        r"export[- ]control",
        r"export[- ]controlled",
        r"\b(?:u\.?s\.?|united states)[- ]person\b",
        r"\b(?:u\.?s\.?|united states)[- ]citizen\b",
        r"\b(?:u\.?s\.?|united states)\s+citizens?\s+only\b",
        r"security\s+clearance",
        r"top[- ]secret",
        r"ts/?sci",
    )
)

ANTI_SPONSORSHIP_PATTERNS = _compile(
    (
        r"(?:do(?:es)?\s+not|cannot|can't|unable\s+to|will\s+not|won't)\s+"
        r"(?:offer|provide)?\s*(?:visa\s+|work\s+)?sponsor",
        r"no\s+(?:visa\s+)?sponsorship",
        r"sponsorship\s+(?:is\s+)?not\s+(?:available|offered|provided)",
        r"without\s+(?:visa\s+)?sponsorship",
        r"must\s+already\s+(?:have|possess|hold)\s+(?:a\s+)?work\s+(?:authorization|permit)",
        r"(?:existing|current|pre-existing)\s+work\s+(?:authorization|permit)",
    )
)

# These patterns intentionally require an affirmative sponsorship statement.
# H-1B/OPT/relocation mentions by themselves are not a credible promise.
SPONSORSHIP_CREDIBLE_PATTERNS = _compile(
    (
        r"visa\s+sponsorship\s+(?:is\s+)?(?:available|offered|provided)",
        r"(?:we|the\s+company)\s+sponsor(?:s)?\s+(?:work\s+)?visas?",
        r"sponsor(?:s|ing|ed)?\s+(?:a\s+)?(?:work\s+)?visas?",
        r"sponsorship\s+(?:is\s+)?(?:available|offered|provided)",
    )
)

REMOTE_SCOPE_PATTERNS = _compile(
    (
        r"\bremote\b[^.\n]{0,80}\bworldwide\b",
        r"\bworldwide\b[^.\n]{0,80}\bremote\b",
        r"\bremote\b[^.\n]{0,80}anywhere\s+in\s+the\s+world",
        r"\bwork\s+from\s+anywhere(?:\s+in\s+the\s+world)?",
        r"\bremote\b[^.\n]{0,80}\bglobal(?:ly)?\b",
        r"\bglobal(?:ly)?\b[^.\n]{0,80}\bremote\b",
        r"\bremote\b[^.\n]{0,80}(?:korea|south\s+korea|apac|asia[- ]?pacific)",
        r"(?:korea|south\s+korea|apac|asia[- ]?pacific)[^.\n]{0,80}\bremote\b",
        r"remote\s+from\s+(?:anywhere|all\s+locations)",
    )
)

REMOTE_ROLE_PATTERNS = _compile(
    (
        r"\bfully?\s+remote\b",
        r"\b100%\s+remote\b",
        r"\bremote[- ]first\b",
        r"\bremote[- ]eligible\b",
        r"\bremote\b\s*[-:–—]\s*[A-Za-z]",
        r"\bremote\s+(position|opportunity|role|job|work)\b",
        r"\bwork\s+(from|remotely)\s+(home|anywhere)\b",
        r"원격\s*(근무|가능|포지션|직무)",
        r"재택\s*(근무|가능|포지션|직무)",
    )
)

# A Wanted location can be only a Korean administrative component such as
# ``금천구``. Keep this bounded to Hangul followed by an address suffix so a
# bare Korean word in a title or JD body cannot create Korea eligibility.
KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN = re.compile(
    r"(?<![가-힣])[가-힣]{1,8}(?:특별시|광역시|특별자치시|특별자치도|시|군|구|도)"
    r"(?![가-힣])"
)

KOREA_PATTERNS = _compile(
    (
        r"south\s+korea",
        r"\bkorea\b",
        r"\bseoul\b",
        r"\bbusan\b",
        r"\bincheon\b",
        r"\bdaejeon\b",
        r"서울",
        r"부산",
        r"인천",
        r"대전",
        r"경기",
        KOREAN_ADMINISTRATIVE_ADDRESS_PATTERN.pattern,
    )
)

US_ONLY_PATTERNS = _compile(
    (
        r"\bus[- ]only\b",
        r"\bu\.s\.?[- ]only\b",
        r"united[- ]states[- ]only",
        r"only[- ](?:in[- ])?(?:the[- ])?u\.?(?:s\.?|sa)\b",
        r"only[- ]hire(?:s|ing)?[- ](?:in[- ])?(?:the[- ])?(?:u\.s\.?|united[- ]states)",
    )
)

FEASIBILITY_PRIORITY = {
    "korea": 0,
    "korea-apac": 1,
    "remote": 2,
    "sponsorship-likely": 3,
}

REASON_LABELS = {
    "actionable": "지원 검토 가능",
    "blocked-itar": "지원 불가 · ITAR/미국인 요건",
    "visa-needed": "정보성 · 비자 필요(스폰서 미확인)",
    "sponsorship-unconfirmed": "정보성 · 스폰서 근거 불충분",
    "apac-work-authorization-unconfirmed": "정보성 · 한국 외 APAC 근무허가 미확인",
    "us-only-remote": "지원 불가 · 미국 전용 원격",
    "remote-scope-unclear": "정보성 · 원격 허용 범위 불명확",
    "generic-order-management": "정보성 · Order Management",
    "generic-cloud-software": "정보성 · 일반 cloud/software",
    "generic-sales-marketing-cx": "정보성 · 영업/마케팅/CX",
    "generic-ai-software": "정보성 · 일반 AI/소프트웨어",
    "consumer-sector": "정보성 · 소비재 beauty/fashion/food/e-commerce",
    "generic-supply-chain": "정보성 · SCM/소싱 중심",
    "generic-production-management": "정보성 · 일반 생산관리",
    "unrelated-manager": "정보성 · 프로필 밖 manager",
    "technical-signal-required": "정보성 · AI/컨설팅 기술 신호 부족",
    "owner-domain-required": "정보성 · 물리/산업 owner-domain 부족",
    "outside-profile": "정보성 · 프로필 범위 밖",
}


def _text(posting: Mapping[str, object]) -> tuple[str, str, str]:
    title = str(posting.get("title") or posting.get("position") or "")
    department = str(posting.get("department") or "")
    body = str(posting.get("body") or posting.get("description") or posting.get("excerpt") or "")
    return title, department, body


def _title_department(posting: Mapping[str, object]) -> str:
    title, department, _ = _text(posting)
    return f"{title} {department}"


def _technical_signal_evidence(posting: Mapping[str, object]) -> list[str]:
    """Return AI/consulting signals from title or department only."""
    title_department = _title_department(posting)
    return [
        label
        for label, patterns in TECHNICAL_AI_CONSULTING_RULES
        if any(pattern.search(title_department) for pattern in patterns)
    ]


def _explicit_tracks(posting: Mapping[str, object]) -> list[object]:
    values: list[object] = []
    for key in ("track", "search_lane", "search_lanes"):
        value = posting.get(key)
        if isinstance(value, (list, tuple, set)):
            values.extend(value)
        elif value:
            values.append(value)
    return values


def _resolved_track(
    posting: Mapping[str, object], technical_signal_evidence: list[str]
) -> str:
    """Resolve persisted search metadata, then infer a lane for legacy rows."""
    explicit = primary_track(_explicit_tracks(posting))
    inferred = (
        TRACK_ENGINEERING_CONSULTING
        if set(technical_signal_evidence) & CONSULTING_SIGNAL_LABELS
        else TRACK_AI_NATIVE
        if technical_signal_evidence
        else TRACK_CORE
    )
    # A non-core persisted lane is authoritative. A legacy/core row whose title
    # clearly belongs to a new lane is inferred into that lane so it is not
    # silently mixed into the core report.
    return explicit if explicit != TRACK_CORE else inferred


def _haystack(posting: Mapping[str, object]) -> str:
    title, department, body = _text(posting)
    location = str(posting.get("location_raw") or posting.get("location") or "")
    country = str(posting.get("country") or posting.get("country_hint") or "")
    return " ".join((title, department, body, location, country))


def _first_match(patterns: Iterable[re.Pattern[str]], text: str) -> str | None:
    for pattern in patterns:
        if pattern.search(text):
            return pattern.pattern
    return None


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _fit(posting: Mapping[str, object]) -> tuple[int, list[str]]:
    """Score only title/department evidence; body evidence is non-actionable."""
    title, department, _ = _text(posting)
    title_department = f"{title} {department}"
    score = 0
    evidence: list[str] = []
    for label, weight, patterns in FIT_RULES:
        if any(pattern.search(title_department) for pattern in patterns):
            score += weight
            evidence.append(label)
    return score, evidence


def _owner_domain_evidence(posting: Mapping[str, object]) -> list[str]:
    """Return owner-domain matches from title/department only."""
    title, department, _ = _text(posting)
    title_department = f"{title} {department}"
    return [
        label
        for label, patterns in OWNER_DOMAIN_RULES
        if any(pattern.search(title_department) for pattern in patterns)
    ]


def _profile_fit_is_sufficient(
    fit_score: int,
    fit_evidence: list[str],
    owner_domain_evidence: list[str],
) -> bool:
    if fit_score < MIN_PROFILE_FIT_SCORE or not fit_evidence:
        return False
    # A fit keyword such as "manufacturing" or "quality" is too broad by
    # itself. A deterministic shortlist also needs a credible physical-product
    # owner domain in the title/department. Body-only mentions never satisfy
    # this gate.
    return bool(set(fit_evidence) & DOMAIN_FIT_LABELS) and bool(owner_domain_evidence)


def _generic_reason(
    posting: Mapping[str, object],
    fit_score: int,
    fit_evidence: list[str],
    owner_domain_evidence: list[str],
) -> str | None:
    title, department, _ = _text(posting)
    title_department = f"{title} {department}"
    if _first_match(CONSUMER_SECTOR_PATTERNS, title_department):
        return "consumer-sector"
    if _first_match(SUPPLY_CHAIN_PATTERNS, title_department):
        return "generic-supply-chain"
    if _first_match(PRODUCTION_MANAGEMENT_PATTERNS, title_department):
        return "generic-production-management"
    for reason, patterns in GENERIC_ROLE_RULES:
        if not _first_match(patterns, title_department):
            continue
        if reason == "generic-ai-software":
            if _first_match(PHYSICAL_AI_SOFTWARE_CONTEXT, title_department):
                continue
        return reason
    if _first_match(UNRELATED_MANAGER_PATTERNS, title_department):
        if not _profile_fit_is_sufficient(fit_score, fit_evidence, owner_domain_evidence):
            return "unrelated-manager"
    return None


def _feasibility(posting: Mapping[str, object], haystack: str) -> tuple[bool, str, str]:
    bucket = str(posting.get("eligibility") or "")
    country = str(posting.get("country") or posting.get("country_hint") or "")
    location = str(posting.get("location_raw") or posting.get("location") or "")
    itar = bucket == "blocked-itar" or bool(_first_match(ITAR_PATTERNS, haystack))
    if itar:
        return False, "blocked-itar", "blocked-itar"

    anti_sponsor = bool(_first_match(ANTI_SPONSORSHIP_PATTERNS, haystack))
    credible_sponsor = bool(_first_match(SPONSORSHIP_CREDIBLE_PATTERNS, haystack))

    # An explicit collector bucket is a negative eligibility signal. Only a
    # later, affirmative sponsorship statement can replace a stale
    # visa-needed label; an otherwise-local-looking location must not silently
    # promote a posting the source marked as requiring a visa.
    if bucket == "visa-needed" and not credible_sponsor:
        return False, "visa-needed", "visa-needed"

    if bucket == "korea" or any(pattern.search(f"{location} {country}") for pattern in KOREA_PATTERNS):
        if anti_sponsor:
            return False, "visa-needed", "visa-needed"
        return True, "korea", "korea"
    if bucket == "korea-apac":
        # This bucket means the posting is in Singapore/India/Taiwan/Japan or
        # another non-Korea APAC location. It is not Korean work authorization.
        # Promote it only when the JD itself affirmatively confirms sponsorship.
        if credible_sponsor and not anti_sponsor:
            return True, "sponsorship-likely", "sponsorship-likely"
        return False, "apac-work-authorization-unconfirmed", "korea-apac"

    remote = bucket == "remote" or posting.get("remote_flag") is True or bool(
        _first_match(REMOTE_ROLE_PATTERNS, haystack)
        or _first_match(REMOTE_SCOPE_PATTERNS, haystack)
    )
    if remote:
        # An explicit negative must win over a broad positive, e.g. a posting
        # whose boilerplate says both "remote globally" and "US only".
        if _first_match(US_ONLY_PATTERNS, haystack):
            return False, "us-only-remote", "remote"
        if anti_sponsor:
            return False, "visa-needed", "visa-needed"
        if _first_match(REMOTE_SCOPE_PATTERNS, haystack):
            return True, "remote", "remote"
        return False, "remote-scope-unclear", "remote"

    if bucket == "sponsorship-likely" or credible_sponsor:
        if credible_sponsor and not anti_sponsor:
            return True, "sponsorship-likely", "sponsorship-likely"
        return False, "sponsorship-unconfirmed", "visa-needed"

    # A non-local, non-remote role with no affirmative sponsorship statement is
    # never promoted by the shortlist layer.
    return False, "visa-needed", "visa-needed"


def assess_shortlist(posting: Mapping[str, object]) -> dict[str, object]:
    """Return deterministic actionability, reason, evidence, and fit score."""
    haystack = _haystack(posting)
    feasible, feasibility_reason, feasibility_bucket = _feasibility(posting, haystack)
    fit_score, fit_evidence = _fit(posting)
    owner_domain_evidence = _owner_domain_evidence(posting)
    technical_signal_evidence = _technical_signal_evidence(posting)
    track = _resolved_track(posting, technical_signal_evidence)
    generic_reason = _generic_reason(
        posting, fit_score, fit_evidence, owner_domain_evidence
    )

    if not feasible:
        reason = feasibility_reason
        actionable = False
    elif generic_reason:
        reason = generic_reason
        actionable = False
    elif track != TRACK_CORE and not technical_signal_evidence:
        reason = "technical-signal-required"
        actionable = False
    elif track != TRACK_CORE and not owner_domain_evidence:
        reason = "owner-domain-required"
        actionable = False
    elif not _profile_fit_is_sufficient(
        fit_score, fit_evidence, owner_domain_evidence
    ):
        reason = "outside-profile"
        actionable = False
    else:
        reason = "actionable"
        actionable = True

    return {
        "actionable": actionable,
        "reason": reason,
        "feasibility": feasibility_bucket,
        "track": track,
        "fit_score": fit_score,
        "fit_evidence": fit_evidence,
        "technical_signal_evidence": technical_signal_evidence,
        "owner_domain_evidence": owner_domain_evidence,
    }


def reason_label(reason: str) -> str:
    """Return the stable Korean report label for an internal reason code."""
    return REASON_LABELS.get(reason, reason)


def annotate_shortlist(postings: Iterable[dict]) -> list[dict]:
    """Annotate postings in place and return them in their original order."""
    annotated = []
    for posting in postings:
        posting.update(assess_shortlist(posting))
        annotated.append(posting)
    return annotated


def rank_actionable(postings: Iterable[dict]) -> list[dict]:
    """Annotate and return only actionable postings, highest fit first."""
    annotated = annotate_shortlist(postings)
    return sorted(
        (posting for posting in annotated if posting["actionable"]),
        key=lambda posting: (
            FEASIBILITY_PRIORITY.get(str(posting.get("feasibility") or ""), 99),
            -_safe_int(posting.get("fit_score")),
            -_safe_int(posting.get("score")),
            str(posting.get("company") or "").casefold(),
            str(posting.get("title") or posting.get("position") or "").casefold(),
            str(posting.get("job_id") or posting.get("id") or ""),
        ),
    )
