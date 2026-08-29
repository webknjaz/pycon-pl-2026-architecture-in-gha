# What you missed if you jumped straight here (Phase A)

**The idea, not just the code:** a reusable workflow is deliberately
constrained to one Python version × one OS × one tox environment per call
(Pattern 1 — singular inputs). That constraint is what makes the *caller's*
`strategy: matrix:` block (see `ci-cd.yml`) able to own 100% of the
orchestration decision — the reusable workflow never needs to know how many
combinations exist, only how to run one of them correctly.

Two small things worth noticing even from a fresh checkout:

- The job's `name:` expression is a tiny, self-contained example of GitHub
  Actions ternary-style syntax (`&&`/`||`) and `format()` — useful to
  recognize before the YAML gets denser in later phases.
- `continue-on-error` reads `inputs.xfail` **or** a prerelease-Python guess
  (`~` prefix / `-dev` suffix / `alpha` substring in `python-version`) — this
  is Pattern 5's one deliberate, narrow exception to "no auto-detection,"
  revisited properly in Phase D.

Next: `checkout checkpoint/phase-b-three-stage` to see tox actually get
invoked, in three deliberately separated stages.
