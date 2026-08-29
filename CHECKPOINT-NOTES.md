# What you missed if you jumped straight here (Phase B)

**The idea, not just the code:** the reusable workflow now runs tox in
three deliberately separate stages: provision (`--notest`), the real run
(`id: tox-run`), and a conditional debug rerun on failure. This separation
means "the environment failed to build" and "a test failed" are never
ambiguous in the logs — you know which one happened before you even read a
line of pytest output.

The debug-rerun step ends with `&& exit 1` on purpose — even if the verbose
rerun happens to pass, the job stays red. A test that fails once and passes
on retry is *flaky*, not *fine*.

**Notice what's absent:** nothing in this workflow or `tox.ini` renders a
coverage/test summary anywhere. That's deliberate — the real upstream
`reusable-tox.yml` bakes this into unconditional core steps (see
`reference/reusable-tox-annotated.md`), which is arguably inconsistent
with the extension-point philosophy the whole design is built around. The
fix is a hook, not `tox.ini` plumbing — see
`reference/coverage-reporting-hook.md` and the demo at the start of
Phase C.

Next: `checkout checkpoint/phase-c-hooks` to see extension points added
around these three stages.
