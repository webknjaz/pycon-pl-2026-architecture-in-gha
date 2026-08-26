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

## Common mistakes to watch for while circulating

- **Confusing `hashFiles() != ''` truthiness** — participants sometimes
  write `if: hashFiles(...) == 'true'`; it returns a hash string or empty
  string, never a boolean. Watch for this in the Phase C hook exercise.
- **Forgetting `passenv`** in a from-scratch `tox.ini` — the exact bug this
  template's `commands_post` hit during authoring (see `tox.ini`'s comment).
  If someone's `test-result-files` output never appears, this is the first
  thing to check.
- **`{posargs}` append confusion** — participants sometimes expect passing
  `tox-run-posargs` to *add to* the `tox.ini` default rather than replace it
  wholesale. Worth a one-line reminder mid-Phase-B.
- **Composite action schema unfamiliarity** — `inputs:`/`runs: using:
  composite`/`steps:` is a new schema for most attendees at the stated
  prerequisite floor (one workflow written). Expect to re-explain the
  `runs:` block shape at least once per table/pair during Phase C.

## Answer to the Pattern 1 taxonomy exercise (0:28–0:40)

If the hypothetical new input is "install a system package before
checkout" — this is **not** an input at all; it's a hook
(`post-src-checkout`), because it's *behavior*, not *data*. This is
usually the trick participants miss: not every new requirement is a new
input. Use it to segue directly into why Pattern 4 exists.

## Design-first framing questions — expected answers (Patterns 2, 3, 5)

Pattern 1 (above) and Pattern 4 already pose a question before revealing
the mechanism. These three round out the other patterns the same way —
posed in `../SCHEDULE.md`'s per-block notes, expected answers here so
you're not deriving them live:

- **Pattern 2 (0:40–0:50):** "How would you test 5 Python versions if the
  reusable workflow only takes one?" Typical answers: "call it in a loop,"
  "duplicate the job 5 times," occasionally someone already knows
  `strategy: matrix:`. Whatever they propose, point out it requires
  *editing the reusable workflow* to add iteration — then reveal that
  native GH Actions matrix strategy needs zero changes to it at all,
  because the caller owns the loop.
- **Pattern 3 (0:50–1:00):** "How long does it take you to tell
  'environment broke' from 'test failed' in your own CI?" Typical answer:
  "I have to scroll/read the log." Bridge line: `--notest` isn't a
  nice-to-have verbosity trick, it's a *structural* separation — which
  stage ran tells you the answer before you read a single log line.
- **Pattern 5 (1:58–2:08):** "Should a Python 3.15 alpha test failure fail
  your whole CI?" Typical answers split between "no, alphas are expected to
  be broken sometimes" and "depends, make it configurable." Both are
  right, which is exactly the point: the real workflow does *both* —
  auto-forgiveness for prerelease version strings (`~`/`-dev`/`alpha`) as
  the one narrow exception, `xfail` as the required explicit override for
  every other case. If nobody mentions "what about a deliberately-broken
  test I know will fail," that's a good follow-up prompt to get to `xfail`
  from the discussion instead of just stating it.

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
