# External Source Selection Matrix

| Need | First source | Why | Typical Skill output |
|---|---|---|---|
| Choose among multiple architecture views | SEI Views & Beyond | View selection is usage-driven | `choose_view_by_question` |
| Choose abstraction levels | C4 | Explicit hierarchy of system/container/component/code | `control_abstraction_depth` |
| Organize whole architecture docs | arc42 | Worked documentation structure | `section_selection` |
| Validate formal UML semantics | OMG UML | Normative terminology | `formal_notation_guard` |
| Distinguish structure chart vs flow | Yourdon/Constantine | Historical semantic distinction | `structure_vs_control_flow` |
| Structured sequence/selection/iteration | Nassi–Shneiderman | Explicit structured-control semantics | `structured_flow` |
| Data-centric legacy program modeling | JSP | Data structure → program structure | `data_structure_first` |
| Legacy hierarchy + IPO | HIPO | Historical documentation method | `legacy_hipo_trigger` |
| Render diagrams in Markdown | Mermaid | Text-based, versionable renderer | `renderer_capability` |
| Formal UML-like text rendering | PlantUML | Broad UML coverage | `renderer_fallback` |
| Large directed graph layout | Graphviz | Layered graph layout | `graph_layout_escalation` |
| Shared model → multiple architecture views | Structurizr | Model/view separation | `one_model_multiple_views` |
| C++ entity / source anchors | Clang AST | Semantic AST matching | `semantic_source_extraction` |
| Exact CFG/dataflow reasoning | Clang DataFlow / CodeQL | Analysis-oriented semantics | `analysis_backend_selection` |
| Generated call/dependency graphs | Doxygen | Fast orientation and graph generation | `generated_graph_as_input` |
| Large repository symbol navigation | Sourcegraph | Precise code navigation/indexing | `navigation_backend` |
| Ownership/lifetime reasoning | C++ Core Guidelines | Explicit ownership vocabulary and cautions | `ownership_guardrail` |
| Lock/concurrency reasoning | Linux locking + lockdep | Concrete concurrency constraints | `concurrency_guardrail` |
| Memory ordering | LKMM | Explicit ordering/barrier model | `ordering_guardrail` |
| Real PostgreSQL source navigation | PostgreSQL docs | Project-native example | `project_specific_source_navigation` |
