#!/usr/bin/env python3
"""Generate the static project overview from feature docs and ops/ops.yaml."""
from __future__ import annotations

import html
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "features"
OPS_FILE = ROOT / "ops" / "ops.yaml"
OUTPUT = ROOT / "site" / "index.html"

FEATURE_LABELS = {
    "astro-portfolio": "Astro 포트폴리오 웹사이트 (astro-portfolio)",
    "jasoseol-collector": "자소설닷컴 공고 수집 엔진 (jasoseol-collector)",
    "jasoseol-report": "자소설닷컴 일일 리포트 & 운영 알림 (jasoseol-report)",
    "jasoseol-calendar": "캘린더 마감일정 동기화 (jasoseol-calendar)",
    "wanted-collector": "원티드 채용공고 수집 & 상태관리 (wanted-collector)",
    "global-collector": "글로벌 ATS 기업공고 수집 (global-collector)",
    "applications-ledger": "지원 파이프라인 원장 & 현황 (applications-ledger)",
    "presentation-builder": "대학원 포트폴리오 PPT 생성기 (presentation-builder)",
    "harness-scheduling": "macOS 예약 작업 & 하네스 연동 (harness-scheduling)",
}


def _feature_rows() -> str:
    rows = []
    for path in sorted(FEATURES_DIR.glob("*.md")):
        if path.name in {"_template.md", "README.md"}:
            continue
        label = FEATURE_LABELS.get(path.stem, path.stem)
        title = html.escape(label)
        href = html.escape(f"../features/{path.name}", quote=True)
        rows.append(
            f'<tr><th scope="row"><a href="{href}">{title}</a></th>'
            f'<td><code>features/{path.name}</code></td></tr>'
        )
    return "\n".join(rows)


def _service_rows(data: dict) -> str:
    rows = []
    services = data.get("services", [])
    if not services:
        return '<tr><td colspan="5" style="text-align: center; color: #64748b;">상시 데몬 없음 (배치 크론 작업 기반)</td></tr>'
    for svc in services:
        svc_id = html.escape(str(svc.get("id", "service:unknown")))
        what = html.escape(str(svc.get("what", "unknown")))
        unit = html.escape(str(svc.get("systemd_unit", "unknown")))
        node = html.escape(str(svc.get("node", data.get("current_node", "unknown"))))
        status = html.escape(str(svc.get("status", "active")))
        secrets = ", ".join(html.escape(str(s)) for s in svc.get("secrets", [])) or "없음"
        rows.append(
            f"<tr><td>{svc_id}</td><td>{what}</td><td><code>{unit}</code></td>"
            f"<td>{node} ({status})</td><td>{secrets}</td></tr>"
        )
    return "\n".join(rows)


def _cron_rows(data: dict) -> str:
    rows = []
    for job in data.get("cron", []):
        job_id = html.escape(str(job.get("id", "cron:unknown")))
        what = html.escape(str(job.get("what", "unknown")))
        schedule = html.escape(str(job.get("schedule", "unknown")))
        node = html.escape(str(job.get("node", data.get("current_node", "unknown"))))
        status = html.escape(str(job.get("status", "active")))
        secrets = ", ".join(html.escape(str(s)) for s in job.get("secrets", [])) or "없음"
        rows.append(
            f"<tr><td>{job_id}</td><td>{what}</td><td><code>{schedule}</code></td>"
            f"<td>{node} ({status})</td><td>{secrets}</td></tr>"
        )
    return "\n".join(rows)


def render() -> str:
    data = yaml.safe_load(OPS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("ops/ops.yaml must contain a mapping")

    services = data.get("services", [])
    cron = data.get("cron", [])
    latest_health = data.get("latest_health", {})
    notes = "\n".join(
        f"<li>{html.escape(str(note))}</li>"
        for note in data.get("notes", [])
    )
    state_paths = "\n".join(
        f"<li><code>{html.escape(str(path))}</code></li>"
        for path in data.get("state_paths", [])
    )
    dependencies = "\n".join(
        f"<li><code>{html.escape(str(item))}</code></li>"
        for item in data.get("external_dependencies", [])
    )
    external_sites = "\n".join(
        f'<li><a href="{html.escape(str(item), quote=True)}">{html.escape(str(item))}</a></li>'
        for item in data.get("external_sites", [])
    )
    secrets_list = ", ".join(
        f"<code>{html.escape(str(s))}</code>"
        for s in data.get("secrets", [])
    ) or "없음"
    health_checks = "\n".join(
        f"<li><code>{html.escape(str(item))}</code></li>"
        for item in data.get("health_checks", [])
    )

    feature_count = len([p for p in FEATURES_DIR.glob("*.md") if p.name not in {"_template.md", "README.md"}])

    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portfolio & 채용 수집 파이프라인 운영 개요</title>
  <style>
    :root {{ color-scheme: light; font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #202938; background: #f5f7fa; }}
    body {{ max-width: 1040px; margin: 2rem auto; padding: 0 1rem 3rem; }}
    h1, h2, h3 {{ line-height: 1.25; color: #0f172a; }}
    section {{ margin: 2rem 0; padding: 1.25rem 1.5rem; background: white; border: 1px solid #dbe2ea; border-radius: 12px; }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; margin-top: 0.5rem; }}
    th, td {{ padding: .65rem .75rem; border-bottom: 1px solid #e4e9ef; vertical-align: top; }}
    th {{ background: #f8fafc; font-weight: 600; }}
    code {{ background: #eef2f6; padding: 0.15rem 0.35rem; border-radius: 4px; font-size: 0.9em; }}
    .meta {{ color: #536174; font-size: 0.95rem; }}
    .notice {{ border-left: 5px solid #0284c7; background: #f0f9ff; }}
    .badge {{ display: inline-block; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; background: #dbeafe; color: #1e40af; }}
    .status-ok {{ color: #15803d; font-weight: 600; }}
  </style>
</head>
<body>
  <header>
    <h1>Portfolio & 채용 인텔리전스 파이프라인 운영 개요</h1>
    <p>Astro 기반 엔지니어링 포트폴리오 웹사이트 + 자동화 채용 공고 수집, 캘린더 동기화 및 운영 봇 일일 브리핑 파이프라인.</p>
    <p class="meta">운영 노드: <strong>{html.escape(str(data.get("current_node", "unknown")))}</strong> · 기준일: <strong>{html.escape(str(data.get("last_verified", "unknown")))}</strong> · 시간대: {html.escape(str(data.get("timezone", "unknown")))}</p>
  </header>

  <section class="notice">
    <h2>운영 상태 및 안내</h2>
    <p><strong>server-pc 운영 유지 중</strong>: 6개의 채용 수집 및 리포트 크론 작업이 server-pc에서 정상 작동 중이며, Mac 작업트리는 서버 작업을 일체 중단하거나 변경하지 않습니다.</p>
    <ul>{notes}</ul>
  </section>

  <section>
    <h2>주요 기능 ({feature_count})</h2>
    <table>
      <thead><tr><th>기능</th><th>문서 링크</th></tr></thead>
      <tbody>
        {_feature_rows()}
      </tbody>
    </table>
  </section>

  <section>
    <h2>상시 서비스 ({len(services)})</h2>
    <table>
      <thead><tr><th>식별자</th><th>역할</th><th>단위 / 명령어</th><th>노드 (상태)</th><th>필요 시크릿</th></tr></thead>
      <tbody>
        {_service_rows(data)}
      </tbody>
    </table>
  </section>

  <section>
    <h2>예약 작업 ({len(cron)})</h2>
    <table>
      <thead><tr><th>식별자</th><th>작업 내용</th><th>일정</th><th>노드 (상태)</th><th>필요 시크릿</th></tr></thead>
      <tbody>
        {_cron_rows(data)}
      </tbody>
    </table>
  </section>

  <section>
    <h2>최신 건전성 및 검증 상태</h2>
    <p class="status-ok">상태: {html.escape(str(latest_health.get("status", "unknown")))} (확인 시각: {html.escape(str(latest_health.get("checked_at", "미기록")))})</p>
    <p>{html.escape(str(latest_health.get("note", "기록 없음")))}</p>
    <h3>정기 확인 항목</h3>
    <ul>{health_checks}</ul>
  </section>

  <section>
    <h2>상태 및 저장소 경로</h2>
    <ul>{state_paths}</ul>
  </section>

  <section>
    <h2>시크릿 카탈로그 (키체인 명칭 전용)</h2>
    <p>{secrets_list}</p>
  </section>

  <section>
    <h2>외부 연동 및 의존성</h2>
    <h3>의존성</h3>
    <ul>{dependencies}</ul>
    <h3>외부 사이트</h3>
    <ul>{external_sites}</ul>
  </section>
</body>
</html>
'''


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = render()
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} ({len(rendered)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
