# Bonus (conceptual only — not built live): wheel installs + Codecov

These two pieces of the real `reusable-tox.yml` are real-world plumbing,
not new architectural ideas, so the workshop schedule shows them as slides
rather than live-building them (frees ~10–15 min for the Phase B "aha
moment" instead — see `SCHEDULE.md`).

## Testing a pre-built wheel instead of source

```yaml
built-wheel-names:
  description: >-
    A glob for the built distributions in the artifact to test (is
    installed into tox env if passed)
  required: false
  type: string
```

Used in the provision stage:

```yaml
${{
  inputs.built-wheel-names != ''
  && format('--installpkg dist/{0}', inputs.built-wheel-names)
  || ''
}}
```

The idea: test the *actual artifact* you're about to publish, not a fresh
`pip install -e .` of the source tree — catches packaging bugs a source
install never would.

## Codecov upload

Two calls to `codecov/codecov-action@v7` (verified current at
`VERIFIED-SOURCE.md` §2) — one for coverage, one (`report_type:
test_results`) for JUnit results, both tagged
`CI-GHA,{flags},OS-{os},VM-{runner-vm-os},Py-{python-version}` so a single
Codecov project can distinguish matrix legs. `codecov/codecov-action` is
used for *both* upload kinds instead of the more obvious
`codecov/test-results-action` specifically to dodge an arm64
architecture-detection bug in the latter
(`codecov/test-results-action#121`).

## Why these are cut from the live build, not just shortened

Both require external accounts/tokens (Codecov) or an upstream build step
that doesn't exist in this teaching repo (a real sdist/wheel build job) —
neither teaches a new **pattern**, only a new integration. If your own
project needs either, the production annotated reference
(`reference/reusable-tox-annotated.md`) shows the exact real code.
