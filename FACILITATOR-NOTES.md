# Facilitator-only notes (don't share this branch link with participants before the session)

Companion to `../SCHEDULE.md`, `../review/SYNTHESIS.md`, and
`../VERIFIED-SOURCE.md`. This branch is the answer key — same content as
`checkpoint/phase-d-caller`, plus this file.

## Timing cheat-sheet (see SCHEDULE.md for full detail)

- Zero-slack: the 1:22–1:32 break, and the 1:02–1:22 hands-on three-phase
  slot. Trim the break-something-on-purpose demo's own runtime if that
  block is running long — never the break.
- **Also protected, not a cut candidate:** building the coverage-reporting
  hook itself in the 1:40–2:00 hands-on block — that's the core Phase C
  exercise now, not optional practice.
- First cut if running over: Q&A → any of the three share-out moments
  (Pattern 1, hands-on hooks, adapt-to-own-project — additive
  interactivity, not core content) → `steps`-output walkthrough →
  real-production-hook reveal (end of the hands-on hooks block) →
  `post-tox-job` mention → sdist-checkout mention. (Codecov itself isn't a
  cut item — it's not taught as core behavior at all, see `SCHEDULE.md`'s
  Integration-block note. "Comparison with alternatives" isn't scheduled
  at all anymore — it's a one-liner ready only if someone asks.)
- **No pre-recorded fallbacks exist for any demo — every phase runs live,
  the timing risk is knowingly accepted.** See `../CONTINGENCY.md`'s
  "Per-phase live-demo risk" section for the live-only mitigation per
  phase.
- **~20–25 attendees expected, ~10–13 pairs.** No pre-workshop email — a
  QR code to the repo is shown at 0:00, alongside an explicit readiness
  check. Expect some fraction to need help getting a personal GitHub
  account/`tox` installed live — that's accepted, not a surprise; see
  `../CONTINGENCY.md`.

## Mistakes to watch for while circulating (predicted, not observed — this is a first run)

- **`hashFiles() != ''` truthiness is an easy one to get wrong** — it's a
  natural mistake to write `if: hashFiles(...) == 'true'` by analogy with
  boolean checks elsewhere, but it returns a hash string or empty string,
  never a boolean. Watch for this in the Phase C hook exercise.
- **`[testenv:pre-commit]`'s `pass_env = {[testenv]pass_env}` is a small,
  real example of tox's cross-section substitution syntax** — worth a
  10-second aside if anyone reads `tox.ini` closely: it pulls in `[testenv]`'s
  own `pass_env` list (currently empty) and appends `SKIP`, so `SKIP=<hook-id>`
  set by whoever invokes `tox -e pre-commit` reaches the actual `pre-commit`
  process. Confirmed working end-to-end (`SKIP=ruff-format-first-pass tox -e
  pre-commit` correctly skips just that hook).
- **`{posargs}` append confusion is plausible** — passing `tox-run-posargs`
  reads like it should *add to* the `tox.ini` default rather than replace
  it wholesale; it doesn't. Worth a one-line reminder mid-Phase-B.
- **Composite action schema unfamiliarity is likely** — `inputs:`/`runs:
  using: composite`/`steps:` is a new schema for most attendees at the
  stated prerequisite floor (one workflow written). Budget time to
  re-explain the `runs:` block shape at least once per table/pair during
  Phase C.

## Answer to the Pattern 1 "data or hook?" exercise (0:30–0:42)

Simplified from an earlier "classify into 5 input-role categories"
version — that taxonomy didn't teach anything that mattered again later,
so it's gone. Now it's a direct question, 2–3 rapid hypotheticals, asked
before revealing each answer:

1. **"Show test/coverage results as a job summary."** Not an input — it's
   *behavior*, so it's a hook (`post-tox-run`). This is the primary
   example on purpose: it's the exact thing built hands-on in the
   1:40–2:00 block, so this exercise previews real, upcoming work instead
   of an arbitrary example that's never referenced again.
2. **"Pin a specific runner OS image."** An input — pure data
   (`runner-vm-os`), no behavior involved.
3. **"Tag a release commit before building dists."** A hook — real
   example, this is literally what `ansible/awx-plugins`'s
   `prepare-for-tox-run` hook does in production (see
   `reference/reusable-tox-annotated.md`).

The likely trap is treating every new requirement as a new input — not
every one is; the "is this data or behavior?" question is the actual
transferable skill, not memorizing which category a real workflow's 22
inputs happen to fall into. End with a quick show-of-hands share-out
before moving to Pattern 2.

## Design-first framing questions — expected answers (Patterns 2, 3, 5)

Pattern 1 (above) and Pattern 4 already pose a question before revealing
the mechanism. These three round out the other patterns the same way —
posed in `../SCHEDULE.md`'s per-block notes. Below are **plausible answers
to anticipate, not answers observed from a prior run of this workshop** —
this is the first time it's being given; use these to prepare a bridge
line, not as a script to expect verbatim:

- **Pattern 2 (0:42–0:52):** "How would you test 5 Python versions if the
  reusable workflow only takes one?" Plausible answers: "call it in a
  loop," "duplicate the job 5 times," or someone may already know
  `strategy: matrix:`. Whatever comes up, point out it requires *editing
  the reusable workflow* to add iteration — then reveal that native GH
  Actions matrix strategy needs zero changes to it at all, because the
  caller owns the loop. If nothing comes up, offer "duplicate the job" as
  the strawman yourself.
- **Pattern 3 (0:52–1:02):** "How long does it take you to tell
  'environment broke' from 'test failed' in your own CI?" A plausible
  answer is "I have to scroll/read the log" — if so, bridge with:
  `--notest` isn't a nice-to-have verbosity trick, it's a *structural*
  separation — which stage ran tells you the answer before you read a
  single log line.
- **Pattern 5 (2:00–2:10):** "Should a Python 3.15 alpha test failure fail
  your whole CI?" Plausible answers split between "no, alphas are expected
  to be broken sometimes" and "depends, make it configurable." Both are
  defensible, which is exactly the point: the real workflow does *both* —
  auto-forgiveness for prerelease version strings (`~`/`-dev`/`alpha`) as
  the one narrow exception, `xfail` as the required explicit override for
  every other case. If nobody raises "what about a deliberately-broken
  test I know will fail," that's a good follow-up prompt to get to `xfail`
  from the discussion instead of just stating it.

## Coverage-reporting hook: demo at 1:32–1:40, then built hands-on at 1:40–2:00 — don't overclaim

This branch's `.github/reusables/tox-dev/workflow/reusable-tox/hooks/
post-tox-run/action.yml` is the **answer key** for what participants build
themselves in the very next block — `tox exec --skip-pkg-install --quiet
-- coverage report --format=markdown >> "$GITHUB_STEP_SUMMARY"`, gated on
`toxenv == 'py'`. Show it live (demo, not yet build) right as Pattern 4
opens, at 1:32–1:40 — it's the direct answer to "whatever happened to the
outputs demo Phase B skipped?" (Phase B deliberately never built the
`commands_post`/`$GITHUB_OUTPUT` mechanism; this hook is why). Then, at
1:40–2:00, participants build the same thing themselves — this is a
demo-then-practice structure, not two disconnected moments. Presented as
"here's how test/coverage reporting *should* be architected" — a fix for a
real gap, not a description of what any production repo already does.
Keep these three facts separate when talking about it, they're easy to
blur together live:

1. **The critique is about the real upstream `reusable-tox.yml`**, not
   about any caller: it bakes JUnit/Cobertura-summary and Codecov upload
   into unconditional core steps. That's the thing arguably inconsistent
   with Pattern 4.
2. **The real precedent is narrower than our hook**: `ansible/awx-plugins`,
   `ansible/awx_plugins.interfaces`, and `aio-libs/propcache` each have a
   real `post-tox-job` hook (note: different hook point from ours) gated
   on `toxenv == 'pre-commit'` that uploads MyPy coverage to **Coveralls**
   — proof hooks can carry reporting, but narrower (one tool's coverage,
   one external service) than a general pattern. **Coincidence worth
   flagging if it comes up:** this repo's own Phase D caller matrix
   *also* has a `pre-commit` toxenv (Step 4's `needs-jq`→`pre-commit`
   swap) — same name, unrelated reason. Our `pre-commit` leg exists to
   demonstrate a realistic matrix dimension; it has nothing to do with
   this real-world hook's gate. Don't let the room conflate the two.
3. **The one-liner itself is real** (`aio-libs/propcache` uses this exact
   `coverage report --format=markdown` command) **but lives in a
   hand-rolled `test:` job there that doesn't call `reusable-tox.yml` at
   all.** If a participant asks "so does propcache do this via a hook?" —
   the honest answer is no, not yet; this workshop's `post-tox-run` hook is
   a synthesis of a real technique wired into the real extension
   mechanism, not a citation of an existing hook.

**Cut-order note (updated):** this demo now closes the loop Phase B
deliberately left open — it's connective tissue for the curriculum's own
narrative, not a bonus. If short on time, cut the real-production-hook
reveal in Phase C's hands-on block (cheroot/awx-plugins release automation)
*before* cutting this one — see `SCHEDULE.md`'s overflow cut-order.

## Attribution — say it this way on stage

- `--notest` two-phase provisioning: "an idea from tox's own `--notest`
  design" — no issue number (verified `tox#877` is unrelated; see
  `review/REVIEW-FACTCHECK.md`).
- Verbose failure-rerun idiom: "an idiom I've also seen in Ansible's and
  coveragepy's CI" — not a precise citation.
- hashFiles-as-file-exists hook gating: Anthony Sottile,
  `asottile/workflows` — verified exact match, cite with confidence.
- "Novel approach" claim: frame as "my own design, refined across 30+ repos
  I maintain," not an industry-consensus claim.
