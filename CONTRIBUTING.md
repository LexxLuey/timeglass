# Contributing to TimeGlass

Thank you for your interest in contributing to TimeGlass! We welcome contributions from the community to help make this tool better for everyone.

## Ways to Contribute

- **Report Bugs**: Found a bug? [Open an issue](https://github.com/your-repo/timeglass/issues) with detailed information.
- **Suggest Features**: Have an idea for a new feature? [Create a feature request](https://github.com/your-repo/timeglass/issues).
- **Write Code**: Fix bugs, implement features, or improve documentation.
- **Improve Documentation**: Help make our docs clearer and more comprehensive.
- **Test**: Help us find and fix issues by testing the tool.

## Development Setup

### Prerequisites

- Python 3.10+
- Rust (for the profiling engine)
- Git

### Clone the Repository

```bash
git clone https://github.com/your-repo/timeglass.git
cd timeglass
```

### Set Up Development Environment

1. **Install Poetry (if not already installed):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone and set up the project:**
   ```bash
   git clone https://github.com/your-repo/timeglass.git
   cd timeglass
   poetry install
   ```

3. **Install Rust (if not already installed):**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   ```

4. **Build the Rust extension:**
   ```bash
   cargo build --release
   ```

5. **Run tests:**
   ```bash
   poetry run pytest
   ```

## Code Style

We follow these coding standards:

- **Python**: Follow PEP 8 style guidelines. Use `black` for code formatting and `flake8` for linting.
- **Rust**: Follow the official Rust style guidelines. Use `rustfmt` for formatting and `clippy` for linting.
- **Commits**: Write clear, descriptive commit messages. Use conventional commits format (e.g., `feat: add new feature`, `fix: resolve bug`).

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality. Install them with:

```bash
poetry run pre-commit install
```

## Testing

- Write unit tests for new features and bug fixes.
- Ensure all tests pass before submitting a pull request.
- Aim for good test coverage, especially for critical components.

Run the test suite:

```bash
poetry run pytest
```

For coverage report:

```bash
poetry run pytest --cov=timeglass --cov-report=html
```

## Pull Request Process

1. **Fork the repository** and create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our code style and testing guidelines.

3. **Update documentation** if necessary (README, PRD, etc.).

4. **Run tests** and ensure everything passes.

5. **Commit your changes** with clear messages.

6. **Push to your fork** and [create a pull request](https://github.com/your-repo/timeglass/pulls).

7. **Wait for review**. We may ask for changes or clarifications.

8. **Merge** once approved!

### Pull Request Guidelines

- Provide a clear description of what your PR does.
- Reference any related issues.
- Keep PRs focused on a single feature or fix.
- Ensure CI checks pass.

## Documentation

- Update README.md for user-facing changes.
- Update PRD.md for significant feature additions.
- Add docstrings to new functions and classes.
- Keep documentation up-to-date with code changes.

## Issue Reporting

When reporting bugs or requesting features:

- Use a clear, descriptive title.
- Provide steps to reproduce (for bugs).
- Include relevant code snippets, error messages, or screenshots.
- Specify your environment (OS, Python version, etc.).

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and constructive in discussions.
- Help newcomers learn and contribute.
- Focus on the merit of ideas, not personal opinions.
- Report any unacceptable behavior to the maintainers.

## Getting Help

- Check existing [issues](https://github.com/your-repo/timeglass/issues) and [discussions](https://github.com/your-repo/timeglass/discussions).
- Join our community chat (if available).
- Contact the maintainers directly.

Thank you for contributing to TimeGlass! Your efforts help make FastAPI development more efficient and enjoyable for everyone. 🚀
