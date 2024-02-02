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


## Docker
- `sudo docker-compose -f docker-compose.yml up --force-recreate -d --build`
- Check the docs at `http://localhost:8000/docs`


---

## Answer

> If we are going to deploy this on production, what do you think is the next
improvement that you will prioritize next? This can be a feature, a tech debt, or
an architectural design

Here are some of the improvements this system can target in the roadmap:

- Features:
    - Non-admin login system - allow other employee types to use the system for viewing and/or inquiries regarding a project or benefit.
    - Notification system - notifies the employee and admin for nearing contract end date. (E-mail, SMS, and browser notifications)
    - File upload - allow uploading of files for either media or document attachments like employees' picture and requirements
    - Database backup - since the current database uses SQLite, backing it up is very easy

- Tech debt:
    - Database
        - dedicated database that is not local and file based like SQLite
        - async database driver to further utilize the async nature of the framework (ASGI)
    - Benefit and Project schema
        - Improve the database schema as well as managing it
    - Security checker like SNYK

- Architectural design:
    - Consider cloud infrastracture since the service is small and is fit to be a microservice
    - Use Sentry or Datadog for better application logs and performance monitoring
    - Use CI/CD for hassle-free deployments
