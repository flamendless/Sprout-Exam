# SproutExam Client

This template should help get you started developing with Vue 3 in Vite.

## Setup

- Install [Bun](https://bun.sh/)
- Install [Poetry](https://python-poetry.org/)
- `git clone https://github.com/flamendless/Sprout-Exam`
- `cd Sprout-Exam/frontend`
- Install dependencies using `bun install`
- Create local `.env` in the project root or use the template `sample.env` with `cp sample.env .env`
- Run server with `bun run dev`


## Docker
- `sudo docker build -t sproutexamclient/vue .`
- `sudo docker-compose up -d`
- Check the client at `http://localhost:8080/`


---

## Answer

> If we are going to deploy this on production, what do you think is the next
improvement that you will prioritize next? This can be a feature, a tech debt, or
an architectural design

Here are some of the improvements this system can target in the roadmap:

- Features:
    - Projects view - for admin and contractual type employees
    - Benefits view - for admin and regular type employees
    - Audit logs view - for admin type employees (the backend already supports this)
    - Use modals and other HTML features for better UI/UX

- Tech debt:
    - Improve routes/endpoints
    - Improve forms
    - Improve validation of user inputs

- Architectural design:
    - Consider SSR (server side rendering) instead of SPA (single page application) since the client can be big
    - Use Sentry or Datadog for better application logs and performance monitoring
    - Use CI/CD for hassle-free deployments
