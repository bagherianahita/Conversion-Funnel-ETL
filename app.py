"""Streamlit demo — conversion funnel ETL and download trends."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from etl import build_download_trends, plot_rolling_trends, sample_events

DEFAULT_PORT = 8508
OUTPUT_DIR = Path("output")

st.set_page_config(page_title="Conversion Funnel ETL", page_icon="📈", layout="wide")
st.title("Conversion Funnel ETL")
st.caption("Session-level event ETL with rolling-average download trends — synthetic demo data.")

if st.button("Run ETL pipeline", type="primary"):
    with st.spinner("Processing events…"):
        events = sample_events()
        agg = build_download_trends(events)
        OUTPUT_DIR.mkdir(exist_ok=True)
        chart_path = OUTPUT_DIR / "download_trends.png"
        plot_rolling_trends(agg, save_path=str(chart_path))
        st.session_state.agg = agg
        st.session_state.chart_path = chart_path

if "agg" in st.session_state:
    st.subheader("Aggregated download trends")
    st.dataframe(st.session_state.agg, use_container_width=True, hide_index=True)
    if st.session_state.chart_path.exists():
        st.subheader("7-day rolling average chart")
        st.image(str(st.session_state.chart_path), use_container_width=True)
else:
    st.info("Click **Run ETL pipeline** to generate the session dataset and chart.")

st.divider()
st.markdown(f"**Run locally:** `streamlit run app.py` → http://localhost:{DEFAULT_PORT}")
