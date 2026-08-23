# Toolkit Contract

The toolkit must be deterministic where feasible and honest where it cannot be.

- Missing optional dependency → explicit `available: false` + reason.
- Reference/candidate dimension mismatch → FAIL, never silent resize for final evaluation.
- Core metrics must run without Torch.
- OCR failure must not block compare/report.
- Generated artifacts belong in `.visual-replica/` by default and should not be committed unless desired.
- Comparison commands do not edit application code.
- Diagnosis gives probable code areas; the coding agent decides and performs the patch.
