"""Offline tests for scripts/apply_flow.py and scripts/apply_browser.py (t265)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from scripts import apply_browser, apply_flow

TODAY = date(2026, 10, 14)


def wanted_md(job_id: str, company: str, title: str, body: str = "", due: str | None = None) -> str:
    meta = {"wanted_id": int(job_id), "company": company, "position": title,
            "url": f"https://www.wanted.co.kr/wd/{job_id}", "location": "서울", "due_time": due,
            "first_seen": "2026-10-01"}
    lines = [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items()]
    return "---\n" + "\n".join(lines) + "\n---\n\n## 주요업무\n\n" + body + "\n"


@pytest.fixture()
def inbox(tmp_path: Path) -> Path:
    folder = tmp_path / "wanted"
    folder.mkdir()
    (folder / "1.md").write_text(wanted_md(
        "1", "모터회사", "BLDC 모터 제어 펌웨어 엔지니어",
        "BLDC 모터 인버터 제어, 임베디드 펌웨어, CAN 통신, 시험 및 양산 이관"), encoding="utf-8")
    (folder / "2.md").write_text(wanted_md(
        "2", "웹회사", "React Next.js 기반 서비스 QA 테스트 자동화 엔지니어",
        "React, Next.js, Spring Boot 서비스 테스트 자동화"), encoding="utf-8")
    (folder / "3.md").write_text(wanted_md(
        "3", "마감회사", "BLDC 모터 제어 엔지니어", "모터 제어", due="2026-10-01"), encoding="utf-8")
    (folder / "4.md").write_text(wanted_md(
        "4", "이미지원", "BLDC 모터 제어 엔지니어", "모터 제어 임베디드"), encoding="utf-8")
    return tmp_path


@pytest.fixture(scope="module")
def facts() -> list[dict]:
    return apply_flow.load_facts()


def test_parse_frontmatter_roundtrip():
    meta, body = apply_flow.parse_frontmatter(wanted_md("9", "A", "B", "본문"))
    assert meta["wanted_id"] == 9 and meta["company"] == "A"
    assert "본문" in body
    assert apply_flow.parse_frontmatter("no frontmatter")[0] == {}


def test_load_candidates_marks_form_kind(inbox):
    postings = apply_flow.load_candidates(inbox)
    assert {p["key"] for p in postings} == {"wanted:1", "wanted:2", "wanted:3", "wanted:4"}
    assert all(p["form"] == "login" for p in postings)
    assert apply_flow.form_kind("https://jobs.lever.co/x/1") == "open"
    assert apply_flow.form_kind("https://aptiv.wd5.myworkdayjobs.com/x") == "login"


def test_shortlist_ranks_domain_fit_and_drops_closed_applied_and_misfit(inbox, tmp_path, facts):
    ledger = tmp_path / "applications.json"
    ledger.write_text(json.dumps({"applications": [{"job_id": "4", "status": "제출"}]}), encoding="utf-8")
    rows = apply_flow.build_shortlist(top=10, inbox=inbox, ledger_path=ledger, today=TODAY, facts=facts)
    keys = [r["key"] for r in rows]
    assert keys[0] == "wanted:1"
    assert "wanted:3" not in keys  # deadline 2026-10-01 already passed
    assert "wanted:4" not in keys  # already in the ledger
    if "wanted:2" in keys:  # web QA may pass the title gate but must rank below
        assert keys.index("wanted:2") > keys.index("wanted:1")
        assert any("no record in profile" in reason for reason in rows[keys.index("wanted:2")]["reasons"])
    assert any("profile domain" in reason for reason in rows[0]["reasons"])


def test_shortlist_drops_duplicate_reposts(tmp_path, facts):
    folder = tmp_path / "wanted"
    folder.mkdir()
    for job_id in ("11", "12"):
        (folder / f"{job_id}.md").write_text(wanted_md(
            job_id, "같은회사", "BLDC 모터 제어 엔지니어", "모터 인버터 임베디드"), encoding="utf-8")
    rows = apply_flow.build_shortlist(top=10, inbox=tmp_path, ledger_path=tmp_path / "none.json",
                                      today=TODAY, facts=facts)
    assert len(rows) == 1


def test_check_open_builds_ats_urls_and_reads_probe():
    seen: list[str] = []

    def probe(url):
        seen.append(url)
        return url.endswith("/4900")

    greenhouse = {"url": "https://job-boards.greenhouse.io/anthropic/jobs/4900", "job_id": "4900",
                  "source": "global"}
    assert apply_flow.check_open(greenhouse, probe) is True
    assert seen[-1] == "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs/4900"
    lever = {"url": "https://jobs.lever.co/shieldai/abc", "job_id": "abc", "source": "global"}
    assert apply_flow.check_open(lever, probe) is False
    assert seen[-1] == "https://api.lever.co/v0/postings/shieldai/abc"


def test_kit_uses_only_profile_lines_and_keeps_todos(inbox, facts):
    posting = apply_flow.find_posting("wanted:1", inbox)
    files = apply_flow.build_kit(posting, facts, ["Why do you want to work here?", "Expected salary"])
    assert sorted(files) == ["1_resume-variant.md", "2_cover-letter-ko.md", "3_cover-letter-en.md",
                             "4_form-answers.md", "5_portfolio-links.md"]
    letter = files["2_cover-letter-ko.md"]
    quoted = [line[2:].rstrip() for line in letter.split("\n") if line.startswith("- ")]
    fact_texts = {f["text"] for f in facts}
    assert quoted, "letter must carry profile evidence"
    assert all(q in fact_texts for q in quoted), "every bullet is a verbatim profile line"
    assert "[TODO: 운영자 입력" in letter
    answers = files["4_form-answers.md"]
    assert "Expected salary" in answers and "[TODO: 운영자 입력 — 희망 연봉]" in answers
    assert apply_flow.SITE_URL in files["5_portfolio-links.md"]


def test_classify_and_answer_questions(facts):
    assert apply_flow.classify_question("Do you require visa sponsorship?") == "authorization"
    assert apply_flow.classify_question("Link to your GitHub") == "links"
    posting = {"title": "Engineer", "company": "X"}
    en = [{"text": "Built a dynamometer torque-control system.", "ref": "resume_en.md"}]
    assert "[TODO" in apply_flow.answer_question("Are you authorized to work here?", en, posting)
    assert apply_flow.GITHUB_URL in apply_flow.answer_question("GitHub profile", en, posting)
    why = apply_flow.answer_question("Why this role?", en, posting)
    assert "dynamometer" in why and "[TODO" in why


def test_track_creates_moves_and_validates(tmp_path, inbox):
    ledger = tmp_path / "applications.json"
    ledger.write_text(json.dumps({"updated_at": "2026-01-01", "applications": []}), encoding="utf-8")
    posting = apply_flow.find_posting("wanted:1", inbox)
    row = apply_flow.track("wanted:1", "준비중", "kit written", ledger, TODAY, posting)
    assert row["status"] == "준비중" and row["applied_at"] is None
    row = apply_flow.track("wanted:1", "제출", ledger_path=ledger, today=TODAY)
    assert row["applied_at"] == "2026-10-14"
    row = apply_flow.track("wanted:1", "면접", "1차 면접 안내", ledger, date(2026, 10, 20))
    data = json.loads(ledger.read_text(encoding="utf-8"))
    assert len(data["applications"]) == 1
    assert [h["status"] for h in data["applications"][0]["history"]] == ["준비중", "제출", "면접"]
    with pytest.raises(SystemExit):
        apply_flow.track("wanted:1", "없는상태", ledger_path=ledger, today=TODAY)
    with pytest.raises(SystemExit):
        apply_flow.track("wanted:99", "제출", ledger_path=ledger, today=TODAY)


def test_browser_never_treats_submit_as_clickable_and_flags_login():
    assert apply_browser.is_submit_control("Submit application")
    assert apply_browser.is_submit_control("지원하기")
    assert not apply_browser.is_submit_control("Add another")
    assert apply_browser.looks_like_login_wall("https://id.wanted.co.kr/login?x=1", "이메일 회원가입")
    assert not apply_browser.looks_like_login_wall("https://jobs.lever.co/x/apply", "Full name Email")


def test_browser_plan_fills_standing_fields_and_leaves_unsourced_empty():
    fields = [{"label": "Email", "type": "email"}, {"label": "GitHub", "type": "text"},
              {"label": "Expected salary", "type": "text"},
              {"label": "Why do you want to work here?", "type": "textarea"}]
    en = [{"text": "Built a dynamometer torque-control system.", "ref": "resume_en.md"}]
    plan = apply_browser.plan_fill(fields, en, {"title": "T", "company": "C"})
    by_label = {row["label"]: row for row in plan}
    assert by_label["Email"]["value"] == apply_browser.STANDING["email"]
    assert by_label["GitHub"]["value"] == apply_flow.GITHUB_URL
    assert by_label["Expected salary"]["value"] is None
    # a draft that still needs the operator is never typed into the form
    assert by_label["Why do you want to work here?"]["value"] is None


# ── pf-2: collector backup ──────────────────────────────────────────────────

def _git(repo: Path, *args: str):
    import subprocess
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True)


def test_backup_commits_only_collector_paths_and_pushes(tmp_path):
    import subprocess
    from datetime import datetime
    from scripts import backup_collected

    repo = tmp_path / "repo"
    (repo / "docs" / "jd" / "_inbox" / "wanted").mkdir(parents=True)
    (repo / "scripts").mkdir()
    _git(tmp_path, "init", "-q", str(repo))
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "scripts" / "keep.py").write_text("x = 1\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "init")
    (repo / "docs/jd/_inbox/wanted/1.md").write_text("posting\n")
    (repo / "scripts" / "keep.py").write_text("x = 2\n")  # source change must NOT be committed

    assert backup_collected.pending_paths(repo) == ["docs/jd/_inbox/wanted/1.md"]
    assert backup_collected.run(repo, apply=False) == 0
    assert _git(repo, "log", "--oneline").stdout.count("\n") == 1  # dry run commits nothing

    calls: list[list[str]] = []
    alerts: list[str] = []

    def runner(cmd, **kwargs):
        calls.append(cmd)
        if cmd[0] == "git":
            return subprocess.run(cmd, **kwargs)
        return subprocess.CompletedProcess(cmd, 0, "", "")  # the fake `hih git push`

    code = backup_collected.run(repo, apply=True, runner=runner,
                                notify=lambda *a, **k: alerts.append(a[0]),
                                now=datetime(2026, 10, 14))
    assert code == 0 and not alerts
    assert calls[-1][1:] == ["git", "push"]
    assert "data: collector snapshot 2026-10-14 (1 files)" in _git(repo, "log", "-1", "--format=%s").stdout
    assert _git(repo, "show", "--name-only", "--format=", "HEAD").stdout.split() == [
        "docs/jd/_inbox/wanted/1.md"]
    assert "scripts/keep.py" in _git(repo, "status", "--porcelain").stdout  # still dirty, untouched
    assert backup_collected.run(repo, apply=True, runner=runner) == 0  # idempotent: nothing pending


def test_backup_failed_push_alerts_operator(tmp_path):
    import subprocess
    from scripts import backup_collected

    repo = tmp_path / "repo"
    (repo / "docs" / "jd" / "_inbox").mkdir(parents=True)
    _git(tmp_path, "init", "-q", str(repo))
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "docs/jd/_inbox/a.md").write_text("a\n")
    alerts: list[tuple] = []

    def runner(cmd, **kwargs):
        if cmd[0] == "git":
            return subprocess.run(cmd, **kwargs)
        return subprocess.CompletedProcess(cmd, 1, "", "gitleaks: leak found")

    code = backup_collected.run(repo, apply=True, runner=runner,
                                notify=lambda text, **k: alerts.append((text, k)))
    assert code == 1
    assert alerts and "push 실패" in alerts[0][0] and alerts[0][1]["level"] == "error"
