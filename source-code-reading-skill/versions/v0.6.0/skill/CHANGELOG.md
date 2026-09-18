# Changelog

## 0.6.0 — Cognitive + Engineering Merge Release

### Added
- five-dimension knowledge model: Structure / Behavior / Constraint / Evidence / Evolution;
- canonical Cognitive Spine;
- Situated Knowledge: version, build context, performance, decision, learning path, conflict, change impact;
- consolidated fast-entry reference pages for architecture, patterns, representation, traceability, and validation;
- merge decision record documenting source selection, conflict resolution, and non-regression checks;
- semantic merged-capability test.

### Preserved
- full v0.5.1 architecture, graph, path/topic/source, tracing, validation, document, knowledge-source, cases, evolution, template, example, and test assets;
- complete diagram catalog;
- merge-based/non-regression evolution policy.

### Strengthened
- six-stage × seven-gate execution spine;
- L0–L3 progressive depth;
- dominant-pattern selection;
- relation-semantics fallback;
- Claim → Evidence → Source Anchor discipline;
- FACT / INFERENCE / INTERPRETATION distinction;
- case → rule → regression evolution loop.

### Fixed (post-freeze patch)
- `SKILL.md` frontmatter: the folded block scalar `>-` was replaced by the literal block
  scalar `|-`. The official validator extracts the description with `description:\s*(.+)`,
  whose `\s*` cannot cross the `>` of `>-`, so it captured the literal string `>-` and
  rejected every release with `Description cannot contain angle brackets (< or >)`.
  This was a validator-facing defect, not a description-text problem: the description prose
  never contained angle brackets. No description text was changed. Verified with
  `skill-creator/scripts/quick_validate.py` → `Skill is valid!`.
- `tests/test_skill_integrity.py`: added existence and non-empty guards for the baseline and
  candidate directories. Previously a mistyped or missing baseline path made every
  preservation check vacuously true and printed
  `PASS: preserved 0 baseline files; changed 0 approved baseline files; added 59 files` —
  a false pass at exactly the moment the guard matters most. Invalid input now exits 2.

> Note: this patch was applied after the v0.6.0 freeze. `skill/` therefore no longer matches
> `source.zip` byte for byte; see `versions/v0.6.0/README.md` 备注.
