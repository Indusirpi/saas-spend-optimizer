import streamlit as st
import pandas as pd
import tempfile
from backend.pipeline import run_pipeline

st.set_page_config(page_title="SaaS Spend Optimizer", layout="wide")

st.title("💳 SaaS Spend Optimizer")
st.caption("AI-powered recurring detection, anomaly analysis, and cost optimization insights.")

# Sidebar
with st.sidebar:
    st.header("Upload Data")
    txn_file = st.file_uploader("Transactions CSV", type=["csv"])
    inv_file = st.file_uploader("Inventory CSV (optional)", type=["csv"])

if not txn_file:
    st.info("Upload a Transactions CSV to begin.")
    st.stop()

# Save uploads temporarily
with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as f:
    f.write(txn_file.getbuffer())
    txn_path = f.name

inv_path = None
if inv_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as f:
        f.write(inv_file.getbuffer())
        inv_path = f.name

# Run pipeline
results = run_pipeline(txn_path, inv_path)

summary = results["summary"]
recurring = results["recurring"]
spikes = results["spikes"]
duplicates = results["duplicates"]
recs = results["recommendations"]

# ================= KPIs =================
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Run Rate (Est.)",
    f"${summary.loc[0, 'monthly_run_rate_est']:,.2f}"
)

col2.metric(
    "Recurring Vendors",
    int(summary.loc[0, "recurring_vendors"])
)

col3.metric(
    "Price Spikes",
    int(summary.loc[0, "price_spikes"])
)

col4.metric(
    "Estimated Savings",
    f"${summary.loc[0, 'estimated_monthly_savings']:,.2f}"
)

st.divider()

# ================= Tabs =================
tabs = st.tabs(["Recurring", "Anomalies", "Recommendations"])

# --- Recurring ---
with tabs[0]:
    st.subheader("Detected Recurring Subscriptions")
    st.dataframe(recurring, use_container_width=True)

    if not recurring.empty:
        st.subheader("Top Vendors by Estimated Monthly Cost")
        chart_data = recurring.sort_values(
            "run_rate_monthly_est", ascending=False
        ).set_index("vendor_norm")["run_rate_monthly_est"]

        st.bar_chart(chart_data)

# --- Anomalies ---
with tabs[1]:
    st.subheader("Price Spikes")
    if spikes.empty:
        st.success("No price spikes detected.")
    else:
        st.dataframe(spikes, use_container_width=True)

    st.subheader("Duplicate Vendor Names")
    if duplicates.empty:
        st.success("No duplicate vendor names detected.")
    else:
        st.dataframe(duplicates, use_container_width=True)

# --- Recommendations ---
with tabs[2]:
    st.subheader("Actionable Recommendations")

    if recs.empty:
        st.info("No optimization recommendations generated.")
    else:
        st.dataframe(recs, use_container_width=True)

        st.download_button(
            "Download recommendations.csv",
            data=recs.to_csv(index=False).encode("utf-8"),
            file_name="recommendations.csv",
            mime="text/csv"
        )
