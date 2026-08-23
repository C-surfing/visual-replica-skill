# Contributing

Keep the project a **Skill + Toolkit**. New code should either improve expert workflow quality or provide deterministic evidence. Avoid autonomous code-editing/runtime features.

Before a PR:

```bash
pip install -e '.[dev]'
pytest
ruff check visual_replica tests
```

Changes to scoring/diagnosis should include a synthetic regression test or benchmark case. Optional dependencies must fail transparently rather than fabricating a score.
