```md
Title: Add scaffold for Finstop (FastAPI backend, parsing, analysis, docker, frontend skeleton)

Description:
This PR adds an initial scaffold for the Finstop financial-analysis application on branch `scaffold-finstop`. It includes:

- FastAPI backend with:
  - JWT-based user auth (starter, in-memory store)
  - File upload endpoint for Excel/PDF
  - Basic parsing logic (pandas, pdfplumber)
  - Simple ratio computations and a lightweight LLM prompt generator
- Docker/Docker Compose configuration for local development
- Minimal frontend skeleton (React) showing file upload + token usage
- requirements.txt listing runtime dependencies
- CI skeleton (.github/workflows/ci.yml), PR template, and CONTRIBUTING.md

Important notes:
- Secrets are placeholders; do not deploy until FINSTOP_SECRET and API keys are replaced and stored securely.
- The in-memory user store is only for a developer preview. Replace with a DB (Postgres) and add migrations (Alembic).
- PDF extraction and statement mapping are heuristic. Add manual mapping UI and improved extraction for production.

Checklist:
- [ ] Replace placeholders for secrets (FINSTOP_SECRET, OPENAI_API_KEY, STRIPE_API_KEY)
- [ ] Add persistent DB + migrations and replace the in-memory user store
- [ ] Add tests (unit + integration) and update CI to run them
- [ ] Implement Stripe checkout + webhooks and gate endpoints by subscription status
- [ ] Integrate LLM with secure API key usage and response caching
- [ ] Harden security (CORS, HTTPS, secrets management, rate limiting)

How to test locally:
1. Checkout branch scaffold-finstop
2. Follow CONTRIBUTING.md to run backend and frontend locally
3. Use the sample API steps in README.md to register, obtain token, and upload sample Excel/PDF

Notes on expected behavior:
- The upload endpoint will parse Excel/PDF files and return parsed content, a set of sample ratios (heuristic), and a short narrative generated from the computed ratios.
- The narrative generator is a lightweight helper and does not call an LLM by default in this scaffold; integrate OpenAI or your preferred LLM in analysis.generate_expert_report for richer output.
```
