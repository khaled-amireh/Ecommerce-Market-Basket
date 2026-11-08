# Contributing

This project preserves an exploratory market-basket analysis. Start with the
[README](README.md), [evidence baseline](docs/EVIDENCE_BASELINE.md), and
[technical audit](docs/CODE_AUDIT.md).

## Documentation contributions

Tie implementation claims to a script line or zero-based notebook cell and
source line. Distinguish input-source metadata, saved historical outputs,
independently reproduced values, illustrative examples, and future proposals.
Do not infer totals from DataFrame labels or fill in clipped product names.

Use relative links for repository files, descriptive image alt text, valid
Markdown tables, and static self-contained SVG assets. Preserve the original
chart and label its actual axes. Check anchors, file paths, and `git diff --check`
before proposing a change. Keep a documentation PR separate from analysis changes.

## Analysis changes need new evidence

Use a dedicated branch and disposable environment for any future code work.
Explain the target population before changing preprocessing, item keys, product
ranking, support thresholds, or the denominator. Record input checksum, package
versions, stage counts, exact parameters, and complete output tables. Compare
with the historical results without overwriting the original evidence silently.
See the [reproduction guide](docs/REPRODUCTION.md).

A syntax repair should demonstrate script/notebook parity. A filtering or
population change needs new mining results. Claims of stable recommendations
need temporal evaluation; claims of incremental business benefit need an
appropriate controlled experiment. No deployment or performance claim should
rest on a high-lift rule alone.

## Scope of the 2026-11-08 documentation work

Only README, new `docs/` files, this guide, and the original banner added under
`images/` were in scope. Existing Python, notebook source/Markdown/outputs,
charts, dependency manifest, and license were protected byte for byte. No data
was acquired, no mining was rerun, and no Git history was rewritten or pushed.
That preservation constraint describes this work, not a permanent ban on
separately reviewed implementation improvements.

Submit focused Conventional Commits, inspect staged changes, and respect the
[MIT license](LICENSE) and separate third-party dataset terms. Publishing is
the repository owner's decision.
