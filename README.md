# CodeOwl

An AI-powered code analysis and review platform.

## Overview

CodeOwl is a full-stack application that leverages AI to provide intelligent code analysis, reviews, and insights for your repositories.

## Project Structure

This is a monorepo containing:

- **[CodeOwlBE/](CodeOwlBE/)** - Backend API (Python/FastAPI)
- **CodeOwlFE/** - Frontend application (Coming soon)

## Tech Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: LangChain, Google Generative AI, Sentence Transformers
- **Vector Database**: Qdrant
- **Code Analysis**: Tree-sitter (Python)
- **GitHub Integration**: PyGithub
- **Package Manager**: UV

### Frontend
- Coming soon

## Getting Started

### Prerequisites
- Python 3.13+
- UV package manager

### Backend Setup

See the [Backend README](CodeOwlBE/README.md) for detailed setup instructions.

Quick start:
```bash
cd CodeOwlBE
uv sync
uv run python main.py
```

### Frontend Setup
Coming soon

## Development

### Project Layout
```
CodeRabbit-Mine-V3/
├── CodeOwlBE/          # Backend API
│   ├── src/            # Source code
│   ├── tests/          # Tests
│   └── main.py         # Entry point
└── CodeOwlFE/          # Frontend (TBD)
```

## Contributing

1. Clone the repository
2. Install dependencies for the component you're working on
3. Make your changes
4. Run tests
5. Submit a pull request

## License

TBD
