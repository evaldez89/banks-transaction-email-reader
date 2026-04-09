# AGENTS

This repository is designed for modular, testable development of bank transaction email extraction.

## Scope and Architecture

- Keep domain contracts in `domain/` and avoid infrastructure dependencies there.
- Keep provider implementations in `mail_services/`.
- Keep parser registry and provider registry in `infrastructure/`.
- Keep orchestration in `main.py` and avoid embedding parser/provider internals in the CLI.

## Coding Rules

- Use Python 3.12+ typing syntax (built-in generics and modern type aliases).
- Keep comments and documentation in English.
- Prefer explicit registration over implicit discovery for extensibility.
- Add small, focused functions and classes with clear responsibilities.

## Testing Expectations

- Add or update tests for every behavior change.
- Prefer parser unit tests with HTML fixtures.
- Use mocks for integration-style tests that touch external services.
- Ensure `pytest` passes before opening a pull request.

## Contribution Flow

1. Create focused commits with clear, imperative messages.
2. Keep breaking changes explicit in commit messages and PR description.
3. Update documentation when behavior or architecture changes.
4. Open a PR with a concise summary and testing notes.
