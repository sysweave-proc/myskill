# Source Code Reading Skill v0.1–v0.5 Evolution Audit

## Conclusion

- v0.1 → v0.2: normal additive evolution.
- v0.2 → v0.3: normal additive evolution.
- v0.3 → v0.4: mostly additive, but `references/tracing/exploration-policy.md` was lost and is a material process regression; `knowledge-sources/README.md` was also lost as documentation.
- v0.4 → v0.5: regression. The package fell from 35 files to 12 and dropped established reusable assets including `knowledge-sources/`, `evolution/`, `cases/`, `references/diagrams/`, detailed tracing/validation/document policies, templates and examples. Some concepts were restated in a shorter `SKILL.md`, but the rule assets themselves disappeared.

## v0.5.1 repair

v0.5.1 is built from the complete v0.4 baseline, then adds:

- progressive gates: Scope → Orient → Minimum Model → Pattern → Trace → Represent → Validate;
- L0–L3 progressive depth policy;
- Core Skill vs capability-extension boundary;
- merge-based/non-regression evolution policy;
- baseline capability inventory and SHA-256 file manifest;
- integrity regression test;
- restoration of the general exploration policy and knowledge-sources README.

## Hard invariant going forward

A new Skill version is a merge, not a clean-room rewrite. Existing files/capabilities are preserved by default. Any removal requires an explicit rationale and regression evidence.
