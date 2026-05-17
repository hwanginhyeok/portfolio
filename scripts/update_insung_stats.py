"""
인성이 Supabase에서 실 운영 지표를 읽어 src/data/insung_stats.json 갱신.

환경변수 (GitHub Secrets 또는 로컬 .env):
  INSUNG_SUPABASE_URL
  INSUNG_SUPABASE_SERVICE_ROLE_KEY

실행:
  python scripts/update_insung_stats.py
"""
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

SUPABASE_URL = os.environ.get("INSUNG_SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("INSUNG_SUPABASE_SERVICE_ROLE_KEY", "")
STATS_PATH = Path(__file__).resolve().parent.parent / "src" / "data" / "insung_stats.json"


def supabase_count(table: str) -> int | None:
    """PostgREST exact-count로 row 수만 가져오기. 실패 시 None."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return None
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*"
    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Prefer": "count=exact",
            "Range": "0-0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_range = resp.headers.get("Content-Range", "")
            # 형식: "0-0/123" 또는 "*/0"
            if "/" in content_range:
                total = content_range.split("/")[-1]
                return int(total) if total.isdigit() else 0
    except urllib.error.HTTPError as e:
        print(f"  [{table}] HTTP {e.code}: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"  [{table}] ERROR: {e}", file=sys.stderr)
    return None


def main() -> int:
    if not (SUPABASE_URL and SUPABASE_KEY):
        print("ERROR: INSUNG_SUPABASE_URL / INSUNG_SUPABASE_SERVICE_ROLE_KEY 미설정", file=sys.stderr)
        return 2

    print(f"Supabase: {SUPABASE_URL}")
    print("테이블 카운트 조회 중...")

    counts = {
        "comments_generated": supabase_count("comment_activity"),
        "incoming_comments": supabase_count("incoming_comments"),
        "neighbor_candidates": supabase_count("neighbor_candidates"),
        "active_personas": supabase_count("example_personas"),
        "support_tickets": supabase_count("support_tickets"),
    }
    for k, v in counts.items():
        print(f"  {k}: {v}")

    # 기존 JSON 로드
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))

    # live_metrics 섹션 갱신 (기존 phases/tech_stack 등은 보존)
    stats["live_metrics"] = {
        "comments_generated": counts["comments_generated"] or 0,
        "incoming_comments": counts["incoming_comments"] or 0,
        "neighbor_candidates": counts["neighbor_candidates"] or 0,
        "active_personas": counts["active_personas"] or 0,
        "support_tickets": counts["support_tickets"] or 0,
        "last_synced": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    stats["_note"] = f"자동 갱신 (last sync: {stats['live_metrics']['last_synced']})"

    STATS_PATH.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\n✅ {STATS_PATH.relative_to(STATS_PATH.parent.parent.parent)} 갱신 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
