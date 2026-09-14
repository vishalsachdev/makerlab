# Disabled skills (archived 2026-09-14, off-season)

Summer camp skills, moved out of `.claude/skills/` so they stop loading into every
session's skill list. The next camp season is about 8 months out (summer 2027).
Nothing is deleted.

- `camp-welcome-emails` - weekly parent welcome emails for next Monday's camps
- `handle-camp-cancellation` - cancellation intake, refund tier, business-office memo,
  FormBuilder cancel, waitlist backfill

## Restore (target: January 2027, before registration opens)

    git mv .claude/skills-disabled/camp-welcome-emails .claude/skills/camp-welcome-emails
    git mv .claude/skills-disabled/handle-camp-cancellation .claude/skills/handle-camp-cancellation

Also re-enable the availability workflow (disabled in GitHub 2026-09-14, schedule
commented out since 2026-08-03), after renewing `FORMBUILDER_TOKEN` (expires 11/08/2026):

    gh workflow enable 275662132 -R vishalsachdev/makerlab
    # then uncomment the schedule block in .github/workflows/update-availability.yml

The makerlab-camps "Generate weekly camp rosters" workflow has been disabled since the
2026 season ended; enable it there too if rosters are needed.

Restore before running either skill. `camp-welcome-emails/SKILL.md` calls its scripts
by the `.claude/skills/camp-welcome-emails/scripts/...` path.

## Inbound pointers (checked 2026-09-14)

- `scripts/podio/find_cancellation_requests.py` names `handle-camp-cancellation` in its
  docstring (Step 0 intake). Harmless while archived.
- Session log entries in `docs/session-archive.md` mention both skills (history only).

## Related archived memory

The camp-season Claude memories (refund tiers, FormBuilder login and answer-edit
gotchas, refund-confirmation mailbox split, waitlist hold window) were moved to
`~/.claude/projects/-Users-vishal-code-makerlab/memory/archive/` on the same day.
Several of those facts are already inside these skills.

## Before the 2027 season, also check

- `summer.html` posts the 8-20 day refund tier as "Half refund minus the $20
  non-refundable deposit", while the cancellation skill and the ops runbook apply
  50% flat with no deposit deduction. Make them agree before registration opens.
