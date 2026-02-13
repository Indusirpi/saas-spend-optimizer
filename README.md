# SaaS Spend Optimizer (Python)

A Python-based spend intelligence tool that analyzes SaaS subscription transactions to:
- Detect recurring subscriptions (monthly/annual cadence + confidence)
- Flag price spikes and vendor-name duplicates
- Identify orphan recurring spend (not in inventory)
- Generate actionable cost-saving recommendations and export reports

## Problem Statement

- Growing startups and enterprises often lose visibility into SaaS spending due to:
- Fragmented transaction data
- Duplicate vendor names (e.g., "Zoom" vs "Zoom Video Communications")
- Hidden recurring subscriptions
- Price increases over time
- Orphan subscriptions missing from internal inventory
- This project builds a data-driven spend intelligence engine to solve that.

## Project Structure
- `backend/` — core analytics engine (ingestion, normalization, detection, recommendations)
- `database/` — schema + sample data
- `tests/` — unit tests (pytest)
- `run_pipeline.py` — CLI runner (exports CSV reports)
- `frontend/` — Streamlit dashboard (web UI)
  
## 🛠 Tech Stack

- Python 3.10+
- Pandas (data processing)
- NumPy
- Scikit-learn (Isolation Forest)
- Streamlit (dashboard)
- Pytest (unit testing)
  
## System Flow

![Flowchart](https://github.com/Indusirpi/Docs/blob/main/Real%20Payment%20Decision%20Flow-2026-02-13-010311.png)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run frontend/app.py
```

## Run Pipeline via CLI

```bash
python run_pipeline.py \
  --transactions database/sample_data/transactions.csv \
  --inventory database/sample_data/inventory.csv \
  --outdir outputs
```
## Why This Project Matters

- This project demonstrates:
- Data engineering fundamentals
- Feature engineering for financial signals
- Applied ML anomaly detection
- Modular pipeline design
- Clean separation of backend and UI
- Production-style deployment (Streamlit Cloud)
- Test-driven development
  
## Dashboard Preview
<p>
  <img src="https://github.com/Indusirpi/Docs/blob/main/fa1ecfa3-1.png" width="500"/>
<img src="https://github.com/Indusirpi/Docs/blob/main/c1061b42-1.png" width="500"/>
</p>

## 🌐 Live Demo

https://saas-spend-optimizer.streamlit.app/




