# _agent-inbox

Handoffs between agents for the makerlab repo. Follows the fleet protocol in vishalsachdev/code-control-ledger (`docs/cross-family-source-of-truth-protocol-2026-10-09.md` and `_agent-inbox/README.md`).

- One Markdown file per item, named `YYYY-MM-DD-short-title.md`.
- Header: To, From, Repo, File, Kind, Priority, Requested by, Authored and committed by, Needs Vishal. Sections: What, Why, Notes.
- Pending item bodies are not edited. When done, move the item to `done/` and add a `## Result` block. Done items are kept.
- Grok bots only file items here or move their own items to `done/`. They make no content changes elsewhere in this repo.
- No camper, parent, student or registration data in any item. This repo is public.
