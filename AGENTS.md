# Repository guidance

- Do not add test cases, test files, test suites, or test fixtures anywhere in this repository.
- Validate changes with syntax checks, import checks, and non-destructive smoke checks without adding tests to the repository.
- Keep Odoo CLI command handlers in `odoo-cli/src/commands/`. Keep shared configuration, services, and terminal presentation in their respective folders.
- Preserve the `run.sh` and `test.sh` entry points and compatibility with existing CLI configuration files.
