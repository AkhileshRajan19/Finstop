```md
# Contributing & Local run instructions

This file explains how to run the scaffold locally and push changes.

Prereqs:
- Python 3.11
- Node.js (for frontend) — optional for basic testing
- Docker & Docker Compose (optional) — recommended for consistent environment

Local backend run (quick):
1. Clone and checkout the scaffold branch:
   - git clone https://github.com/AkhileshRajan19/Finstop.git
   - cd Finstop
   - git checkout scaffold-finstop

2. Create a virtualenv and install dependencies:
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install --upgrade pip
   - pip install -r backend/requirements.txt

3. Set environment variables (example):
   - export FINSTOP_SECRET="replace-me"
   - export OPENAI_API_KEY="sk-..."
   - export STRIPE_API_KEY="sk_test_..."

4. Run the backend:
   - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   - Visit http://localhost:8000/docs for interactive API docs

Local frontend run (optional):
1. cd frontend
2. npm install
3. npm start
4. The frontend expects backend at http://localhost:8000

Docker compose (optional):
1. Create a .env file with FINSTOP_SECRET, OPENAI_API_KEY, STRIPE_API_KEY
2. docker-compose up --build
3. Backend will be available at http://localhost:8000

How to push the scaffold files (if not already present):
- git add .
- git commit -m "Add scaffold for Finstop"
- git push origin scaffold-finstop

Creating a PR:
- Create a PR from `scaffold-finstop` to `main`.
- Use the PR description in PR_BODY.md as the body.
- Fill the checklist in the PR template and address items before merging.

Security reminder:
- Never commit secrets into the repo.
- Use GitHub Secrets for workflows, and a secrets manager (AWS/GCP/HashiCorp) for deployment.
```
