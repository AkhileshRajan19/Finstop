# Finstop - Financial Analysis Platform (Starter)

This repository contains a starter scaffold for a subscription-based financial analysis app.

Features:
- User authentication (JWT)
- File upload (Excel / PDF) to extract financial statements
- Financial analysis module computing standard ratios (liquidity, profitability, leverage, efficiency, market)
- LLM-backed expert-style narrative reports
- Stripe checkout skeleton for subscriptions
- Docker-ready backend

Notes:
- PDF table extraction uses pdfplumber and optionally camelot (system deps required for camelot).
- LLM integration uses the OpenAI API (API key required).
- For production, refine parsing, data validation, rate limiting, logging, and security (HTTPS, CSP, secrets management).