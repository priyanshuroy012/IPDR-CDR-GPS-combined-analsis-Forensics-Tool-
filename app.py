import streamlit as st
import os
import pandas as pd
import altair as alt
import json

from utils import (
    normalize_columns, check_required,
    extract_gps_from_android_image,
    convert_for_json, display_forensic_report,
    compute_file_hash, generate_forensic_pdf_report
)

from train_model_dual import (
    train_anomaly_model,
    format_output_table,
    detect_spoofing_and_sim_swap
)

from streamlit_folium import st_folium
from map_utils import create_hybrid_movement_map_with_labels, display_timeline_with_playback

# ✅ Gemini Integration
from gemini_utils import generate_forensic_explanation


# ---------------- UI CONFIG ---------------- #
st.set_page_config(page_title="Android Forensics")

st.markdown("""
    <style>
        .block-container {padding: 2rem;}
        label, .stCheckbox > div {font-size: 16px;}
        h1, h2, h3, h4, h5, h6 {color: #003366;}
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Android Forensics: GPS + IPDR + CDR Analyzer")


# ---------------- SIDEBAR ---------------- #
st.sidebar.header("📂 Upload Forensic Logs")
st.sidebar.markdown("---")

use_logical_image = st.sidebar.checkbox("📁 Extract GPS from logical image folder", value=True)
gps_only = st.sidebar.checkbox("📍 Analyze GPS only", value=True)

# ✅ Gemini toggle
use_gemini = st.sidebar.checkbox("🧠 Enable AI Insights (Gemini)", value=True)

profile = st.sidebar.selectbox("🎯 Detection Profile", ["Conservative", "Balanced", "Aggressive"], index=1)

profile_params = {
    "Conservative": (200, 1800, 800),
    "Balanced": (100, 900, 500),
    "Aggressive": (50, 600, 300)
}

gps_threshold_default, max_gap_default, speed_threshold_default = profile_params[profile]

with st.sidebar.expander("⚙️ Detection Parameters"):
    gps_threshold_km = st.slider("GPS Threshold", 10, 500, gps_threshold_default)
    max_gap_secs = st.slider("Max Gap", 60, 3600, max_gap_default)
    speed_threshold = st.slider("Speed Threshold", 100, 1000, speed_threshold_default)

model_choice = st.sidebar.selectbox("🧠 Model", ["Isolation Forest", "Autoencoder"])
model_type = "autoencoder" if model_choice == "Autoencoder" else "isolation_forest"


# ---------------- DATA LOADING ---------------- #
if use_logical_image:
    folder_path = st.sidebar.text_input("Folder Path", "my_folder")
    gps_df = extract_gps_from_android_image(folder_path) if os.path.exists(folder_path) else pd.DataFrame()
else:
    gps_file = st.sidebar.file_uploader("GPS CSV", type="csv")
    gps_df = pd.read_csv(gps_file) if gps_file else pd.DataFrame()

ipdr_file = st.sidebar.file_uploader("IPDR CSV", type="csv")
cdr_file = st.sidebar.file_uploader("CDR CSV", type="csv")


# ---------------- PROCESSING ---------------- #
if not gps_df.empty:

    raw_ipdr_df = pd.read_csv(ipdr_file) if ipdr_file else pd.DataFrame()
    raw_cdr_df = pd.read_csv(cdr_file) if cdr_file else pd.DataFrame()

    gps_df = normalize_columns(gps_df, "gps")
    ipdr_df = normalize_columns(raw_ipdr_df, "ipdr") if not raw_ipdr_df.empty else raw_ipdr_df
    cdr_df = normalize_columns(raw_cdr_df, "cdr") if not raw_cdr_df.empty else raw_cdr_df

    check_required(gps_df, ["timestamp", "lat", "lon"], "GPS")

    model, scaler, timeline_df, features_df, alerts = train_anomaly_model(
        gps_df, ipdr_df, cdr_df,
        gps_threshold_km=gps_threshold_km,
        max_gap_secs=max_gap_secs,
        speed_threshold=speed_threshold,
        model_type=model_type
    )

    st.success("✅ Analysis Complete")


    # ---------------- SUMMARY ---------------- #
    st.markdown("## 🧠 Investigation Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", len(timeline_df))
    col2.metric("Anomalies", timeline_df['anomaly'].sum())
    col3.metric("GPS Jumps", timeline_df['notes'].str.contains("jump", na=False).sum())


    # ---------------- GEMINI INSIGHTS ---------------- #
    if use_gemini:
        st.markdown("---")
        st.header("🧠 AI Forensic Insights")

        anomalies = timeline_df[timeline_df['anomaly'] == 1].head(3)

        for i, (_, row) in enumerate(anomalies.iterrows()):
            with st.expander(f"Event {i+1} - {row['timestamp']}"):

                anomaly_data = {
                    "timestamp": str(row.get("timestamp")),
                    "ip_address": str(row.get("ip", "N/A")),
                    "gps_location": f"{row.get('lat')}, {row.get('lon')}",
                    "distance": str(row.get("distance_km", "N/A")),
                    "time_gap": str(row.get("time_gap", "N/A")),
                    "device_id": str(row.get("device_id", "N/A"))
                }

                if st.button(f"Explain {i}", key=i):
                    explanation = generate_forensic_explanation(anomaly_data)
                    st.write(explanation)


    # ---------------- TABS ---------------- #
    tab1, tab2, tab3 = st.tabs(["Timeline", "Chart", "Map"])

    with tab1:
        st.dataframe(format_output_table(timeline_df))

    with tab2:
        chart = alt.Chart(timeline_df).mark_bar().encode(
            x='type', y='count()', color='type'
        )
        st.altair_chart(chart, use_container_width=True)

    with tab3:
        map_obj = create_hybrid_movement_map_with_labels(timeline_df)
        st_folium(map_obj)


    # ---------------- REPORT ---------------- #
    st.markdown("---")
    st.header("📄 Report")

    report = {
        "total_events": len(timeline_df),
        "anomalies": int(timeline_df['anomaly'].sum())
    }

    # ✅ Gemini summary in report
    if use_gemini:
        try:
            ai_summary = generate_forensic_explanation({"summary": report})
            st.subheader("🧠 AI Summary")
            st.write(ai_summary)
            report["ai_summary"] = ai_summary
        except:
            report["ai_summary"] = "Unavailable"

    st.download_button(
        "Download JSON",
        json.dumps(report, indent=2),
        file_name="report.json"
    )

    if st.button("Generate PDF"):
        pdf = generate_forensic_pdf_report(report)
        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, "report.pdf")

else:
    st.warning("Upload GPS data to begin")



