# What you missed if you jumped straight here (Phase C)

**The idea, not just the code:** four hook points now exist —
`post-src-checkout` → `prepare-for-tox-run` → `post-tox-run` →
`post-tox-job` — each gated by `hashFiles('.../action.yml') != ''` used as
a poor man's `file.exists()`. Only one is actually implemented here
(`post-tox-run`); the other three are real extension points that
currently do nothing because their `action.yml` files don't exist yet in
this repo. Delete `.github/reusables/.../post-tox-run/action.yml` and
push — the hook cleanly no-ops, no error. That's the whole point: adding
(or removing) a hook never requires touching the reusable workflow's own
code.

**Look at the hook itself**
(`.github/reusables/tox-dev/workflow/reusable-tox/hooks/post-tox-run/action.yml`):
it renders coverage as a markdown table in the job summary —
`tox exec --skip-pkg-install --quiet -- coverage report --format=markdown
>> "$GITHUB_STEP_SUMMARY"` — gated on
`fromJSON(inputs.calling-job-context).toxenv == 'py'` so it doesn't try to
report coverage for a leg that never ran pytest-cov. This is the direct
answer to "whatever happened to the outputs mechanism Phase B skipped?" —
Phase B deliberately never builds the `commands_post`/`$GITHUB_OUTPUT`
mechanism; this hook is why. Every hook gets the calling job's entire
input set as one JSON blob, not individual named parameters — new inputs
on the core workflow never require touching the hook interface. Real
production hooks (see `reference/reusable-tox-annotated.md`) use this
exact same `fromJSON(...).toxenv == '...'` idiom, just for narrower,
release-automation-specific purposes — worth a look after building this
one, to see how the same mechanism serves a very different use case.

**Also shown at the start of this phase (not built, a facilitator demo):**
a real hook from production (`cheroot`'s `post-src-checkout` or
`awx-plugins`'s `prepare-for-tox-run`) — release-automation-specific,
"here's what production actually looks like," contrasted with the more
general-purpose hook you just built.

Next: `checkout checkpoint/phase-d-caller` for the realistic matrix and
Pattern 5's explicit-env-var block.
