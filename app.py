"""
Indian Railways Train Delay Prediction & Network Punctuality Analytics
========================================================================
Interactive Dispatch Decision Support System & Machine Learning Lab.
Engineered for Live Demonstrations, Model Audits & Streamlit Cloud Deployment.
Modern human-crafted UI with bespoke CSS curves, rounded borders & responsive cards.
"""

import os
import io
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Project preprocessing helper functions
from utils import clean_data_pandas, engineer_features_pandas, handle_outliers_iqr_numpy

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & BESPOKE MODERN UI STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Indian Railways Delay Predictor & ML Lab",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bespoke, Modern CSS with Rounded Curves, Subtle Shadows & Enterprise Polish
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 95%;
    }

    /* Modern Rounded App Header */
    .ir-hero-header {
        background: linear-gradient(135deg, #0b2545 0%, #133a68 50%, #1e4976 100%);
        color: #ffffff;
        padding: 1.6rem 2rem;
        border-radius: 18px;
        box-shadow: 0 10px 25px -5px rgba(11, 37, 69, 0.25), 0 8px 10px -6px rgba(11, 37, 69, 0.15);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .ir-hero-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(180deg, #ff9933 0%, #ffffff 50%, #138808 100%); /* Tricolor accent */
    }
    .ir-hero-header h1 {
        color: #ffffff !important;
        margin: 0 0 0.4rem 0;
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    .ir-hero-header p {
        color: #cbd5e1;
        margin: 0;
        font-size: 0.95rem;
        font-weight: 400;
        max-width: 850px;
        line-height: 1.45;
    }

    /* Modern Card Containers with Soft Curves */
    .modern-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.35rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.15rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .modern-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.07), 0 4px 6px -4px rgba(0, 0, 0, 0.03);
    }

    /* Preset Interactive Cards */
    .preset-card-box {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.15rem;
        min-height: 155px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
    }
    .preset-card-box:hover {
        border-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.12);
    }
    .preset-card-box.active {
        border-color: #2563eb;
        background: #eff6ff;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }

    /* Pill Badges with Smooth Curved Borders */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .pill-green {
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .pill-amber {
        background: #fef3c7;
        color: #b45309;
        border: 1px solid #fde68a;
    }
    .pill-red {
        background: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }

    /* Dispatch Hero Banner */
    .dispatch-banner {
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 1.25rem 0;
        border: 1px solid transparent;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .dispatch-green {
        background: #f0fdf4;
        border-color: #bbf7d0;
        color: #14532d;
    }
    .dispatch-amber {
        background: #fffbeb;
        border-color: #fde68a;
        color: #78350f;
    }
    .dispatch-red {
        background: #fef2f2;
        border-color: #fecaca;
        color: #7f1d1d;
    }

    /* Mathematical Formula Card */
    .formula-pill-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        transition: border-color 0.2s ease;
    }
    .formula-pill-box:hover {
        border-color: #cbd5e1;
    }

    /* Segmented Navigation Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.9rem;
        color: #64748b;
        border: none !important;
        background-color: transparent;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
    }

    /* Curved Input Widgets */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #cbd5e1 !important;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }

    /* Curved Streamlit Buttons */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        padding: 0.6rem 1.4rem;
        border: 1.5px solid #cbd5e1;
        transition: all 0.15s ease;
    }
    div.stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
    }

    /* Expander with Curved Borders */
    div[data-testid="stExpander"] {
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        margin-bottom: 0.85rem;
    }

    /* Sidebar Custom Cards */
    .sidebar-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.85rem;
    }

    /* Code & Monospace Elements */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 6px;
        padding: 0.15rem 0.4rem;
        background-color: #f1f5f9;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MODEL PIPELINE LOADER (CACHED, FAST SUB-15MS INFERENCE)
# -----------------------------------------------------------------------------
ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "pandas_numpy_pipeline.joblib")

@st.cache_resource(show_spinner="Loading trained LightGBM model and preprocessing parameters...")
def get_model_pipeline():
    path = ARTIFACT_PATH
    if not os.path.exists(path):
        alt = os.path.join("artifacts", "pandas_numpy_pipeline.joblib")
        if os.path.exists(alt):
            path = alt
        else:
            raise FileNotFoundError(f"Pipeline artifact missing at {path}")
    return joblib.load(path)

try:
    pipeline = get_model_pipeline()
    model = pipeline["model"]
    train_mean = pipeline["train_mean"]
    train_std = pipeline["train_std"]
    feature_columns = pipeline["feature_columns"]
    cat_cols = pipeline["cat_cols"]
    num_cols = pipeline["num_cols"]
    iqr_bounds = pipeline.get("iqr_bounds", {})
    pipeline_ready = True
except Exception as err:
    pipeline_ready = False
    pipeline_err_msg = str(err)

# -----------------------------------------------------------------------------
# 3. DOMAIN METADATA & 16 IR ZONES DATABASE
# -----------------------------------------------------------------------------
ZONE_DATABASE = {
    "Northern Railway (NR)": {"abbr": "NR", "congestion": 0.92, "fog": 0.88, "hq": "New Delhi", "desc": "High winter fog corridor, trunk line bottlenecks"},
    "North Central Railway (NCR)": {"abbr": "NCR", "congestion": 0.90, "fog": 0.82, "hq": "Prayagraj", "desc": "Dense Kanpur-Prayagraj HDN trunk corridor"},
    "Eastern Railway (ER)": {"abbr": "ER", "congestion": 0.95, "fog": 0.32, "hq": "Kolkata", "desc": "Highest congestion (95%), heavy suburban & coal traffic"},
    "Central Railway (CR)": {"abbr": "CR", "congestion": 0.85, "fog": 0.05, "hq": "Mumbai CST", "desc": "High frequency suburban & ghat operations"},
    "Western Railway (WR)": {"abbr": "WR", "congestion": 0.83, "fog": 0.05, "hq": "Mumbai Central", "desc": "Major Mumbai-Delhi Western corridor"},
    "East Central Railway (ECR)": {"abbr": "ECR", "congestion": 0.88, "fog": 0.55, "hq": "Hajipur", "desc": "Dense passenger & coal transport in Bihar/Jharkhand"},
    "North Eastern Railway (NER)": {"abbr": "NER", "congestion": 0.82, "fog": 0.78, "hq": "Gorakhpur", "desc": "Indo-Gangetic winter fog sensitivity"},
    "West Central Railway (WCR)": {"abbr": "WCR", "congestion": 0.80, "fog": 0.42, "hq": "Jabalpur", "desc": "Itarsi junction central intersection"},
    "North Western Railway (NWR)": {"abbr": "NWR", "congestion": 0.75, "fog": 0.58, "hq": "Jaipur", "desc": "Desert temperature swings & winter fog"},
    "South Eastern Railway (SER)": {"abbr": "SER", "congestion": 0.74, "fog": 0.22, "hq": "Kolkata", "desc": "Heavy mineral and industrial freight"},
    "South Central Railway (SCR)": {"abbr": "SCR", "congestion": 0.72, "fog": 0.04, "hq": "Secunderabad", "desc": "Key North-South transit corridors"},
    "East Coast Railway (ECoR)": {"abbr": "ECoR", "congestion": 0.70, "fog": 0.18, "hq": "Bhubaneswar", "desc": "High freight loading coastal network"},
    "South East Central Railway (SECR)": {"abbr": "SECR", "congestion": 0.68, "fog": 0.28, "hq": "Bilaspur", "desc": "Highest coal loading per route km"},
    "Southern Railway (SR)": {"abbr": "SR", "congestion": 0.65, "fog": 0.02, "hq": "Chennai Central", "desc": "Minimal fog exposure, high on-time history"},
    "South Western Railway (SWR)": {"abbr": "SWR", "congestion": 0.60, "fog": 0.02, "hq": "Hubballi", "desc": "Moderate congestion, good punctuality track"},
    "Northeast Frontier Railway (NFR)": {"abbr": "NFR", "congestion": 0.58, "fog": 0.22, "hq": "Guwahati", "desc": "Monsoon landslides & single-line bridge bottlenecks"}
}

TRAIN_CATEGORIES = [
    "Vande Bharat Express", "Rajdhani Express", "Shatabdi Express", "Duronto Express",
    "Tejas Express", "Gatimaan Express", "Humsafar Express", "Jan Shatabdi Express",
    "Superfast Express", "Mail/Express", "Sampark Kranti Express", "Intercity Express",
    "Garib Rath Express", "Passenger Train", "DEMU/MEMU"
]

DEMO_SCENARIOS = {
    "🚅 Preset 1: Premier Vande Bharat Express (NR - Delhi to Varanasi)": {
        "train_number": 22436, "train_type": "Vande Bharat Express",
        "year": 2024, "month": 3, "day_of_week": 2, "departure_hour": 6,
        "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 1, "is_festival_season": 0,
        "season": "Summer", "zone": "Northern Railway (NR)", "zone_abbr": "NR",
        "source_station_category": "A1", "destination_station_category": "A1",
        "distance_km": 760, "num_scheduled_stops": 4, "scheduled_travel_hours": 8.0,
        "track_doubled": 1, "is_hdn_route": 1, "traction_type": "Electric (25kV AC)",
        "is_electrified": 1, "psr_count": 1, "is_circular_route": 0, "is_monsoon_season": 0,
        "is_fog_risk": 0, "fog_risk_score": 0.05, "zone_fog_index": 0.15, "zone_congestion_index": 0.60,
        "season_severity_score": 0.25, "loco_age_years": 2.5, "coach_age_years": 2.0,
        "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 9.2, "seat_utilisation_pct": 95.0,
        "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 88.5,
        "tag": "ON-TIME EXPECTED (3.3%)",
        "story": "Premier high-speed corridor on electrified double track, pristine equipment, zero incoming delay."
    },
    "🚂 Preset 2: Howrah - Amritsar Mail in Heavy Monsoon (ER - Trunk Line)": {
        "train_number": 13006, "train_type": "Mail/Express",
        "year": 2024, "month": 8, "day_of_week": 4, "departure_hour": 21,
        "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 0, "is_festival_season": 1,
        "season": "Monsoon", "zone": "Eastern Railway (ER)", "zone_abbr": "ER",
        "source_station_category": "B", "destination_station_category": "C",
        "distance_km": 1150, "num_scheduled_stops": 24, "scheduled_travel_hours": 26.5,
        "track_doubled": 0, "is_hdn_route": 1, "traction_type": "Diesel",
        "is_electrified": 0, "psr_count": 7, "is_circular_route": 0, "is_monsoon_season": 1,
        "is_fog_risk": 0, "fog_risk_score": 0.10, "zone_fog_index": 0.40, "zone_congestion_index": 0.88,
        "season_severity_score": 0.90, "loco_age_years": 18.0, "coach_age_years": 16.5,
        "has_lhb_coaches": 0, "is_rake_shared": 1, "maintenance_score": 4.1, "seat_utilisation_pct": 98.0,
        "late_incoming_rake": 1, "is_special_train": 1, "route_historical_ontime_pct": 42.0,
        "tag": "HIGH DELAY RISK (98.7%)",
        "story": "Diesel single-track bottleneck with 24 halts, cascading delayed incoming rake, heavy monsoon severity."
    },
    "❄️ Preset 3: Winter Fog Corridor Special (NCR - Kanpur to Delhi)": {
        "train_number": 4011, "train_type": "Superfast Express",
        "year": 2024, "month": 1, "day_of_week": 1, "departure_hour": 4,
        "is_weekend": 0, "is_night_departure": 1, "is_peak_hour": 0, "is_festival_season": 0,
        "season": "Winter/Fog", "zone": "North Central Railway (NCR)", "zone_abbr": "NCR",
        "source_station_category": "A", "destination_station_category": "A1",
        "distance_km": 920, "num_scheduled_stops": 14, "scheduled_travel_hours": 15.0,
        "track_doubled": 1, "is_hdn_route": 1, "traction_type": "Electric (25kV AC)",
        "is_electrified": 1, "psr_count": 5, "is_circular_route": 0, "is_monsoon_season": 0,
        "is_fog_risk": 1, "fog_risk_score": 0.85, "zone_fog_index": 0.82, "zone_congestion_index": 0.90,
        "season_severity_score": 0.85, "loco_age_years": 15.0, "coach_age_years": 14.0,
        "has_lhb_coaches": 1, "is_rake_shared": 1, "maintenance_score": 5.8, "seat_utilisation_pct": 102.0,
        "late_incoming_rake": 1, "is_special_train": 1, "route_historical_ontime_pct": 49.0,
        "tag": "HIGH DELAY RISK (98.4%)",
        "story": "Peak winter fog window (04:00 AM) in North Central zone (fog index 0.82), 90% congestion, shared turnaround."
    },
    "🚆 Preset 4: Southern Coastal Intercity (SR - Chennai to Coimbatore)": {
        "train_number": 12675, "train_type": "Intercity Express",
        "year": 2024, "month": 10, "day_of_week": 3, "departure_hour": 6,
        "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 1, "is_festival_season": 0,
        "season": "Post-Monsoon", "zone": "Southern Railway (SR)", "zone_abbr": "SR",
        "source_station_category": "A1", "destination_station_category": "A",
        "distance_km": 495, "num_scheduled_stops": 6, "scheduled_travel_hours": 7.5,
        "track_doubled": 1, "is_hdn_route": 0, "traction_type": "Electric (25kV AC)",
        "is_electrified": 1, "psr_count": 2, "is_circular_route": 0, "is_monsoon_season": 0,
        "is_fog_risk": 0, "fog_risk_score": 0.02, "zone_fog_index": 0.02, "zone_congestion_index": 0.65,
        "season_severity_score": 0.35, "loco_age_years": 5.0, "coach_age_years": 4.5,
        "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 8.5, "seat_utilisation_pct": 84.0,
        "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 84.0,
        "tag": "ON-TIME EXPECTED (4.0%)",
        "story": "Double electrified track, high route historical punctuality (84%), zero incoming delay, minimal fog."
    }
}

# -----------------------------------------------------------------------------
# 4. REPRODUCIBLE INFERENCE ENGINE
# -----------------------------------------------------------------------------
def run_model_inference(df_input: pd.DataFrame):
    df_clean = clean_data_pandas(df_input, is_train=False)
    if "train_number" in df_clean.columns:
        df_clean = df_clean.drop(columns=["train_number"], errors="ignore")
    
    if iqr_bounds:
        df_clean = handle_outliers_iqr_numpy(df_clean, list(iqr_bounds.keys()))
        
    df_eng = engineer_features_pandas(df_clean)
    
    usable_cat = [c for c in cat_cols if c in df_eng.columns]
    df_encoded = pd.get_dummies(df_eng, columns=usable_cat, dtype=np.uint8)
    
    # Strictly align to 8,111 model features
    df_proc = df_encoded.reindex(columns=feature_columns, fill_value=0)
    
    # Scale numeric features
    valid_num = [c for c in num_cols if c in df_proc.columns]
    df_proc[valid_num] = (
        df_proc[valid_num].astype(np.float32) - train_mean[valid_num]
    ) / train_std[valid_num]
    
    probs = model.predict_proba(df_proc)[:, 1]
    return probs, df_eng

def get_risk_classification(prob: float):
    pct = prob * 100.0
    if pct > 65.0:
        return {
            "status": "HIGH DELAY RISK",
            "alert": "RED ALERT",
            "banner_class": "dispatch-red",
            "pill_class": "pill-red",
            "color": "#dc2626",
            "action": "Urgent Operational Intervention Required: Priority signal clearance at route junctions, alert Divisional Operating Manager (DOM), verify turnaround buffers, and ready relief rake if turnaround is shared."
        }
    elif pct >= 40.0:
        return {
            "status": "MODERATE DELAY RISK",
            "alert": "AMBER ADVISORY",
            "banner_class": "dispatch-amber",
            "pill_class": "pill-amber",
            "color": "#d97706",
            "action": "Advisory Caution: Monitor incoming rake turnaround closely at interchange halts. Prepare platform clearance ahead of peak congestion window."
        }
    else:
        return {
            "status": "ON-TIME EXPECTED",
            "alert": "GREEN NORMAL",
            "banner_class": "dispatch-green",
            "pill_class": "pill-green",
            "color": "#16a34a",
            "action": "Clear for Scheduled Departure: Normal timetable priority. No abnormal delay propagation expected across intermediate divisions."
        }

# -----------------------------------------------------------------------------
# 5. APP HERO HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="ir-hero-header">
    <h1>🚆 Indian Railways Train Delay Prediction & Network Analytics</h1>
    <p>Operational Supervised Machine Learning Dashboard & Decision Support System. Developed for operational demonstration and live dispatch simulation using <strong>Tuned LightGBM</strong> (85.85% Accuracy, 92.10% Recall, 0.9038 F1-Score).</p>
</div>
""", unsafe_allow_html=True)

if not pipeline_ready:
    st.error(f"⚠️ Model Pipeline could not be loaded: {pipeline_err_msg}")
    st.stop()

# -----------------------------------------------------------------------------
# 6. REDESIGNED HUMAN-CRAFTED SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
        <span style="font-size: 1.6rem;">🇮🇳</span>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #0f172a; line-height: 1.2;">Indian Railways</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">Control & Operations Console</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
            <span style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Inference Engine</span>
            <span style="font-size: 0.7rem; font-weight: 700; color: #16a34a; background: #dcfce7; padding: 0.15rem 0.45rem; border-radius: 9999px;">ONLINE</span>
        </div>
        <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a;">Tuned LightGBM</div>
        <div style="font-size: 0.78rem; color: #64748b; margin-top: 0.2rem;">Model Artifact: <code>pipeline.joblib</code> (891 KB)</div>
        <div style="font-size: 0.78rem; color: #64748b;">Inference Speed: <strong>&lt; 15 ms</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎯 Dispatch Policy Thresholds")
    st.markdown("""
    <div class="sidebar-card">
        <div style="font-size: 0.8rem; margin-bottom: 0.35rem; display: flex; justify-content: space-between;">
            <span>🟢 <strong>Green (On-Time)</strong></span>
            <span style="color: #16a34a; font-weight: 700;">&lt; 40.0%</span>
        </div>
        <div style="font-size: 0.8rem; margin-bottom: 0.35rem; display: flex; justify-content: space-between;">
            <span>🟡 <strong>Amber (Caution)</strong></span>
            <span style="color: #d97706; font-weight: 700;">40% – 65%</span>
        </div>
        <div style="font-size: 0.8rem; display: flex; justify-content: space-between;">
            <span>🔴 <strong>Red (Critical)</strong></span>
            <span style="color: #dc2626; font-weight: 700;">&gt; 65.0%</span>
        </div>
        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 0.5rem; line-height: 1.3;">Thresholds per Section 13 Demonstration Rules.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚙️ System Specifications")
    st.markdown("""
    <div class="sidebar-card" style="font-size: 0.82rem; line-height: 1.5; color: #334155;">
        <div><strong>Deployment Mode:</strong> Production Ready</div>
        <div><strong>Target Variable:</strong> <code>is_delayed</code> (&gt;15 min delay)</div>
        <div><strong>Features Active:</strong> 43 domain + 8,111 sparse</div>
        <div><strong>Data Leakage Safeguard:</strong> Active</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. MAIN NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_predict, tab_lab, tab_batch, tab_zones = st.tabs([
    "🚄 Single-Journey Predictor",
    "🔬 Model Lab & Score Calculation",
    "📊 Batch Fleet Delay Audit",
    "🗺️ Network Punctuality & 16 Zones"
])

# Initialize session state for user-triggered prediction
if "active_prediction" not in st.session_state:
    st.session_state["active_prediction"] = None
if "current_preset_loaded" not in st.session_state:
    st.session_state["current_preset_loaded"] = "🚅 Preset 1: Premier Vande Bharat Express (NR - Delhi to Varanasi)"

# =============================================================================
# TAB 1: SINGLE-JOURNEY PREDICTOR (STEP-BY-STEP + PREDICT BUTTON)
# =============================================================================
with tab_predict:
    st.markdown("#### ⚡ 1-Click Demonstration Scenarios")
    st.caption("Click any card below to load a documented Indian Railways test journey:")

    demo_cols = st.columns(4)
    preset_keys = list(DEMO_SCENARIOS.keys())

    for i, p_key in enumerate(preset_keys):
        sc_info = DEMO_SCENARIOS[p_key]
        with demo_cols[i]:
            card_title = p_key.split(":")[1].split("(")[0].strip()
            is_active = (st.session_state["current_preset_loaded"] == p_key)
            active_class = "active" if is_active else ""
            pill_type = "pill-green" if "3.3%" in sc_info["tag"] or "4.0%" in sc_info["tag"] else "pill-red"
            
            st.markdown(f"""
            <div class="preset-card-box {active_class}">
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.35rem;">{card_title}</div>
                    <div style="font-size: 0.8rem; color: #64748b; line-height: 1.35;">{sc_info['story']}</div>
                </div>
                <div style="margin-top: 0.75rem;">
                    <span class="status-pill {pill_type}">{sc_info['tag']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Load {card_title[:16]}", key=f"btn_p_{i}"):
                st.session_state["current_preset_loaded"] = p_key
                # Auto-run prediction when a preset card is clicked
                df_preset = pd.DataFrame([DEMO_SCENARIOS[p_key]])
                preset_probs, preset_df_eng = run_model_inference(df_preset)
                st.session_state["active_prediction"] = {
                    "prob": preset_probs[0],
                    "df_eng": preset_df_eng,
                    "journey": DEMO_SCENARIOS[p_key]
                }
                st.rerun()

    preset_data = DEMO_SCENARIOS.get(st.session_state["current_preset_loaded"], DEMO_SCENARIOS[preset_keys[0]])

    st.markdown("---")
    st.markdown("#### 🎛️ Configure Journey Parameters (Step-by-Step)")
    st.caption("Tune the inputs across 4 clear steps, then click **'Run Journey Delay Prediction'** below to execute the model.")

    # 4-Step Accordion Wizard
    with st.expander("📍 **Step 1: Train & Route Basics** (Category, Distance, Timetable)", expanded=True):
        s1_c1, s1_c2, s1_c3, s1_c4 = st.columns(4)
        with s1_c1:
            train_type = st.selectbox(
                "Train Category",
                options=TRAIN_CATEGORIES,
                index=TRAIN_CATEGORIES.index(preset_data["train_type"]) if preset_data and preset_data["train_type"] in TRAIN_CATEGORIES else 0
            )
            train_number = st.text_input("Train Number", value=str(preset_data["train_number"] if preset_data else "22436"))
        with s1_c2:
            distance_km = st.number_input("Distance (km)", min_value=20, max_value=4500, value=int(preset_data["distance_km"] if preset_data else 760), step=10)
            scheduled_travel_hours = st.number_input("Scheduled Travel (Hours)", min_value=0.5, max_value=90.0, value=float(preset_data["scheduled_travel_hours"] if preset_data else 8.0), step=0.5)
        with s1_c3:
            num_scheduled_stops = st.number_input("Intermediate Stops / Halts", min_value=0, max_value=120, value=int(preset_data["num_scheduled_stops"] if preset_data else 4), step=1)
            derived_speed = distance_km / max(scheduled_travel_hours, 0.1)
            st.metric("Derived Scheduled Speed", f"{derived_speed:.1f} km/h")
        with s1_c4:
            source_cat = st.selectbox("Origin Station Class", ["A1", "A", "B", "C", "D", "E"], index=0)
            dest_cat = st.selectbox("Destination Class", ["A1", "A", "B", "C", "D", "E"], index=0)

    with st.expander("🛤️ **Step 2: Zone & Track Infrastructure** (Administrative Zone, Tracks, Traction)", expanded=True):
        s2_c1, s2_c2, s2_c3 = st.columns(3)
        with s2_c1:
            zone_selected = st.selectbox(
                "Railway Zone",
                options=list(ZONE_DATABASE.keys()),
                index=list(ZONE_DATABASE.keys()).index(preset_data["zone"]) if preset_data and preset_data["zone"] in ZONE_DATABASE else 0
            )
            z_meta = ZONE_DATABASE[zone_selected]
            st.caption(f"**Zone HQ:** {z_meta['hq']} | **Capacity Utilisation:** {z_meta['congestion']:.2f} | **Fog Vulnerability:** {z_meta['fog']:.2f}")
        with s2_c2:
            track_doubled = st.checkbox("Track Doubled / Multi-track", value=bool(preset_data["track_doubled"] if preset_data else True))
            is_hdn = st.checkbox("High Density Network (HDN Corridor)", value=bool(preset_data["is_hdn_route"] if preset_data else True))
        with s2_c3:
            traction_type = st.selectbox("Traction System", ["Electric (25kV AC)", "Diesel", "Dual"], index=0 if (not preset_data or "Electric" in preset_data["traction_type"]) else 1)
            is_electrified = (traction_type != "Diesel")

    with st.expander("🔧 **Step 3: Rolling Stock & Turnaround Risk** (Incoming Rake, Coach Type, History)", expanded=True):
        s3_c1, s3_c2, s3_c3 = st.columns(3)
        with s3_c1:
            late_incoming_rake = st.checkbox(
                "🚨 Late Incoming Rake (Turnaround Delayed)",
                value=bool(preset_data["late_incoming_rake"] if preset_data else False),
                help="High impact feature: the incoming train for this rake arrived late from its previous service."
            )
            is_rake_shared = st.checkbox("Shared Rake (Turnaround Service)", value=bool(preset_data["is_rake_shared"] if preset_data else False))
        with s3_c2:
            has_lhb = st.checkbox("Modern LHB Coaches (vs ICF)", value=bool(preset_data["has_lhb_coaches"] if preset_data else True))
            is_special = st.checkbox("Special / Holiday Train", value=bool(preset_data["is_special_train"] if preset_data else False))
        with s3_c3:
            route_historical_ontime_pct = st.slider("Route Historical On-Time %", min_value=10.0, max_value=100.0, value=float(preset_data["route_historical_ontime_pct"] if preset_data else 88.5), step=0.5)

    with st.expander("🌦️ **Step 4: Weather & Departure Window** (Season, Departure Hour, Day)", expanded=True):
        s4_c1, s4_c2, s4_c3 = st.columns(3)
        with s4_c1:
            season = st.selectbox("Season", ["Winter/Fog", "Summer", "Monsoon", "Pre-Monsoon", "Post-Monsoon", "Autumn"], index=1 if not preset_data else ["Winter/Fog", "Summer", "Monsoon", "Pre-Monsoon", "Post-Monsoon", "Autumn"].index(preset_data["season"]))
            is_festival = st.checkbox("Festival Peak Period", value=bool(preset_data["is_festival_season"] if preset_data else False))
        with s4_c2:
            departure_hour = st.slider("Departure Hour (0–23)", 0, 23, int(preset_data["departure_hour"] if preset_data else 6))
            is_night = 1 if (departure_hour >= 22 or departure_hour < 4) else 0
            is_peak = 1 if ((6 <= departure_hour <= 8) or (17 <= departure_hour <= 20)) else 0
        with s4_c3:
            day_of_week = st.selectbox("Day of Week", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x], index=int(preset_data["day_of_week"] if preset_data else 2))
            is_weekend = 1 if day_of_week in [5, 6] else 0
            month = st.slider("Month", 1, 12, int(preset_data["month"] if preset_data else 3))

    # Optional Advanced Drawer
    with st.expander("⚙️ Optional Advanced Parameters (Locomotive Age, PSR Count, Weather Scores)"):
        st.caption("Auto-populated with domain-realistic values. Adjust only to evaluate extreme edge cases.")
        adv1, adv2, adv3, adv4 = st.columns(4)
        with adv1:
            loco_age_years = st.number_input("Locomotive Age (Years)", 0.5, 40.0, float(preset_data["loco_age_years"] if preset_data else 2.5), 0.5)
            coach_age_years = st.number_input("Coach Age (Years)", 0.5, 40.0, float(preset_data["coach_age_years"] if preset_data else 2.0), 0.5)
        with adv2:
            maintenance_score = st.slider("Maintenance Score (1-10)", 1.0, 10.0, float(preset_data["maintenance_score"] if preset_data else 9.2), 0.1)
            seat_utilisation_pct = st.number_input("Seat Utilisation %", 10.0, 160.0, float(preset_data["seat_utilisation_pct"] if preset_data else 95.0), 1.0)
        with adv3:
            psr_count = st.number_input("Speed Restrictions (PSR)", 0, 25, int(preset_data["psr_count"] if preset_data else 1))
            is_circular = st.checkbox("Circular Route", value=bool(preset_data["is_circular_route"] if preset_data else False))
        with adv4:
            fog_risk_score = st.slider("Fog Risk Score", 0.0, 1.0, float(preset_data["fog_risk_score"] if preset_data else 0.05), 0.01)
            season_severity_score = st.slider("Season Severity Score", 0.05, 1.0, float(preset_data["season_severity_score"] if preset_data else 0.25), 0.01)

    # Compile Active Journey Dictionary
    active_journey = {
        "train_number": train_number,
        "train_type": train_type,
        "year": 2024,
        "month": month,
        "day_of_week": day_of_week,
        "departure_hour": departure_hour,
        "is_weekend": is_weekend,
        "is_night_departure": is_night,
        "is_peak_hour": is_peak,
        "is_festival_season": int(is_festival),
        "season": season,
        "zone": zone_selected,
        "zone_abbr": z_meta["abbr"],
        "source_station_category": source_cat,
        "destination_station_category": dest_cat,
        "distance_km": distance_km,
        "num_scheduled_stops": num_scheduled_stops,
        "scheduled_travel_hours": scheduled_travel_hours,
        "track_doubled": int(track_doubled),
        "is_hdn_route": int(is_hdn),
        "traction_type": traction_type,
        "is_electrified": int(is_electrified),
        "psr_count": psr_count,
        "is_circular_route": int(is_circular),
        "is_monsoon_season": 1 if season == "Monsoon" or month in [6, 7, 8, 9] else 0,
        "is_fog_risk": 1 if (season == "Winter/Fog" and z_meta["fog"] > 0.4) else 0,
        "fog_risk_score": fog_risk_score,
        "zone_fog_index": z_meta["fog"],
        "zone_congestion_index": z_meta["congestion"],
        "season_severity_score": season_severity_score,
        "loco_age_years": loco_age_years,
        "coach_age_years": coach_age_years,
        "has_lhb_coaches": int(has_lhb),
        "is_rake_shared": int(is_rake_shared),
        "maintenance_score": maintenance_score,
        "seat_utilisation_pct": seat_utilisation_pct,
        "late_incoming_rake": int(late_incoming_rake),
        "is_special_train": int(is_special),
        "route_historical_ontime_pct": route_historical_ontime_pct
    }

    # -------------------------------------------------------------------------
    # EXPLICIT PREDICT BUTTON (TRIGGER INFERENCE & LOAD RESULTS)
    # -------------------------------------------------------------------------
    st.markdown("")
    col_btn, _ = st.columns([1.5, 2.5])
    with col_btn:
        run_prediction_btn = st.button("🚀 Run Journey Delay Prediction", type="primary", use_container_width=True)

    if run_prediction_btn:
        with st.spinner("Processing features through LightGBM pipeline..."):
            df_active = pd.DataFrame([active_journey])
            live_probs, live_df_eng = run_model_inference(df_active)
            st.session_state["active_prediction"] = {
                "prob": live_probs[0],
                "df_eng": live_df_eng,
                "journey": active_journey
            }

    # If no prediction has run yet, auto-run on initial load with the preset
    if st.session_state["active_prediction"] is None:
        df_init = pd.DataFrame([preset_data])
        init_probs, init_df_eng = run_model_inference(df_init)
        st.session_state["active_prediction"] = {
            "prob": init_probs[0],
            "df_eng": init_df_eng,
            "journey": preset_data
        }

    # -------------------------------------------------------------------------
    # DEDICATED PREDICTION RESULTS COMPONENT
    # -------------------------------------------------------------------------
    res = st.session_state["active_prediction"]
    pred_prob = res["prob"]
    df_engineered_active = res["df_eng"]
    risk_info = get_risk_classification(pred_prob)

    st.markdown("---")
    st.markdown("### 🎯 Live Prediction Output & Dispatch Order")

    res_card1, res_card2, res_card3 = st.columns([1.6, 1.2, 1.2])

    with res_card1:
        st.markdown(f"""
        <div class="modern-card" style="border-left: 6px solid {risk_info['color']};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.05em;">Predicted Delay Probability</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: {risk_info['color']}; margin: 0.2rem 0;">{pred_prob*100:.1f}%</div>
            <div style="font-size: 0.82rem; color: #64748b;">Target: Arrival delay &gt; 15 minutes at destination</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(float(min(max(pred_prob, 0.0), 1.0)))

    with res_card2:
        st.markdown(f"""
        <div class="modern-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.05em;">Operational Risk Status</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: {risk_info['color']}; margin-top: 0.4rem;">{risk_info['status']}</div>
            <div style="margin-top: 0.5rem;"><span class="status-pill {risk_info['pill_class']}">{risk_info['status']}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with res_card3:
        st.markdown(f"""
        <div class="modern-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.05em;">Dispatch Alert Directive</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: {risk_info['color']}; margin-top: 0.4rem;">{risk_info['alert']}</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-top: 0.4rem;">Division Punctuality Protocol</div>
        </div>
        """, unsafe_allow_html=True)

    # Operational Directive Banner with Rounded Curves
    st.markdown(f"""
    <div class="dispatch-banner {risk_info['banner_class']}">
        <div style="font-weight: 800; font-size: 1.05rem;">🚨 Operational Protocol: {risk_info['alert']}</div>
        <div style="font-size: 0.92rem; line-height: 1.5;">{risk_info['action']}</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: MODEL LAB & SCORE CALCULATION ENGINE (ALGORITHM & METRICS SHOWCASE)
# =============================================================================
with tab_lab:
    st.markdown("### 🔬 Model Lab & Live Score Calculation Engine")
    st.markdown("This component demonstrates **how the machine learning pipeline operates**, **why LightGBM was selected over other architectures**, and **how all mathematical scores and features are calculated**.")

    # 1. LIVE MATHEMATICAL FORMULA BREAKDOWN
    st.markdown("#### 📐 Stage-by-Stage Mathematical Feature Formulas (Current Journey)")
    st.caption("Real-time LaTeX calculation trace showing exact values computed for the active journey:")

    eng_row = df_engineered_active.iloc[0]
    j_active = st.session_state["active_prediction"]["journey"]

    calc1, calc2 = st.columns(2)
    with calc1:
        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">1. Average Scheduled Speed (v_avg)</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Feasibility speed implied by scheduled timetable distance and duration:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{avg\_speed\_kmh}} = \frac{{\text{{distance\_km}}}}{{\text{{scheduled\_travel\_hours}}}} = \frac{{{j_active['distance_km']}}}{{{j_active['scheduled_travel_hours']:.1f}}} = \mathbf{{{eng_row['avg_speed_kmh']:.2f}\text{{ km/h}}}}")

        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">2. Halt / Stop Density Index</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Quantifies route friction caused by frequent deceleration and acceleration cycles:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{stops\_density}} = \frac{{\text{{num\_scheduled\_stops}}}}{{\frac{{\text{{distance\_km}}}}{{100}} + 0.1}} = \frac{{{j_active['num_scheduled_stops']}}}{{\frac{{{j_active['distance_km']}}}{{100}} + 0.1}} = \mathbf{{{eng_row['stops_density']:.3f}}}")

        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">3. Composite Weather Severity Interaction</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Multiplicative interaction capturing compounding seasonal, monsoon, and fog risks:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{composite\_weather}} = \text{{season\_score}} \times (1.0 + 0.5 \cdot \text{{monsoon}} + 0.5 \cdot \text{{fog}}) = \mathbf{{{eng_row['composite_weather_severity']:.3f}}}")

    with calc2:
        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">4. Network Vulnerability Index</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Zone congestion index amplified by High Density Network (HDN), buffered by track doubling:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{network\_vuln}} = \text{{congestion}} \times (1.0 + 0.5 \cdot \text{{is\_hdn}} - 0.3 \cdot \text{{track\_doubled}}) = \mathbf{{{eng_row['network_vulnerability']:.3f}}}")

        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">5. Rake Turnaround Cascading Risk</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Product of late incoming rake status and shared trainset configuration:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{rake\_turnaround\_risk}} = \text{{late\_incoming}} \times \text{{is\_shared}} = {int(j_active['late_incoming_rake'])} \times {int(j_active['is_rake_shared'])} = \mathbf{{{eng_row['rake_turnaround_risk']:.0f}}}")

        st.markdown(f"""
        <div class="formula-pill-box">
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.3rem;">6. Historical Delay Risk Prior</div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.4rem;">Transforms route historical on-time punctuality into a 0–1 risk prior:</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(rf"\text{{historical\_delay\_risk}} = \frac{{100.0 - \text{{ontime\_pct}}}}{{100.0}} = \frac{{100.0 - {j_active['route_historical_ontime_pct']:.1f}}}{{100.0}} = \mathbf{{{eng_row['historical_delay_risk']:.3f}}}")

    st.markdown("---")

    # 2. DATA LEAKAGE QUARANTINE PROOF
    st.markdown("#### 🛡️ Data Leakage Quarantine Safeguards")
    st.markdown("""
    In railway machine learning, raw datasets contain attributes that cause severe **data leakage** because they only exist *after* the train arrives.
    Our pipeline enforces a strict pre-departure quarantine boundary:
    """)

    l_col1, l_col2 = st.columns(2)
    with l_col1:
        st.markdown("""
        <div class="modern-card" style="border-left: 5px solid #dc2626; background: #fff5f5;">
            <div style="font-weight: 800; color: #991b1b; font-size: 0.95rem; margin-bottom: 0.4rem;">🚫 Quarantined Target Leakage Columns (Excluded)</div>
            <ul style="margin: 0; padding-left: 1.2rem; color: #7f1d1d; font-size: 0.88rem; line-height: 1.6;">
                <li><code>delay_minutes</code>: Destination arrival delay in minutes (unavailable before departure).</li>
                <li><code>primary_delay_cause</code>: Post-journey operational investigation findings.</li>
                <li><code>is_overloaded</code>: Zero-variance constant feature dropped during data cleaning.</li>
                <li><code>journey_id</code> & <code>departure_date</code>: Unique identifier and raw strings dropped to prevent memorization.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with l_col2:
        st.markdown("""
        <div class="modern-card" style="border-left: 5px solid #16a34a; background: #f0fdf4;">
            <div style="font-weight: 800; color: #166534; font-size: 0.95rem; margin-bottom: 0.4rem;">✅ Permitted Pre-Departure Signals (Included)</div>
            <ul style="margin: 0; padding-left: 1.2rem; color: #14532d; font-size: 0.88rem; line-height: 1.6;">
                <li>Timetable schedule: Route distance, travel duration, halt density.</li>
                <li>Track infrastructure: Track doubling, electrification, PSR speed restriction count.</li>
                <li>Rolling-stock turnaround status: Late incoming rake arrival condition.</li>
                <li>Atmospheric conditions: Seasonal base severity score, zone fog index.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. OFFICIAL 7-MODEL BENCHMARK TABLE
    st.markdown("#### 🏆 Official Comparative Model Benchmark")
    st.markdown("Evaluation metrics from the comprehensive 1.5M-record study (Stratified 80:20 Train-Validation Split):")

    model_benchmark_data = [
        {
            "Model": "Tuned LightGBM (Champion)",
            "Algorithm Family": "Gradient Boosted Trees",
            "Accuracy": 0.8585, "Precision": 0.8872, "Recall": 0.9210, "F1-Score": 0.9038, "ROC-AUC": 0.9121,
            "Selection Rationale": "Highest validation accuracy, recall, and F1-score across all evaluations. Sub-15ms inference latency."
        },
        {
            "Model": "Logistic Regression",
            "Algorithm Family": "Linear Sigmoid Model",
            "Accuracy": 0.8570, "Precision": 0.8901, "Recall": 0.9148, "F1-Score": 0.9023, "ROC-AUC": 0.9229,
            "Selection Rationale": "Strong linear baseline; achieved the highest overall ROC-AUC (0.9229) due to standardized monotonic features."
        },
        {
            "Model": "Default LightGBM",
            "Algorithm Family": "Gradient Boosted Trees",
            "Accuracy": 0.8560, "Precision": 0.8889, "Recall": 0.9148, "F1-Score": 0.9016, "ROC-AUC": 0.9152,
            "Selection Rationale": "Baseline tree ensemble before randomized hyperparameter tuning."
        },
        {
            "Model": "Decision Tree",
            "Algorithm Family": "Recursive Split Tree",
            "Accuracy": 0.8130, "Precision": 0.8585, "Recall": 0.8870, "F1-Score": 0.8725, "ROC-AUC": 0.8593,
            "Selection Rationale": "Captures non-linear feature splits but prone to higher variance and lower recall."
        },
        {
            "Model": "Tuned Random Forest",
            "Algorithm Family": "Bagged Tree Ensemble",
            "Accuracy": 0.7870, "Precision": 0.7783, "Recall": 0.9854, "F1-Score": 0.8697, "ROC-AUC": 0.8854,
            "Selection Rationale": "High recall (98.54%), but lower precision (77.83%) due to false positive alarms on borderline trains."
        },
        {
            "Model": "Default Random Forest",
            "Algorithm Family": "Bagged Tree Ensemble",
            "Accuracy": 0.7730, "Precision": 0.7640, "Recall": 0.9917, "F1-Score": 0.8631, "ROC-AUC": 0.8831,
            "Selection Rationale": "Bootstrap aggregation baseline; biased towards predicting delay."
        },
        {
            "Model": "Dummy Classifier Baseline",
            "Algorithm Family": "Majority Class Predictor",
            "Accuracy": 0.7215, "Precision": 0.7215, "Recall": 1.0000, "F1-Score": 0.8382, "ROC-AUC": 0.5000,
            "Selection Rationale": "Trivial reference baseline. Proves that our machine learning model adds +13.7% accuracy gain."
        }
    ]

    bench_df = pd.DataFrame(model_benchmark_data)
    st.dataframe(
        bench_df[["Model", "Algorithm Family", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "Selection Rationale"]].style.format({
            "Accuracy": "{:.2%}", "Precision": "{:.2%}", "Recall": "{:.2%}", "F1-Score": "{:.4f}", "ROC-AUC": "{:.4f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # 4. TOP FEATURE IMPORTANCES & PRODUCTION ARCHITECTURE
    feat_col, spec_col = st.columns([1.3, 1])

    with feat_col:
        st.markdown("#### 📊 Most Influential Operational Drivers")
        st.caption("Feature importances derived from the 80 decision trees in the fitted LightGBM ensemble:")
        
        if hasattr(model, "feature_importances_"):
            importances = pd.Series(model.feature_importances_, index=feature_columns)
            top_features = importances.sort_values(ascending=False).head(12)
            
            fig_imp, ax_imp = plt.subplots(figsize=(7, 4.5))
            top_features.sort_values().plot(kind="barh", ax=ax_imp, color="#0b2545")
            ax_imp.set_xlabel("Split Importance (Number of Tree Splits)", fontsize=9)
            ax_imp.grid(axis="x", linestyle="--", alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig_imp)
        else:
            st.info("Feature importance data not available.")

    with spec_col:
        st.markdown("#### ⚙️ Production Pipeline Specifications")
        st.markdown("""
        <div class="modern-card">
            <div style="font-weight: 800; font-size: 0.95rem; color: #0b2545; margin-bottom: 0.5rem;">Pipeline Specifications</div>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.85rem; color: #334155; line-height: 1.6;">
                <li><strong>Model Architecture:</strong> LightGBM Gradient Boosted Trees (<code>LGBMClassifier</code>)</li>
                <li><strong>Hyperparameters:</strong> <code>n_estimators=80</code>, <code>max_depth=6</code>, <code>num_leaves=63</code>, <code>learning_rate=0.05</code></li>
                <li><strong>Preprocessing:</strong> Pure Pandas & NumPy vectorized transformations (zero heavy transformer dependencies)</li>
                <li><strong>Feature Space:</strong> 43 continuous/discrete features aligned to 8,111 one-hot dummy columns</li>
                <li><strong>Memory Efficiency:</strong> ~891 KB serialized pipeline; zero raw dataset dependency at startup</li>
                <li><strong>Inference Latency:</strong> &lt; 15 ms per journey</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 3: BATCH FLEET AUDIT
# =============================================================================
with tab_batch:
    st.markdown("### 📊 Operational Batch Fleet Audit")
    st.markdown("Audit a fleet of multiple train services in a single run without loading the 1.5M row dataset.")

    batch_source = st.radio(
        "Choose Batch Source:",
        options=["Run 10-Journey Benchmark Fleet (Curated IR Services)", "Upload Custom CSV File"],
        horizontal=True
    )

    fleet_df = None
    if "10-Journey" in batch_source:
        benchmark_fleet = [
            DEMO_SCENARIOS[preset_keys[0]],
            DEMO_SCENARIOS[preset_keys[1]],
            DEMO_SCENARIOS[preset_keys[2]],
            DEMO_SCENARIOS[preset_keys[3]],
            # Extra representative services
            {
                "train_number": 12009, "train_type": "Shatabdi Express", "year": 2024, "month": 4, "day_of_week": 1,
                "departure_hour": 6, "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 1, "is_festival_season": 0,
                "season": "Summer", "zone": "Western Railway (WR)", "zone_abbr": "WR", "source_station_category": "A1",
                "destination_station_category": "A1", "distance_km": 493, "num_scheduled_stops": 5, "scheduled_travel_hours": 6.2,
                "track_doubled": 1, "is_hdn_route": 1, "traction_type": "Electric (25kV AC)", "is_electrified": 1, "psr_count": 2,
                "is_circular_route": 0, "is_monsoon_season": 0, "is_fog_risk": 0, "fog_risk_score": 0.02, "zone_fog_index": 0.05,
                "zone_congestion_index": 0.83, "season_severity_score": 0.30, "loco_age_years": 4.0, "coach_age_years": 3.5,
                "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 8.8, "seat_utilisation_pct": 92.0,
                "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 82.0
            },
            {
                "train_number": 12423, "train_type": "Rajdhani Express", "year": 2024, "month": 1, "day_of_week": 5,
                "departure_hour": 20, "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 0, "is_festival_season": 0,
                "season": "Winter/Fog", "zone": "Northeast Frontier Railway (NFR)", "zone_abbr": "NFR", "source_station_category": "A1",
                "destination_station_category": "A1", "distance_km": 2420, "num_scheduled_stops": 18, "scheduled_travel_hours": 37.5,
                "track_doubled": 1, "is_hdn_route": 1, "traction_type": "Electric (25kV AC)", "is_electrified": 1, "psr_count": 4,
                "is_circular_route": 0, "is_monsoon_season": 0, "is_fog_risk": 1, "fog_risk_score": 0.65, "zone_fog_index": 0.22,
                "zone_congestion_index": 0.58, "season_severity_score": 0.80, "loco_age_years": 7.5, "coach_age_years": 6.0,
                "has_lhb_coaches": 1, "is_rake_shared": 1, "maintenance_score": 8.0, "seat_utilisation_pct": 96.0,
                "late_incoming_rake": 1, "is_special_train": 0, "route_historical_ontime_pct": 65.0
            },
            {
                "train_number": 58117, "train_type": "Passenger Train", "year": 2024, "month": 7, "day_of_week": 0,
                "departure_hour": 9, "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 0, "is_festival_season": 0,
                "season": "Monsoon", "zone": "South East Central Railway (SECR)", "zone_abbr": "SECR", "source_station_category": "C",
                "destination_station_category": "D", "distance_km": 310, "num_scheduled_stops": 28, "scheduled_travel_hours": 8.5,
                "track_doubled": 0, "is_hdn_route": 0, "traction_type": "Diesel", "is_electrified": 0, "psr_count": 6,
                "is_circular_route": 0, "is_monsoon_season": 1, "is_fog_risk": 0, "fog_risk_score": 0.05, "zone_fog_index": 0.28,
                "zone_congestion_index": 0.68, "season_severity_score": 0.75, "loco_age_years": 22.0, "coach_age_years": 24.0,
                "has_lhb_coaches": 0, "is_rake_shared": 1, "maintenance_score": 3.5, "seat_utilisation_pct": 115.0,
                "late_incoming_rake": 1, "is_special_train": 0, "route_historical_ontime_pct": 39.0
            },
            {
                "train_number": 12740, "train_type": "Garib Rath Express", "year": 2024, "month": 5, "day_of_week": 2,
                "departure_hour": 20, "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 0, "is_festival_season": 0,
                "season": "Summer", "zone": "South Central Railway (SCR)", "zone_abbr": "SCR", "source_station_category": "A1",
                "destination_station_category": "A1", "distance_km": 700, "num_scheduled_stops": 8, "scheduled_travel_hours": 11.5,
                "track_doubled": 1, "is_hdn_route": 0, "traction_type": "Electric (25kV AC)", "is_electrified": 1, "psr_count": 2,
                "is_circular_route": 0, "is_monsoon_season": 0, "is_fog_risk": 0, "fog_risk_score": 0.02, "zone_fog_index": 0.04,
                "zone_congestion_index": 0.72, "season_severity_score": 0.40, "loco_age_years": 10.0, "coach_age_years": 9.0,
                "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 7.5, "seat_utilisation_pct": 98.0,
                "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 78.0
            },
            {
                "train_number": 12260, "train_type": "Duronto Express", "year": 2024, "month": 2, "day_of_week": 3,
                "departure_hour": 17, "is_weekend": 0, "is_night_departure": 0, "is_peak_hour": 1, "is_festival_season": 0,
                "season": "Winter/Fog", "zone": "Eastern Railway (ER)", "zone_abbr": "ER", "source_station_category": "A1",
                "destination_station_category": "A1", "distance_km": 1450, "num_scheduled_stops": 4, "scheduled_travel_hours": 17.0,
                "track_doubled": 1, "is_hdn_route": 1, "traction_type": "Electric (25kV AC)", "is_electrified": 1, "psr_count": 3,
                "is_circular_route": 0, "is_monsoon_season": 0, "is_fog_risk": 1, "fog_risk_score": 0.45, "zone_fog_index": 0.32,
                "zone_congestion_index": 0.95, "season_severity_score": 0.50, "loco_age_years": 5.0, "coach_age_years": 4.0,
                "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 9.0, "seat_utilisation_pct": 94.0,
                "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 74.0
            },
            {
                "train_number": 12080, "train_type": "Jan Shatabdi Express", "year": 2024, "month": 9, "day_of_week": 6,
                "departure_hour": 14, "is_weekend": 1, "is_night_departure": 0, "is_peak_hour": 0, "is_festival_season": 0,
                "season": "Post-Monsoon", "zone": "South Western Railway (SWR)", "zone_abbr": "SWR", "source_station_category": "A",
                "destination_station_category": "A1", "distance_km": 460, "num_scheduled_stops": 7, "scheduled_travel_hours": 7.2,
                "track_doubled": 1, "is_hdn_route": 0, "traction_type": "Diesel", "is_electrified": 0, "psr_count": 2,
                "is_circular_route": 0, "is_monsoon_season": 0, "is_fog_risk": 0, "fog_risk_score": 0.01, "zone_fog_index": 0.02,
                "zone_congestion_index": 0.60, "season_severity_score": 0.30, "loco_age_years": 8.0, "coach_age_years": 7.0,
                "has_lhb_coaches": 1, "is_rake_shared": 0, "maintenance_score": 8.1, "seat_utilisation_pct": 89.0,
                "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 83.0
            }
        ]
        fleet_df = pd.DataFrame(benchmark_fleet)
        fleet_df["journey_id"] = [f"BENCH_{i+1:02d}" for i in range(len(fleet_df))]
    else:
        file_up = st.file_uploader("Upload CSV containing train journeys:", type=["csv"])
        if file_up:
            fleet_df = pd.read_csv(file_up)
            st.success(f"Loaded {len(fleet_df):,} journey records.")

    if fleet_df is not None:
        batch_probs, _ = run_model_inference(fleet_df)
        fleet_res = fleet_df.copy()
        fleet_res["delay_probability"] = np.round(batch_probs * 100.0, 1)
        fleet_res["operational_status"] = [
            "HIGH DELAY RISK" if p > 0.65 else ("MODERATE DELAY RISK" if p >= 0.40 else "ON-TIME EXPECTED")
            for p in batch_probs
        ]
        fleet_res["dispatch_alert"] = [
            "RED" if p > 0.65 else ("AMBER" if p >= 0.40 else "GREEN")
            for p in batch_probs
        ]

        b_c1, b_c2, b_c3, b_c4 = st.columns(4)
        n_total = len(fleet_res)
        n_high = (fleet_res["operational_status"] == "HIGH DELAY RISK").sum()
        n_mod = (fleet_res["operational_status"] == "MODERATE DELAY RISK").sum()
        n_ontime = (fleet_res["operational_status"] == "ON-TIME EXPECTED").sum()

        with b_c1: st.metric("Audited Journeys", f"{n_total:,}")
        with b_c2: st.metric("High Delay Risk (RED)", f"{n_high:,}", f"{n_high/n_total*100:.1f}%")
        with b_c3: st.metric("Moderate Risk (AMBER)", f"{n_mod:,}", f"{n_mod/n_total*100:.1f}%")
        with b_c4: st.metric("On-Time (GREEN)", f"{n_ontime:,}", f"{n_ontime/n_total*100:.1f}%")

        disp_cols = [
            "journey_id", "train_number", "train_type", "zone_abbr", "season",
            "distance_km", "delay_probability", "operational_status", "dispatch_alert"
        ]
        valid_disp = [c for c in disp_cols if c in fleet_res.columns]
        st.dataframe(fleet_res[valid_disp], use_container_width=True)

        csv_buf = io.StringIO()
        fleet_res.to_csv(csv_buf, index=False)
        st.download_button(
            "📥 Download Audited Predictions CSV",
            data=csv_buf.getvalue(),
            file_name="indian_railways_delay_predictions.csv",
            mime="text/csv"
        )


# =============================================================================
# TAB 4: NETWORK PUNCTUALITY & 16 ZONES
# =============================================================================
with tab_zones:
    st.markdown("### 🗺️ Network Punctuality & 16 Zones Stress Matrix")
    st.markdown("Analysis of all 16 Indian Railways administrative zones, contrasting network congestion and winter fog vulnerability.")

    zones_table = pd.DataFrame([
        {
            "Zone": name, "Abbr": d["abbr"], "HQ": d["hq"],
            "Congestion Index": d["congestion"], "Fog Vulnerability": d["fog"],
            "Operational Stress Context": d["desc"]
        }
        for name, d in ZONE_DATABASE.items()
    ]).sort_values("Congestion Index", ascending=False)

    z1, z2 = st.columns([1.4, 1])
    with z1:
        fig_z, ax_z = plt.subplots(figsize=(8, 4.5))
        idx = np.arange(len(zones_table))
        w = 0.38
        ax_z.bar(idx - w/2, zones_table["Congestion Index"], w, label="Congestion Index", color="#0b2545")
        ax_z.bar(idx + w/2, zones_table["Fog Vulnerability"], w, label="Fog Vulnerability", color="#ea580c")
        ax_z.set_ylabel("Index Score (0–1.0)")
        ax_z.set_title("Network Congestion vs Fog Vulnerability Across 16 IR Zones", fontweight="bold", pad=12)
        ax_z.set_xticks(idx)
        ax_z.set_xticklabels(zones_table["Abbr"], rotation=45, ha="right")
        ax_z.legend()
        ax_z.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig_z)

    with z2:
        st.markdown(f"""
        <div class="modern-card">
            <div style="font-weight: 800; color: #0b2545; font-size: 1rem; margin-bottom: 0.5rem;">Operational Takeaways</div>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.88rem; color: #334155; line-height: 1.6;">
                <li><strong>Northern (NR) & North Central (NCR):</strong> Suffer acute winter congestion where fog score exceeds 0.82–0.88 and network capacity is &gt;90%.</li>
                <li><strong>Eastern Railway (ER):</strong> Highest structural route congestion (<strong>0.95</strong>) with heavy mineral freight and suburban traffic into Howrah.</li>
                <li><strong>Southern Railway (SR):</strong> Lowest fog impact (<strong>0.02</strong>), maintaining significantly higher baseline punctuality.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(zones_table, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# 8. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem;">
    Indian Railways Operations & Punctuality Intelligence Console | Production ML Inference System<br>
    Target Definition: Train Delay &gt; 15 Minutes (Railway Board Standard)
</div>
""", unsafe_allow_html=True)
