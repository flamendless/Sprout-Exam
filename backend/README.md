# Sprout Exam API

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) - Fast Python framework
- [Poetry](https://python-poetry.org/) - Python environment manager
- [Python3.11](https://www.python.org/downloads/release/python-3110/) - Python3.11
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
- [SQLite3](https://www.sqlite.org/index.html) - Small database engine
- [Uvicorn](https://www.uvicorn.org/) - ASGI web server for Python

## Setup

- Install Python3.11 (use your system package manager)
- Install [Poetry](https://python-poetry.org/)
- `git clone https://github.com/flamendless/Sprout-Exam`
- `cd Sprout-Exam/backend`
- Install dependencies using `poetry install`
- Activate the shell with `poetry shell`
- Create local `.env` in the project root or use the template `sample.env` with `cp sample.env .env`
- Run server with `poetry run uvicorn src.main:app --reload --port 7777`


## Test
- Install test dependencies with `poetry install --with=test`
- Run `poetry run pytest -v`
