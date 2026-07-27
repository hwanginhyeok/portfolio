# Coordination Board

Single shared board for pane-to-pane work messages. This directory is the SSOT for
dispatched work — agents inspect it; they do not act on chat text alone.

Every pane checks `messages/*.md` before starting new work, using ITS identity:
`board.py list --as "<role>,<model>,<pane>,#<seat>"` (always include the role name).

Frontmatter schema (written by `board.py post`):

- `work_id`/`thread_id`/`id`, `from`, `to`, `project`, `session`, `window`, `pane`,
  `model`, `role`, `recipient_number` (`#N`), `kind`, `dispatch_mode` (`hard`|`review`),
  `status`, `source_task`, `reply_expected`, `done_signal`, `evidence_path`, `title`.

Recipient matching — an agent acts on a message iff:
`to == all`  OR  identity ∩ to ≠ ∅  OR  it is the sender. Seats are `#N`-namespaced.

Rules:

- Targeted messages are acted on only by matching recipients; others stay silent.
- Replies append to the same thread under `## Replies` (lock-serialized — parallel
  review replies are never lost).
- PM oversight: `board.py list --all` shows the whole board (every recipient).
- PM closes the thread only when deliverable/evidence is verified.
