# AGENTS.md — Tool Selection (Python)

When you need to call tools from the shell, use this rubric:

## File & Text

- Find files by file name: `fd`
- Find files with path name: `fd -p <file-path>`
- List files in a directory: `fd . <directory>`
- Find files with extension and pattern: `fd -e <extension> <pattern>`
- Find Text: `rg` (ripgrep)
- Find Code Structure: `ast-grep`
  - Common languages:
    - Python → `ast-grep --lang python -p '<pattern>'`
    - TypeScript → `ast-grep --lang ts -p '<pattern>'`
    - Bash → `ast-grep --lang bash -p '<pattern>'`
    - TSX (React) → `ast-grep --lang tsx -p '<pattern>'`
    - JavaScript → `ast-grep --lang js -p '<pattern>'`
    - Rust → `ast-grep --lang rust -p '<pattern>'`
    - JSON → `ast-grep --lang json -p '<pattern>'`
  - Prefer `ast-grep` over ripgrep/grep unless a plain-text search is explicitly requested.
- Select among matches: pipe to `fzf`

## Data

- JSON: `jq`
- YAML/XML: `yq`

## Python Tooling

- Package Management & Virtual Envs: `uv`
  (fast replacement for pip/pip-tools/virtualenv; use `uv pip install ...`, `uv run ...`)
- Linting & Formatting: `ruff`
  (linter + formatter; use `ruff check .`, `ruff format .`)
- Static Typing: `mypy`
  (type checking; use `mypy .`)
- Security: `bandit`
  (Python security linter; use `bandit -r .`)
- Testing: `pytest`
  (test runner; use `pytest -q`, `pytest -k <pattern>` to filter tests)
- Logging: `loguru`
  (runtime logging utility; import in code:

  ```python
  from loguru import logger
  logger.info("message")
  ```)

## Notes

- Prefer uv for Python dependency and environment management instead of pip/venv/poetry/pip-tools.


<file_length_and_structure>

- Prefer maintainability signals over hard caps.
- Split when cognitive complexity > 15, cohesion drops, or fan-in/fan-out spikes.
- If a file nears 400–500 lines, assess for separation by capability or dependency graph.
- Organize with feature-oriented folders and consistent naming.
</file_length_and_structure>

<design_paradigm>

- Support OOP, functional, and data-oriented styles as idiomatic to the language.
- Favor composition and small stable interfaces. Avoid premature abstraction.
- Prefer pure functions and algebraic data types where appropriate (Go/Rust/TS/Python).
</design_paradigm>

<single_responsibility_principle>

- Each module exposes one capability. Close helpers may live with it if cohesion is high.
- Split when a unit owns more than one lifecycle or crosses domain boundaries.
- Enforce SRP via public APIs and package boundaries, not line counts.
</single_responsibility_principle>

<modular_design>

- Modules are interchangeable, testable, and isolated with clear contracts.
- Optimize for replaceability and test seams over speculative reuse.
- Reduce tight coupling. Prefer dependency inversion via interfaces/protocols.
</modular_design>

<roles_and_patterns>

- UI stacks: ViewModel = UI state/logic, Manager = business logic, Coordinator = navigation/flow.
- Non-UI stacks: Service (use cases), Handler (IO endpoints, CLIs), Repository (persistence), Job/Workflow (batch/queues).
- Do not mix view/rendering with business logic.
</roles_and_patterns>

<function_and_class_size>

- Functions: ≤ 20–30 cognitive steps. Split when branching or responsibilities multiply.
- Classes/objects: split when owning >1 lifecycle or >1 external dependency graph.
</function_and_class_size>

<dependency_injection>

- Prefer constructor injection. Keep DI containers optional.
- Use interfaces/protocols in Swift/Kotlin/TS; simple funcs/structs in Go/Rust; protocols/ABCs in Python.
- Stabilize boundaries; avoid over-engineering for small scopes.
</dependency_injection>

<naming_and_readability>

- Names must be descriptive and intention-revealing.
- Allow domain qualifiers with generic terms (e.g., UserData, BillingInfo).
- Forbid empty suffixes like Helper/Util without explicit scope.
</naming_and_readability>

<testing_hooks>

- Provide deterministic seams and small stable interfaces.
- Add contract tests at module boundaries. Snapshot/golden tests for UI/renderers.
- Prefer local duplication over leaky abstractions if it improves testability.
</testing_hooks>

<boundaries_and_dependencies>

- Package by feature. Keep dependency direction: UI → app → domain → infra.
- Enforce with import rules/module maps. Monitor coupling and cyclic deps.
</boundaries_and_dependencies>

<scalability_mindset>

- Code for safe growth: clear contracts, replaceable parts, and observability points.
- Add extension points via interfaces and DI from day one when justified by scope.
</scalability_mindset>

<avoid_god_classes>

- No massive ViewController/ViewModel/Service.
- Split into UI, State, Handlers, Networking, etc., with explicit contracts.
</avoid_god_classes>

---
