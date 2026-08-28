# Facilitator-only notes (don't share this branch link with participants before the session)

Companion to `../SCHEDULE.md`, `../review/SYNTHESIS.md`, and
`../VERIFIED-SOURCE.md`. This branch is the answer key — same content as
`checkpoint/phase-d-caller`, plus this file.

## Timing cheat-sheet (see SCHEDULE.md for full detail)

- Zero-slack: the 1:20–1:30 break, and the Phase-B aha-moment slot
  (1:00–1:20). Trim the break-something-on-purpose demo's own runtime if
  Phase B is running long — never the break.
- First cut if running over: Q&A → alternatives discussion → Codecov/steps
  walkthrough → post-tox-job mention → sdist-checkout mention.
- Every CI-dependent demo has a pre-recorded fallback. Default to showing
  it; treat any live run as a background bonus, never something the room
  waits on.

## Mistakes to watch for while circulating (predicted, not observed — this is a first run)

- **`hashFiles() != ''` truthiness is an easy one to get wrong** — it's a
  natural mistake to write `if: hashFiles(...) == 'true'` by analogy with
  boolean checks elsewhere, but it returns a hash string or empty string,
  never a boolean. Watch for this in the Phase C hook exercise.
- **Forgetting `passenv`** in a from-scratch `tox.ini` — the exact bug this
  template's `commands_post` hit during authoring (see `tox.ini`'s comment).
  If someone's `test-result-files` output never appears, this is the first
  thing to check.
- **`{posargs}` append confusion is plausible** — passing `tox-run-posargs`
  reads like it should *add to* the `tox.ini` default rather than replace
  it wholesale; it doesn't. Worth a one-line reminder mid-Phase-B.
- **Composite action schema unfamiliarity is likely** — `inputs:`/`runs:
  using: composite`/`steps:` is a new schema for most attendees at the
  stated prerequisite floor (one workflow written). Budget time to
  re-explain the `runs:` block shape at least once per table/pair during
  Phase C.

## Answer to the Pattern 1 taxonomy exercise (0:28–0:40)

If the hypothetical new input is "install a system package before
checkout" — this is **not** an input at all; it's a hook
(`post-src-checkout`), because it's *behavior*, not *data*. The likely
trap here is treating every new requirement as a new input — not every
one is. Use it to segue directly into why Pattern 4 exists.

## Design-first framing questions — expected answers (Patterns 2, 3, 5)

Pattern 1 (above) and Pattern 4 already pose a question before revealing
the mechanism. These three round out the other patterns the same way —
posed in `../SCHEDULE.md`'s per-block notes. Below are **plausible answers
to anticipate, not answers observed from a prior run of this workshop** —
this is the first time it's being given; use these to prepare a bridge
line, not as a script to expect verbatim:

- **Pattern 2 (0:40–0:50):** "How would you test 5 Python versions if the
  reusable workflow only takes one?" Plausible answers: "call it in a
  loop," "duplicate the job 5 times," or someone may already know
  `strategy: matrix:`. Whatever comes up, point out it requires *editing
  the reusable workflow* to add iteration — then reveal that native GH
  Actions matrix strategy needs zero changes to it at all, because the
  caller owns the loop. If nothing comes up, offer "duplicate the job" as
  the strawman yourself.
- **Pattern 3 (0:50–1:00):** "How long does it take you to tell
  'environment broke' from 'test failed' in your own CI?" A plausible
  answer is "I have to scroll/read the log" — if so, bridge with:
  `--notest` isn't a nice-to-have verbosity trick, it's a *structural*
  separation — which stage ran tells you the answer before you read a
  single log line.
- **Pattern 5 (1:58–2:08):** "Should a Python 3.15 alpha test failure fail
  your whole CI?" Plausible answers split between "no, alphas are expected
  to be broken sometimes" and "depends, make it configurable." Both are
  defensible, which is exactly the point: the real workflow does *both* —
  auto-forgiveness for prerelease version strings (`~`/`-dev`/`alpha`) as
  the one narrow exception, `xfail` as the required explicit override for
  every other case. If nobody raises "what about a deliberately-broken
  test I know will fail," that's a good follow-up prompt to get to `xfail`
  from the discussion instead of just stating it.

## Coverage-reporting hook reveal (1:38–1:58, second reveal) — don't overclaim

This branch's `.github/reusables/tox-dev/workflow/reusable-tox/hooks/
post-tox-run/action.yml` is a real, tested hook
(`tox exec --skip-pkg-install --quiet -- coverage report --format=markdown
>> "$GITHUB_STEP_SUMMARY"`) presented as "here's how test/coverage
reporting *should* be architected" — a fix for a real gap, not a
description of what any production repo already does. Keep these three
facts separate when talking about it, they're easy to blur together live:

1. **The critique is about the real upstream `reusable-tox.yml`**, not
   about any caller: it bakes JUnit/Cobertura-summary and Codecov upload
   into unconditional core steps. That's the thing arguably inconsistent
   with Pattern 4.
2. **The real precedent is narrower than our hook**: `ansible/awx-plugins`,
   `ansible/awx_plugins.interfaces`, and `aio-libs/propcache` each have a
   real `post-tox-job` hook (note: different hook point from ours) gated
   on `toxenv == 'pre-commit'` that uploads MyPy coverage to **Coveralls**
   — proof hooks can carry reporting, but narrower (one tool's coverage,
   one external service) than a general pattern.
3. **The one-liner itself is real** (`aio-libs/propcache` uses this exact
   `coverage report --format=markdown` command) **but lives in a
   hand-rolled `test:` job there that doesn't call `reusable-tox.yml` at
   all.** If a participant asks "so does propcache do this via a hook?" —
   the honest answer is no, not yet; this workshop's `post-tox-run` hook is
   a synthesis of a real technique wired into the real extension
   mechanism, not a citation of an existing hook.

If short on time, cut this reveal before cutting the real-production-hook
reveal (cheroot/awx-plugins release automation) — see `SCHEDULE.md`'s
overflow cut-order.

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
