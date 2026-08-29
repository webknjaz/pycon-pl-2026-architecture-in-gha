# What you missed if you jumped straight here (Phase D)

**The idea, not just the code:** this is the final teaching-version state.
Two things landed in this phase:

1. **Pattern 5, Exhibit B** — the workflow-level `env:` block (color +
   encoding vars) and `TOX_TESTENV_PASSENV`. `TOX_TESTENV_PASSENV` widens
   every testenv's passenv list from *outside* `tox.ini` entirely — real
   projects rely on this instead of hand-maintaining a `passenv`/`pass_env`
   line per project. (`tox.ini`'s own `[testenv:pre-commit]` still has a
   small local `pass_env` for `SKIP` — a different, narrower need, unrelated
   to color output.) Explicitness has a cost: thirteen tools, thirteen
   different color env vars, one workflow forced to know all of them.
2. **A realistic caller matrix** (3 Python versions × 2 tox envs = 6 legs)
   in `ci-cd.yml` — the reusable workflow's own code did not change at all
   to support going from 2 legs (Phase A) to 6. That's the payoff of
   Pattern 1 + Pattern 2 together.
3. **A `check:` job using `re-actors/alls-green`** — the matrix's own
   capstone. Branch protection's required-checks list breaks every time a
   matrix's shape changes; naively listing every job in `check`'s `needs:`
   has a subtle bug too (on failure, `check` becomes `skipped`, not
   `failed`, without real aggregation logic). `alls-green` fixes both:
   `needs: [tests]`, `if: always()`, and `needs.tests.result` already
   aggregates correctly across all 6 matrix legs — no per-leg handling
   needed. Referenced via `@release/v1`, a real stable channel, unlike
   `tox-dev/workflow`'s own "unstable/experimental" self-description.

`reference/reusable-tox-annotated.md` has the full real 22-input production
version if you want to see what's cut here. Wheel installs and
sdist-checkout are left conceptual-only (real-world plumbing, not core
architecture — see `reference/bonus-wheel-and-codecov.md`). Codecov is cut
for a different reason entirely: it's deliberately not taught as core
behavior at all — see `reference/coverage-reporting-hook.md` for why, and
the hook shown at the start of Phase C for the alternative.

This is the end of the guided build. From here: adapt this template to your
own project, or explore the full annotated reference.
