```md
## Summary

<!-- Briefly describe what this PR does. -->

## What I changed
- Added scaffold for Finstop: backend (FastAPI), parsing & analysis modules, Docker files, and a minimal frontend skeleton.
- Files are on branch `scaffold-finstop`.

## Checklist before merge
- [ ] Replace placeholder secrets (FINSTOP_SECRET, OPENAI_API_KEY, STRIPE_API_KEY) in environment settings before deploying.
- [ ] Replace in-memory user store with persistent DB (e.g., Postgres) and add migrations.
- [ ] Add tests (unit/integration) and update CI to run them.
- [ ] Add Stripe webhooks & subscription gating, verify with test cards.
- [ ] Add LLM API keys and secure secrets in your chosen secrets manager.
- [ ] Review and harden CORS and other security settings.

## Additional notes
- See CONTRIBUTING.md for local setup and how to run the backend and frontend locally.
- CI currently runs a lightweight install + compile step. Update CI to run tests once present.
```
