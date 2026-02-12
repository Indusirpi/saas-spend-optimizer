# SaaS Spend Optimizer (Python)

A Python-based spend intelligence tool that analyzes SaaS subscription transactions to:
- Detect recurring subscriptions (monthly/annual cadence + confidence)
- Flag price spikes and vendor-name duplicates
- Identify orphan recurring spend (not in inventory)
- Generate actionable cost-saving recommendations and export reports

## Project Structure
- `backend/` — core analytics engine (ingestion, normalization, detection, recommendations)
- `database/` — schema + sample data
- `tests/` — unit tests (pytest)
- `run_pipeline.py` — CLI runner (exports CSV reports)
- `frontend/` — Streamlit dashboard (web UI)

## Input Data Schema
See `database/schema.md`.

## Quick Start (CLI)
Install dependencies:
```bash
pip install -r requirements.txt
