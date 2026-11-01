"""
Indian Railways Train Delay Prediction & Network Punctuality Analytics
========================================================================
Interactive Operational Dispatch Decision Support System & Machine Learning Lab.
Engineered for Live Demonstrations, Model Audits & Streamlit Community Cloud Deployment.
Theme: Deep Dark + Elegant Gold (#080B12, #101622, #151D2B, #D4AF37, #F1D27A)
Course: ECSCI24302 – Machine Learning Essentials | Adani University
"""

import os
import io
import time
import datetime
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Project preprocessing helper functions from utils.py
from utils import clean_data_pandas, engineer_features_pandas, handle_outliers_iqr_numpy

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Indian Railways Delay Analytics | ML Lab",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. PREMIUM DEEP DARK + ELEGANT GOLD CSS SYSTEM
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Colors */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #F5F5F5;
    }

    /* Streamlit Main Background */
    .stApp {
        background-color: #080B12;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
        max-width: 95%;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #101622 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.18) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }

    /* Custom Hero Header */
    .gold-hero-header {
        background: linear-gradient(135deg, #101622 0%, #151D2B 60%, #1a2436 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 1.6rem 2.2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(212, 175, 55, 0.08);
        position: relative;
        overflow: hidden;
    }
    .gold-hero-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #D4AF37 0%, #F1D27A 50%, #D4AF37 100%);
    }
    .gold-hero-header h1 {
        color: #F5F5F5 !important;
        margin: 0 0 0.35rem 0;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .gold-hero-header p {
        color: #9CA3AF !important;
        margin: 0;
        font-size: 0.95rem;
        font-weight: 400;
        max-width: 950px;
        line-height: 1.45;
    }
    .gold-hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid rgba(212, 175, 55, 0.3);
        color: #D4AF37;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Luxury Surface Cards */
    .gold-card {
        background-color: #151D2B;
        border: 1px solid rgba(212, 175, 55, 0.22);
        border-radius: 14px;
        padding: 1.35rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .gold-card:hover {
        border-color: rgba(212, 175, 55, 0.45);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35), 0 0 10px rgba(212, 175, 55, 0.08);
    }
    .gold-card-title {
        color: #D4AF37 !important;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Metric Box */
    .metric-gold-card {
        background: #101622;
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    .metric-gold-val {
        font-size: 1.75rem;
        font-weight: 800;
        color: #D4AF37;
        font-family: 'JetBrains Mono', monospace;
        margin: 0.2rem 0;
    }
    .metric-gold-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* Preset Selection Cards */
    .preset-box {
        background: #101622;
        border: 1.5px solid rgba(212, 175, 55, 0.2);
        border-radius: 12px;
        padding: 1.0rem;
        min-height: 155px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
    }
    .preset-box:hover {
        border-color: #D4AF37;
        background: #151D2B;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.35), 0 0 12px rgba(212, 175, 55, 0.15);
    }
    .preset-box.active {
        border-color: #D4AF37;
        background: rgba(212, 175, 55, 0.08);
        box-shadow: 0 0 0 1.5px #D4AF37;
    }

    /* Status Indicator Badges */
    .badge-green {
        background: rgba(22, 163, 106, 0.15);
        border: 1px solid #16A36A;
        color: #4ade80;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
    }
    .badge-amber {
        background: rgba(233, 162, 59, 0.15);
        border: 1px solid #E9A23B;
        color: #fbbf24;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
    }
    .badge-red {
        background: rgba(220, 68, 68, 0.15);
        border: 1px solid #DC4444;
        color: #f87171;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
    }

    /* Result Dispatch Alert Banners */
    .dispatch-banner-green {
        background: linear-gradient(135deg, rgba(22, 163, 106, 0.18) 0%, rgba(16, 22, 34, 0.8) 100%);
        border: 1.5px solid #16A36A;
        border-radius: 14px;
        padding: 1.4rem;
        margin-top: 1rem;
    }
    .dispatch-banner-amber {
        background: linear-gradient(135deg, rgba(233, 162, 59, 0.18) 0%, rgba(16, 22, 34, 0.8) 100%);
        border: 1.5px solid #E9A23B;
        border-radius: 14px;
        padding: 1.4rem;
        margin-top: 1rem;
    }
    .dispatch-banner-red {
        background: linear-gradient(135deg, rgba(220, 68, 68, 0.18) 0%, rgba(16, 22, 34, 0.8) 100%);
        border: 1.5px solid #DC4444;
        border-radius: 14px;
        padding: 1.4rem;
        margin-top: 1rem;
    }

    /* Dark Input Field Overrides */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #101622 !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 8px !important;
        color: #F5F5F5 !important;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.25) !important;
    }
    input, select, textarea {
        color: #F5F5F5 !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #101622 !important;
        color: #D4AF37 !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.3rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #080B12 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #D4AF37 !important;
        color: #080B12 !important;
        border: 1.5px solid #D4AF37 !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #F1D27A !important;
        border-color: #F1D27A !important;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.45) !important;
    }

    /* Code & Monospace Elements */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: rgba(212, 175, 55, 0.1) !important;
        color: #F1D27A !important;
        border-radius: 5px;
        padding: 0.15rem 0.4rem;
        border: 1px solid rgba(212, 175, 55, 0.18);
    }

    /* Tables */
    .stDataFrame {
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #101622;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #9CA3AF;
        border: none !important;
        background-color: transparent;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #151D2B !important;
        color: #D4AF37 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. MODEL PIPELINE LOADER (CACHED, FAST SUB-15MS INFERENCE)
# -------------------------------------------------------------
ARTIFACT_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "pandas_numpy_pipeline.joblib")

@st.cache_resource(show_spinner="Loading trained LightGBM model artifact...")
def load_cached_pipeline():
    path = ARTIFACT_PATH
    if not os.path.exists(path):
        alt = os.path.join("artifacts", "pandas_numpy_pipeline.joblib")
        if os.path.exists(alt):
            path = alt
        else:
            raise FileNotFoundError(f"Pipeline artifact missing at {path}")
    return joblib.load(path)

try:
    pipeline_obj = load_cached_pipeline()
    model = pipeline_obj["model"]
    train_mean = pipeline_obj["train_mean"]
    train_std = pipeline_obj["train_std"]
    feature_columns = pipeline_obj["feature_columns"]
    cat_cols = pipeline_obj["cat_cols"]
    num_cols = pipeline_obj["num_cols"]
    iqr_bounds = pipeline_obj.get("iqr_bounds", {})
    pipeline_ready = True
except Exception as err:
    pipeline_ready = False
    pipeline_err_msg = str(err)

# -------------------------------------------------------------
# 4. DOMAIN METADATA & 16 RAILWAY ZONES DATABASE
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# 5. INFERENCE LOGIC (EXACT PIPELINE TRANSFORMATION)
# -------------------------------------------------------------
def run_model_inference(df_input: pd.DataFrame):
    """Executes the exact preprocessing sequence and model scoring."""
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
            "badge_class": "badge-red",
            "banner_class": "dispatch-banner-red",
            "color": "#DC4444",
            "action": "Urgent Operational Intervention Required: Priority junction clearance, alert Divisional Operating Manager (DOM), verify turnaround buffers, and stand by relief rake."
        }
    elif pct >= 40.0:
        return {
            "status": "MODERATE DELAY RISK",
            "alert": "AMBER ADVISORY",
            "badge_class": "badge-amber",
            "banner_class": "dispatch-banner-amber",
            "color": "#E9A23B",
            "action": "Advisory Caution: Monitor incoming rake turnaround closely at interchange halts. Prepare platform clearance ahead of peak congestion window."
        }
    else:
        return {
            "status": "ON-TIME EXPECTED",
            "alert": "GREEN NORMAL",
            "badge_class": "badge-green",
            "banner_class": "dispatch-banner-green",
            "color": "#16A36A",
            "action": "Standard Timetable Clearance: Proceed under standard divisional timetable scheduling. No emergency intervention required."
        }

# -------------------------------------------------------------
# 6. SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if "prediction_history" not in st.session_state:
    st.session_state["prediction_history"] = []
if "active_prediction" not in st.session_state:
    st.session_state["active_prediction"] = None
if "current_preset_loaded" not in st.session_state:
    st.session_state["current_preset_loaded"] = "🚅 Preset 1: Premier Vande Bharat Express (NR - Delhi to Varanasi)"

# -------------------------------------------------------------
# 7. SIDEBAR BRANDING & NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
        <span style="font-size: 1.8rem;">🚆</span>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #D4AF37; line-height: 1.2;">INDIAN RAILWAYS</div>
            <div style="font-size: 0.75rem; color: #9CA3AF; font-weight: 600;">Delay Analytics & ML Lab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if pipeline_ready:
        st.markdown("""
        <div style="background: #151D2B; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 10px; padding: 0.8rem; margin-bottom: 1.0rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.72rem; font-weight: 700; color: #9CA3AF; text-transform: uppercase;">Inference Engine</span>
                <span style="font-size: 0.68rem; font-weight: 700; color: #4ade80; background: rgba(22, 163, 106, 0.2); padding: 0.15rem 0.45rem; border-radius: 9999px;">ONLINE</span>
            </div>
            <div style="font-weight: 700; font-size: 0.92rem; color: #D4AF37; margin-top: 0.2rem;">Tuned LightGBM</div>
            <div style="font-size: 0.75rem; color: #9CA3AF;">Artifact: <code>pipeline.joblib</code> (891 KB)</div>
            <div style="font-size: 0.75rem; color: #9CA3AF;">Latency: <strong style="color:#D4AF37;">&lt; 15 ms</strong></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Engine Error: {pipeline_err_msg}")
        st.stop()

    st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #D4AF37; text-transform: uppercase; margin-bottom: 0.3rem;'>Navigation Menu</div>", unsafe_allow_html=True)
    
    app_mode = st.radio(
        "Go to Module:",
        [
            "🌟 Overview & Mission Control",
            "⚡ Train Delay Predictor",
            "📜 Prediction Audit History",
            "📈 Exploratory Data Analysis (EDA)",
            "🛠️ Data Preprocessing & Pipeline",
            "🧬 Feature Engineering & Selection",
            "🤖 Model Development & Benchmarks",
            "📊 Evaluation Metrics & Confusion Matrix",
            "🔍 Error Analysis & Misclassifications",
            "🧠 Model Interpretation (Feature Importance)",
            "📑 Batch Fleet Delay Audit",
            "🗺️ Network Punctuality & 16 Zones",
            "📋 Academic Compliance & 19-Stage Audit"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.15); margin: 1rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #151D2B; border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 10px; padding: 0.8rem; margin-bottom: 0.8rem;">
        <div style="font-size: 0.75rem; font-weight: 700; color: #D4AF37; margin-bottom: 0.4rem; text-transform: uppercase;">Dispatch Triage Rules</div>
        <div style="font-size: 0.78rem; margin-bottom: 0.25rem; display: flex; justify-content: space-between;">
            <span style="color:#4ade80;">● On-Time (Green)</span>
            <span style="font-weight:700; color:#4ade80;">&lt; 40.0%</span>
        </div>
        <div style="font-size: 0.78rem; margin-bottom: 0.25rem; display: flex; justify-content: space-between;">
            <span style="color:#fbbf24;">● Moderate Risk (Amber)</span>
            <span style="font-weight:700; color:#fbbf24;">40% – 65%</span>
        </div>
        <div style="font-size: 0.78rem; display: flex; justify-content: space-between;">
            <span style="color:#f87171;">● High Delay (Red)</span>
            <span style="font-weight:700; color:#f87171;">&gt; 65.0%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 0.72rem; color: #64748B; text-align: center; line-height: 1.4;">
        ECSCI24302 Machine Learning Essentials<br/>
        Adani University © 2026–2027
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 8. TOP HERO BANNER (PRESENT ACROSS ALL MODULES)
# -------------------------------------------------------------
st.markdown(f"""
<div class="gold-hero-header">
    <div class="gold-hero-badge">🚆 ECSCI24302 PBL ML PLATFORM  •  ACADEMIC YEAR 2026–2027</div>
    <h1>Indian Railways Train Delay Prediction & Network Punctuality Analytics</h1>
    <p>Operational Supervised Machine Learning System adhering strictly to the 19-stage Problem-Based Learning (PBL) curriculum. 
    Powered by <strong>Tuned LightGBM</strong> (85.85% Accuracy, 92.10% Recall, 0.9038 F1-Score, 0.9121 ROC-AUC) and 
    <strong>Logistic Regression</strong> (0.9229 ROC-AUC).</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MODULE 1: 🌟 OVERVIEW & MISSION CONTROL
# =============================================================================
if app_mode == "🌟 Overview & Mission Control":
    st.markdown("### 🌟 Executive Overview & Mission Control")
    
    # 4 Key Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-gold-card">
            <div class="metric-gold-label">Training Corpus</div>
            <div class="metric-gold-val">1,500,000</div>
            <div style="font-size: 0.72rem; color: #9CA3AF;">10k Stratified Sample Trained</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-gold-card">
            <div class="metric-gold-label">Champion Accuracy</div>
            <div class="metric-gold-val">85.85%</div>
            <div style="font-size: 0.72rem; color: #4ade80;">Tuned LightGBM Classifier</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-gold-card">
            <div class="metric-gold-label">Safety Recall</div>
            <div class="metric-gold-val">92.10%</div>
            <div style="font-size: 0.72rem; color: #4ade80;">1,329 of 1,443 Delays Caught</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-gold-card">
            <div class="metric-gold-label">Max ROC-AUC</div>
            <div class="metric-gold-val">0.9229</div>
            <div style="font-size: 0.72rem; color: #D4AF37;">Logistic Regression Ranking</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.1, 0.9])
    with col_l:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">📖 Project Genesis & Machine Learning Objectives</div>
            <p style="color: #F5F5F5; font-size: 0.92rem; line-height: 1.55;">
                Indian Railways operates the world's fourth-largest railway system, running over 13,000 passenger services daily. 
                Because high-speed premier trains, slow local passenger services, and freight trains share identical track sections, 
                an unexpected disruption propagates secondary delays across entire zones.
            </p>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.5;">
                This project builds an end-to-end Machine Learning pipeline that predicts <code>is_delayed</code> 
                (arrival delay &gt; 15 minutes at destination) hours prior to departure. The system is designed to provide 
                station masters and traffic controllers with proactive early warnings to prioritize track clearance and allocate platform buffers.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">⚙️ How This Decision Support System Works</div>
            <ol style="color: #9CA3AF; font-size: 0.85rem; line-height: 1.6; padding-left: 1.2rem;">
                <li><strong style="color:#D4AF37;">Input Ingestion:</strong> Ingests pre-departure timetable, route geography, infrastructure, rolling stock age, and turnaround parameters.</li>
                <li><strong style="color:#D4AF37;">Leakage Quarantine:</strong> Strictly excludes post-event variables (<code>delay_minutes</code>, <code>primary_delay_cause</code>).</li>
                <li><strong style="color:#D4AF37;">Domain Feature Synthesis:</strong> Computes 11 domain features including commercial speed, stop density, weather severity, and rake turnaround risk.</li>
                <li><strong style="color:#D4AF37;">Sub-15ms Inference:</strong> Executes vectorized scaling and generates probabilities using serialized LightGBM tree ensemble.</li>
                <li><strong style="color:#D4AF37;">Operational Triage:</strong> Flags journeys into Green (&lt;40%), Amber (40%–65%), or Red (&gt;65%) dispatch alert levels.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🛡️ Academic Integrity & Operational Scope</div>
            <div style="font-size: 0.84rem; color: #9CA3AF; line-height: 1.5;">
                <div style="margin-bottom: 0.6rem;">
                    <strong style="color:#F5F5F5;">Decision-Support Prototype:</strong> This application is an academic prototype for operational analytics; it does NOT replace official Indian Railways signaling or safety interlocks.
                </div>
                <div style="margin-bottom: 0.6rem;">
                    <strong style="color:#F5F5F5;">Dataset Source:</strong> Kaggle Indian Railways Train Delay Prediction Dataset (1.5M train records, 375k test records).
                </div>
                <div style="margin-bottom: 0.6rem;">
                    <strong style="color:#F5F5F5;">Zero Synthetic Data:</strong> All metrics, error counts, and confusion matrices reflect authentic notebook experimental outputs.
                </div>
                <div>
                    <strong style="color:#F5F5F5;">Hardware Honesty:</strong> Model training was executed on a stratified 10,000-record sample to prevent local RAM exhaustion when categorical encoding expands to 8,111 columns.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🚀 Fast Navigation Shortcuts</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15); font-size:0.8rem;">
                    <strong style="color:#D4AF37;">⚡ Predictor</strong><br>Test 1-click presets or custom journeys.
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15); font-size:0.8rem;">
                    <strong style="color:#D4AF37;">📈 EDA Dashboard</strong><br>Explore 72% imbalance & delay causes.
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15); font-size:0.8rem;">
                    <strong style="color:#D4AF37;">🤖 Model Lab</strong><br>Inspect official 7-model comparison.
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15); font-size:0.8rem;">
                    <strong style="color:#D4AF37;">📋 19-Stage Audit</strong><br>Check complete syllabus compliance.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# MODULE 2: ⚡ TRAIN DELAY PREDICTOR
# =============================================================================
elif app_mode == "⚡ Train Delay Predictor":
    st.markdown("### ⚡ Live Single-Journey Delay Predictor")
    st.caption("Select a documented operational preset or configure custom timetable parameters to compute pre-departure delay probability.")

    # 1-Click Preset Demonstration Buttons
    st.markdown("#### 🚅 Documented Operational Demonstration Scenarios")
    p_cols = st.columns(4)
    preset_names = list(DEMO_SCENARIOS.keys())

    for idx, p_name in enumerate(preset_names):
        p_data = DEMO_SCENARIOS[p_name]
        with p_cols[idx]:
            is_active = (st.session_state["current_preset_loaded"] == p_name)
            active_border = "border: 1.5px solid #D4AF37; background: rgba(212, 175, 55, 0.08);" if is_active else ""
            badge = '<span class="badge-green">ON-TIME EXPECTED</span>' if "3.3%" in p_data["tag"] or "4.0%" in p_data["tag"] else '<span class="badge-red">HIGH DELAY RISK</span>'
            
            st.markdown(f"""
            <div class="preset-box" style="{active_border}">
                <div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: #F5F5F5; margin-bottom: 0.3rem;">{p_name.split(':')[1].split('(')[0].strip()}</div>
                    <div style="font-size: 0.72rem; color: #9CA3AF; margin-bottom: 0.4rem;">{p_data['story'][:90]}...</div>
                </div>
                <div>{badge}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Load Preset #{idx+1}", key=f"btn_preset_{idx}"):
                st.session_state["current_preset_loaded"] = p_name
                st.session_state["active_prediction"] = None
                st.rerun()

    current_data = DEMO_SCENARIOS[st.session_state["current_preset_loaded"]]
    st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.15); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # Interactive Form
    st.markdown(f"#### 🛠️ Configure Parameters for: <span style='color:#D4AF37;'>{st.session_state['current_preset_loaded'].split(':')[1].strip()}</span>", unsafe_allow_html=True)

    with st.form("single_journey_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div style='font-weight:700; color:#D4AF37; font-size:0.9rem; margin-bottom:0.4rem;'>1. Schedule & Geography</div>", unsafe_allow_html=True)
            in_train_num = st.number_input("Train Number", min_value=1000, max_value=99999, value=int(current_data["train_number"]))
            
            type_idx = TRAIN_CATEGORIES.index(current_data["train_type"]) if current_data["train_type"] in TRAIN_CATEGORIES else 0
            in_train_type = st.selectbox("Train Category", TRAIN_CATEGORIES, index=type_idx)
            
            zone_keys = list(ZONE_DATABASE.keys())
            zone_idx = zone_keys.index(current_data["zone"]) if current_data["zone"] in zone_keys else 0
            in_zone = st.selectbox("Railway Zone", zone_keys, index=zone_idx)
            
            in_distance = st.number_input("Route Distance (km)", min_value=10.0, max_value=3500.0, value=float(current_data["distance_km"]), step=10.0)
            in_stops = st.number_input("Scheduled Intermediate Halts", min_value=1, max_value=60, value=int(current_data["num_scheduled_stops"]))
            in_hours = st.number_input("Scheduled Travel Hours", min_value=0.5, max_value=60.0, value=float(current_data["scheduled_travel_hours"]), step=0.5)

        with col2:
            st.markdown("<div style='font-weight:700; color:#D4AF37; font-size:0.9rem; margin-bottom:0.4rem;'>2. Infrastructure & Operations</div>", unsafe_allow_html=True)
            in_dep_hour = st.slider("Departure Hour (0–23)", min_value=0, max_value=23, value=int(current_data["departure_hour"]))
            in_season = st.selectbox("Operational Season", ["Summer", "Monsoon", "Winter/Fog", "Post-Monsoon"], index=["Summer", "Monsoon", "Winter/Fog", "Post-Monsoon"].index(current_data["season"]) if current_data["season"] in ["Summer", "Monsoon", "Winter/Fog", "Post-Monsoon"] else 0)
            
            in_track_doubled = st.selectbox("Track Infrastructure", ["Double / Quadruple Track (1)", "Single Track Bottleneck (0)"], index=0 if current_data["track_doubled"] == 1 else 1)
            in_hdn = st.selectbox("High-Density Network (HDN) Corridor", ["Yes - Trunk Line (1)", "No - Branch Section (0)"], index=0 if current_data["is_hdn_route"] == 1 else 1)
            in_traction = st.selectbox("Traction Type", ["Electric (25kV AC)", "Diesel", "Dual Traction"], index=0 if "Electric" in current_data["traction_type"] else 1)
            in_psr = st.number_input("Permanent Speed Restrictions (PSR Count)", min_value=0, max_value=20, value=int(current_data["psr_count"]))

        with col3:
            st.markdown("<div style='font-weight:700; color:#D4AF37; font-size:0.9rem; margin-bottom:0.4rem;'>3. Rolling Stock & Turnaround Buffer</div>", unsafe_allow_html=True)
            in_loco_age = st.slider("Locomotive Age (Years)", min_value=0.5, max_value=30.0, value=float(current_data["loco_age_years"]), step=0.5)
            in_coach_age = st.slider("Coach Set Age (Years)", min_value=0.5, max_value=30.0, value=float(current_data["coach_age_years"]), step=0.5)
            in_late_rake = st.selectbox("Incoming Rake Arrival Status", ["On-Time Rake Available (0)", "Late Incoming Rake (>30 min delay) (1)"], index=1 if current_data["late_incoming_rake"] == 1 else 0)
            in_shared_rake = st.selectbox("Turnaround Rake Sharing", ["Dedicated Rake (0)", "Shared Turnaround Rake (1)"], index=1 if current_data["is_rake_shared"] == 1 else 0)
            in_ontime_pct = st.slider("Route Historical Punctuality (%)", min_value=10.0, max_value=99.0, value=float(current_data["route_historical_ontime_pct"]), step=1.0)
            in_seat_util = st.slider("Passenger Seat Utilisation (%)", min_value=30.0, max_value=120.0, value=float(current_data["seat_utilisation_pct"]), step=1.0)

        submit_btn = st.form_submit_button("⚡ Compute Delay Probability & Dispatch Directive", type="primary")

    if submit_btn:
        # Construct input DataFrame
        zone_info = ZONE_DATABASE[in_zone]
        user_row = {
            "train_number": in_train_num,
            "train_type": in_train_type,
            "year": 2024,
            "month": 1 if "Winter" in in_season else (7 if "Monsoon" in in_season else 4),
            "day_of_week": 2,
            "departure_hour": in_dep_hour,
            "is_weekend": 0,
            "is_night_departure": 1 if in_dep_hour >= 22 or in_dep_hour <= 4 else 0,
            "is_peak_hour": 1 if in_dep_hour in [8, 9, 10, 17, 18, 19] else 0,
            "is_festival_season": 0,
            "season": in_season,
            "zone": in_zone,
            "zone_abbr": zone_info["abbr"],
            "source_station_category": "A1",
            "destination_station_category": "A1",
            "distance_km": in_distance,
            "num_scheduled_stops": in_stops,
            "scheduled_travel_hours": in_hours,
            "track_doubled": 1 if "Double" in in_track_doubled else 0,
            "is_hdn_route": 1 if "Yes" in in_hdn else 0,
            "traction_type": in_traction,
            "is_electrified": 1 if "Electric" in in_traction else 0,
            "psr_count": in_psr,
            "is_circular_route": 0,
            "is_monsoon_season": 1 if "Monsoon" in in_season else 0,
            "is_fog_risk": 1 if "Winter" in in_season and in_dep_hour <= 7 else 0,
            "fog_risk_score": zone_info["fog"],
            "zone_fog_index": zone_info["fog"],
            "zone_congestion_index": zone_info["congestion"],
            "season_severity_score": 0.85 if "Winter" in in_season else (0.80 if "Monsoon" in in_season else 0.30),
            "loco_age_years": in_loco_age,
            "coach_age_years": in_coach_age,
            "has_lhb_coaches": 1 if "Vande" in in_train_type or "Rajdhani" in in_train_type or in_coach_age < 10 else 0,
            "is_rake_shared": 1 if "Shared" in in_shared_rake else 0,
            "maintenance_score": 8.5 if in_coach_age < 5 else 5.5,
            "seat_utilisation_pct": in_seat_util,
            "late_incoming_rake": 1 if "Late" in in_late_rake else 0,
            "is_special_train": 0,
            "route_historical_ontime_pct": in_ontime_pct
        }

        df_single = pd.DataFrame([user_row])
        
        with st.spinner("Processing engineered features and querying Tuned LightGBM ensemble..."):
            t_start = time.time()
            probs, df_eng = run_model_inference(df_single)
            t_ms = (time.time() - t_start) * 1000.0
            
            predicted_prob = float(probs[0])
            risk_info = get_risk_classification(predicted_prob)
            
            st.session_state["active_prediction"] = {
                "prob": predicted_prob,
                "pct": predicted_prob * 100.0,
                "risk": risk_info,
                "latency_ms": t_ms,
                "train_number": in_train_num,
                "train_type": in_train_type,
                "zone": in_zone,
                "distance": in_distance,
                "avg_speed": float(df_eng["avg_speed_kmh"].iloc[0]),
                "network_vuln": float(df_eng["network_vulnerability"].iloc[0]),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Append to session history
            st.session_state["prediction_history"].append({
                "Timestamp": st.session_state["active_prediction"]["timestamp"],
                "Train No": in_train_num,
                "Train Type": in_train_type,
                "Zone": in_zone,
                "Distance (km)": in_distance,
                "Delay Prob (%)": f"{predicted_prob * 100.0:.1f}%",
                "Status": risk_info["status"],
                "Alert Tier": risk_info["alert"]
            })

    # Render Active Prediction Results
    if st.session_state["active_prediction"]:
        res = st.session_state["active_prediction"]
        risk = res["risk"]
        
        st.markdown(f"""
        <div class="{risk['banner_class']}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span class="{risk['badge_class']}">{risk['alert']}</span>
                <span style="font-size: 0.75rem; color: #9CA3AF; font-family: 'JetBrains Mono', monospace;">Inference Time: {res['latency_ms']:.2f} ms</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 1rem;">
                <div style="font-size: 2.8rem; font-weight: 800; color: {risk['color']}; font-family: 'JetBrains Mono', monospace;">
                    {res['pct']:.1f}%
                </div>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #F5F5F5;">
                        {risk['status']}
                    </div>
                    <div style="font-size: 0.85rem; color: #9CA3AF;">
                        Target Definition: Arrival delay exceeding 15 minutes at destination terminus.
                    </div>
                </div>
            </div>
            <div style="background: rgba(8, 11, 18, 0.6); border-radius: 8px; padding: 0.85rem; margin-top: 0.85rem; border-left: 3px solid {risk['color']};">
                <div style="font-size: 0.78rem; font-weight: 700; color: #D4AF37; text-transform: uppercase; margin-bottom: 0.2rem;">Divisional Dispatch Directive</div>
                <div style="font-size: 0.85rem; color: #F5F5F5; line-height: 1.45;">{risk['action']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Operational Feature Drivers Card
        st.markdown("""
        <div class="gold-card" style="margin-top: 1rem;">
            <div class="gold-card-title">🔍 Key Model Influencers for This Journey</div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; margin-top: 0.5rem;">
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
                    <div style="font-size:0.7rem; color:#9CA3AF;">Scheduled Speed</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#D4AF37;">""" + f"{res['avg_speed']:.1f} km/h" + """</div>
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
                    <div style="font-size:0.7rem; color:#9CA3AF;">Network Vulnerability</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#D4AF37;">""" + f"{res['network_vuln']:.2f}" + """</div>
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
                    <div style="font-size:0.7rem; color:#9CA3AF;">Zone Congestion</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#D4AF37;">""" + f"{ZONE_DATABASE[res['zone']]['congestion'] * 100:.0f}%" + """</div>
                </div>
                <div style="background:#101622; padding:0.6rem; border-radius:8px; border:1px solid rgba(212,175,55,0.15);">
                    <div style="font-size:0.7rem; color:#9CA3AF;">Zone Fog Index</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#D4AF37;">""" + f"{ZONE_DATABASE[res['zone']]['fog'] * 100:.0f}%" + """</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# MODULE 3: 📜 PREDICTION AUDIT HISTORY
# =============================================================================
elif app_mode == "📜 Prediction Audit History":
    st.markdown("### 📜 Session Prediction Audit History")
    st.caption("Inspect, audit, and export all delay predictions generated during this interactive session.")

    history_list = st.session_state["prediction_history"]

    if not history_list:
        st.info("ℹ️ No predictions logged yet. Go to **⚡ Train Delay Predictor** to run your first train delay inference.")
    else:
        df_hist = pd.DataFrame(history_list)
        st.dataframe(df_hist, use_container_width=True)

        col_h1, col_h2, _ = st.columns([1, 1, 2])
        with col_h1:
            csv_data = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export History as CSV",
                data=csv_data,
                file_name=f"ir_delay_prediction_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_h2:
            if st.button("🗑️ Clear Prediction History", use_container_width=True):
                st.session_state["prediction_history"] = []
                st.rerun()

# =============================================================================
# MODULE 4: 📈 EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
elif app_mode == "📈 Exploratory Data Analysis (EDA)":
    st.markdown("### 📈 Exploratory Data Analysis (EDA)")
    st.caption("Empirical distributions and domain patterns extracted directly from Notebook 1 (`01_Exploratory_Data_Analysis.ipynb`).")

    eda_tabs = st.tabs([
        "⚖️ Target Class Imbalance",
        "🚆 Train Category Gradient",
        "🗺️ Zonal Bottlenecks & Seasons",
        "🔍 Root Causes & Correlations"
    ])

    with eda_tabs[0]:
        st.markdown("#### Target Variable Class Imbalance (`is_delayed`)")
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🚨 Crucial EDA Discovery: The 72% Imbalance Trap</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                In the training dataset, <strong style="color:#D4AF37;">72.16%</strong> of journeys are delayed (&gt;15 minutes arrival delay), 
                while only <strong style="color:#4ade80;">27.84%</strong> arrive on time. 
                This demonstrates why evaluating models using Accuracy alone is dangerous: a trivial baseline predicting "delayed" every time 
                achieves 72.15% accuracy while having zero real-world predictive skill!
            </p>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists("reports/figures/eda_img_1.png"):
            st.image("reports/figures/eda_img_1.png", caption="Figure 1: Target Variable Imbalance (left) and Continuous Delay Minutes Distribution (right)", use_container_width=True)

    with eda_tabs[1]:
        st.markdown("#### Punctuality by Train Category Priority")
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🚄 Corridor Dispatch Priority Gradient</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                Premier express trains receive green-corridor priority from dispatchers, resulting in low delay rates: 
                <strong>Vande Bharat Express (~18%)</strong>, <strong>Rajdhani Express (~24%)</strong>, and <strong>Shatabdi Express (~26%)</strong>. 
                In contrast, unreserved <strong>Passenger Trains (~88%)</strong> and conventional <strong>Mail/Express (~76%)</strong> 
                suffer heavy delays because they are frequently held on loop tracks to give precedence to premier expresses.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists("reports/figures/eda_img_2.png"):
            st.image("reports/figures/eda_img_2.png", caption="Figure 2: Delay Rates Grouped by Train Category (left) and Administrative Railway Zone (right)", use_container_width=True)

    with eda_tabs[2]:
        st.markdown("#### Seasonal Disruptions & Zonal Bottlenecks")
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">❄️ Winter Fog Corridor & Monsoon Vulnerability</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                Winter experiences the highest delay severity due to dense fog across the Indo-Gangetic plains (NR, NCR, NER), 
                forcing trains to operate under cautionary speed limits (30–60 km/h). 
                Monsoon causes track waterlogging and ghat section landslides. In contrast, Southern Railway (SR) and South Western Railway (SWR) 
                maintain the highest punctuality (&lt;62% delay rate) due to favorable terrain and lower fog exposure.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists("reports/figures/eda_img_3.png"):
            st.image("reports/figures/eda_img_3.png", caption="Figure 3: Delay Rate by Season (left) and Delay Probability vs Distance (right)", use_container_width=True)

    with eda_tabs[3]:
        st.markdown("#### Primary Delay Root Causes & Numerical Correlation Heatmap")
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">⚠️ Operational Root Causes Breakdown</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                Among historical delayed journeys with diagnostic logging: <strong>Late incoming rake turnaround accounts for 38%</strong> of all delays, 
                followed by <strong>track maintenance and speed restrictions (22%)</strong>, <strong>signal & telecommunication failures (18%)</strong>, 
                and <strong>station congestion (14%)</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            if os.path.exists("reports/figures/eda_img_4.png"):
                st.image("reports/figures/eda_img_4.png", caption="Figure 4: Historical Primary Operational Delay Causes", use_container_width=True)
        with c_r2:
            if os.path.exists("reports/figures/eda_img_5.png"):
                st.image("reports/figures/eda_img_5.png", caption="Figure 5: Pearson Correlation Heatmap of Numerical Features with is_delayed", use_container_width=True)

# =============================================================================
# MODULE 5: 🛠️ DATA PREPROCESSING & PIPELINE
# =============================================================================
elif app_mode == "🛠️ Data Preprocessing & Pipeline":
    st.markdown("### 🛠️ Data Preprocessing & Target Leakage Prevention")
    st.caption("Step-by-step documentation of all data transformations executed in Notebook 2 (`02_Data_Preprocessing_and_Feature_Engineering.ipynb`).")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🚨 Target Leakage Prevention (Crucial Engineering)</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                Data leakage occurs when an algorithm is trained using features that would not exist at pre-departure dispatch time. 
                We identified two severe leakage variables in <code>ir_train.csv</code>:
            </p>
            <ul style="color: #F5F5F5; font-size: 0.85rem; line-height: 1.6;">
                <li><code>delay_minutes</code>: Continuous arrival delay duration recorded upon journey completion. Using this to predict <code>is_delayed</code> (&gt;15 min) is circular reasoning.</li>
                <li><code>primary_delay_cause</code>: Post-journey diagnostic label written by station masters after arrival.</li>
            </ul>
            <div style="background: rgba(220, 68, 68, 0.15); border-left: 3px solid #DC4444; padding: 0.6rem; border-radius: 6px; font-size: 0.82rem; color: #f87171;">
                <strong>Enforcement Action:</strong> Both features were strictly quarantined and permanently removed from matrix X before model training.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🧹 Data Hygiene & Cleaning Audits</div>
            <ul style="color: #9CA3AF; font-size: 0.85rem; line-height: 1.6;">
                <li><strong style="color:#D4AF37;">0 Missing Values:</strong> All 45 features in <code>ir_train.csv</code> are 100% complete.</li>
                <li><strong style="color:#D4AF37;">0 Duplicate Rows:</strong> Every observation represents a unique journey instance.</li>
                <li><strong style="color:#D4AF37;">Zero-Variance Removal:</strong> <code>is_overloaded</code> was constant (0) for all rows; dropped to save memory.</li>
                <li><strong style="color:#D4AF37;">Identifiers Dropped:</strong> <code>journey_id</code> and raw <code>departure_date</code> strings removed.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">✂️ NumPy IQR Outlier Winsorization</div>
            <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
                Instead of dropping rows (which loses valuable journey records), we applied Interquartile Range (IQR) Winsorization:
                <code>Upper Bound = Q3 + 1.5 x IQR</code>.
            </p>
            <ul style="color: #F5F5F5; font-size: 0.85rem; line-height: 1.6;">
                <li><code>distance_km</code>: IQR = 450 km. Capped at <strong>1,466.0 km</strong> (3,779 extreme records Winsorized).</li>
                <li><code>scheduled_travel_hours</code>: IQR = 7.55 hrs. Capped at <strong>24.9 hrs</strong> (1,473 transcontinental runs Winsorized).</li>
            </ul>
            <p style="color: #9CA3AF; font-size: 0.82rem;">
                This stabilizes linear gradients while keeping all training instances intact.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">📐 Stratified Splitting & Z-Score Scaling</div>
            <ul style="color: #9CA3AF; font-size: 0.85rem; line-height: 1.6;">
                <li><strong style="color:#D4AF37;">Stratified 80:20 Split:</strong> 8,000 train & 2,000 validation records preserving exact 72.16% class ratio (seed 42).</li>
                <li><strong style="color:#D4AF37;">Strict Column Alignment:</strong> One-hot encoding creates 8,111 sparse columns aligned via <code>reindex(fill_value=0)</code>.</li>
                <li><strong style="color:#D4AF37;">Leakage-Free Scaling:</strong> Continuous features standardized via <code>z = (x - mean_train) / std_train</code>. Means and standard deviations were computed strictly on the training partition.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# MODULE 6: 🧬 FEATURE ENGINEERING & SELECTION
# =============================================================================
elif app_mode == "🧬 Feature Engineering & Selection":
    st.markdown("### 🧬 Domain Feature Engineering (11 Engineered Features)")
    st.caption("Detailed mathematical formulations and operational motivations for all 11 features created in `utils.py`.")

    eng_cards = [
        ("1. avg_speed_kmh", "distance_km / scheduled_travel_hours", "Commercial scheduled speed. Unrealistic speeds on congested routes indicate severe delay risk.", "#1 Predictor (570 splits)"),
        ("2. stops_density", "num_scheduled_stops / (distance_km / 100.0 + 0.1)", "Halt frequency per 100 km. Every deceleration and acceleration amplifies dwell variance.", "Captures suburban/express friction"),
        ("3. avg_stop_distance", "distance_km / (num_scheduled_stops + 1.0)", "Average distance between halts. Separates long non-stop express runs from short hops.", "Discriminates service types"),
        ("4. composite_weather_severity", "severity_score x (1 + 0.5*monsoon + 0.8*fog)", "Blends seasonal baseline with active winter fog and heavy monsoon weather alerts.", "Top 10 Feature (132 splits)"),
        ("5. historical_delay_risk", "(100.0 - route_historical_ontime_pct) / 100.0", "Inverts route historical punctuality into a normalized risk probability [0 to 1].", "Top 15 Feature (86 splits)"),
        ("6. network_vulnerability", "congestion_index x (1 + 0.5*is_hdn_route - 0.3*doubled)", "Quantifies trunk corridor exposure weighted by junction congestion and track bottlenecks.", "#2 Predictor (309 splits)"),
        ("7. rake_turnaround_risk", "incoming_rake_delay_min / (turnaround_time_available + 1)", "Measures buffer deficit when an incoming rake arrives late and eats maintenance time.", "Direct cascade delay driver"),
        ("8. equipment_age_index", "0.6 * loco_age_years + 0.4 * coach_age_years", "Weighted rolling stock age. Older rakes experience traction faults and brake binding.", "#4 Predictor (221 splits)"),
        ("9. congestion_delay_ratio", "zone_congestion_index / (avg_speed_kmh + 1.0)", "Identifies structural operational traps where high congestion meets slow speed limits.", "Captures bottleneck stress"),
        ("10-11. dep_hour_sin / cos", "sin/cos(2 * pi * departure_hour / 24.0)", "Trigonometric cyclical encoding ensuring 11 PM (23:00) and midnight (00:00) are mathematically adjacent.", "Preserves 24h daily cycles")
    ]

    for name, formula, desc, impact in eng_cards:
        st.markdown(f"""
        <div class="gold-card" style="padding: 1.0rem 1.35rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-weight: 700; color: #D4AF37; font-size: 0.95rem;">{name}</span>
                <span style="font-size: 0.72rem; color: #4ade80; background: rgba(22, 163, 106, 0.15); border: 1px solid #16A36A; padding: 0.15rem 0.5rem; border-radius: 6px; font-weight: 600;">{impact}</span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #F1D27A; background: rgba(212, 175, 55, 0.08); padding: 0.35rem 0.65rem; border-radius: 6px; margin-bottom: 0.4rem;">
                {formula}
            </div>
            <div style="font-size: 0.82rem; color: #9CA3AF; line-height: 1.4;">
                {desc}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if os.path.exists("reports/figures/prep_img_1.png"):
        st.image("reports/figures/prep_img_1.png", caption="Figure 6: Pearson Correlation Matrix of Engineered Features with Target Variable (is_delayed)", use_container_width=True)

# =============================================================================
# MODULE 7: 🤖 MODEL DEVELOPMENT & BENCHMARKS
# =============================================================================
elif app_mode == "🤖 Model Development & Benchmarks":
    st.markdown("### 🤖 Supervised Algorithms & Official Model Comparison")
    st.caption("Official Model Comparison Table conforming to Section 14 of `MLE_PBL_Project_Instructions.pdf`.")

    comp_data = [
        {"Model": "Baseline (Dummy)", "Best Hyperparameters": "strategy='most_frequent'", "Accuracy": "0.7215", "Precision": "0.7215", "Recall": "1.0000", "F1-Score": "0.8382", "ROC-AUC": "0.5000", "Role": "Trivial majority baseline. Zero discriminatory skill."},
        {"Model": "Logistic Regression", "Best Hyperparameters": "C=1.0, penalty='l2', max_iter=500", "Accuracy": "0.8570", "Precision": "0.8901", "Recall": "0.9148", "F1-Score": "0.9023", "ROC-AUC": "0.9229", "Role": "Highest ROC-AUC ranking power. Fast convergence."},
        {"Model": "Decision Tree", "Best Hyperparameters": "max_depth=10, min_samples_leaf=20", "Accuracy": "0.8130", "Precision": "0.8585", "Recall": "0.8870", "F1-Score": "0.8725", "ROC-AUC": "0.8593", "Role": "Non-linear Gini threshold splits; prone to variance."},
        {"Model": "Random Forest (Default)", "Best Hyperparameters": "n_estimators=100, max_depth=None", "Accuracy": "0.7730", "Precision": "0.7640", "Recall": "0.9917", "F1-Score": "0.8631", "ROC-AUC": "0.8831", "Role": "Bagged ensemble; high recall but excessive false alarms."},
        {"Model": "LightGBM (Default)", "Best Hyperparameters": "n_estimators=100, lr=0.1, leaves=31", "Accuracy": "0.8560", "Precision": "0.8889", "Recall": "0.9148", "F1-Score": "0.9016", "ROC-AUC": "0.9152", "Role": "Fast gradient boosted tree baseline."},
        {"Model": "Random Forest (Tuned)", "Best Hyperparameters": "n_estimators=80, max_depth=16, split=5", "Accuracy": "0.7870", "Precision": "0.7783", "Recall": "0.9854", "F1-Score": "0.8697", "ROC-AUC": "0.8854", "Role": "Tuned via 2-fold CV (CV AUC = 0.8826)."},
        {"Model": "Tuned LightGBM ★", "Best Hyperparameters": "lr=0.05, num_leaves=63, max_depth=6", "Accuracy": "0.8585", "Precision": "0.8872", "Recall": "0.9210", "F1-Score": "0.9038", "ROC-AUC": "0.9121", "Role": "CHAMPION OPERATIONAL MODEL. Highest Accuracy, Recall & F1."}
    ]
    df_comp = pd.DataFrame(comp_data)
    st.dataframe(df_comp, use_container_width=True)

    st.markdown("""
    <div class="gold-card" style="margin-top: 1rem;">
        <div class="gold-card-title">🏆 Champion Model Selection Rationale</div>
        <p style="color: #F5F5F5; font-size: 0.9rem; line-height: 1.55;">
            <strong>Tuned LightGBM was selected as the operational champion model</strong> because it achieves the best balance 
            between operational safety (<strong style="color:#4ade80;">92.10% Recall</strong> catches 92% of all delayed journeys) 
            and operational efficiency (<strong style="color:#D4AF37;">88.72% Precision</strong> minimizes false alarms). 
            While Logistic Regression achieved a slightly higher ROC-AUC (0.9229), Tuned LightGBM delivered higher overall Accuracy 
            (85.85% vs 85.70%) and superior F1-score (0.9038 vs 0.9023), capturing complex non-linear interactions between weather severity 
            and high-density network corridors.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Plot metric comparison
    fig_comp, ax_comp = plt.subplots(figsize=(10, 4.2), dpi=150)
    fig_comp.patch.set_facecolor('#101622')
    ax_comp.set_facecolor('#151D2B')
    
    models_plot = ["Baseline", "Logistic Reg", "Decision Tree", "Random Forest", "LightGBM (Tuned)"]
    acc_vals = [72.15, 85.70, 81.30, 78.70, 85.85]
    rec_vals = [100.0, 91.48, 88.70, 98.54, 92.10]
    f1_vals = [83.82, 90.23, 87.25, 86.97, 90.38]
    
    x = np.arange(len(models_plot))
    width = 0.25
    
    ax_comp.bar(x - width, acc_vals, width, label='Accuracy (%)', color='#D4AF37')
    ax_comp.bar(x, rec_vals, width, label='Recall (%)', color='#4ade80')
    ax_comp.bar(x + width, f1_vals, width, label='F1-Score (%)', color='#60a5fa')
    
    ax_comp.set_ylabel('Percentage (%)', color='#9CA3AF', fontsize=10)
    ax_comp.set_title('Validation Performance Comparison Across Algorithm Families', color='#D4AF37', fontsize=12, fontweight='bold', pad=12)
    ax_comp.set_xticks(x)
    ax_comp.set_xticklabels(models_plot, color='#F5F5F5', fontsize=9.5)
    ax_comp.tick_params(colors='#9CA3AF')
    ax_comp.set_ylim(60, 105)
    ax_comp.grid(axis='y', linestyle='--', alpha=0.15, color='#CBD5E1')
    ax_comp.legend(facecolor='#101622', edgecolor=(212/255, 175/255, 55/255, 0.3), labelcolor='#F5F5F5', fontsize=8.5)
    
    for spine in ax_comp.spines.values():
        spine.set_color((212/255, 175/255, 55/255, 0.2))
        
    plt.tight_layout()
    st.pyplot(fig_comp)
    plt.close()

# =============================================================================
# MODULE 8: 📊 EVALUATION METRICS & CONFUSION MATRIX
# =============================================================================
elif app_mode == "📊 Evaluation Metrics & Confusion Matrix":
    st.markdown("### 📊 Comprehensive Evaluation Metrics & Confusion Matrix")
    st.caption("Quantitative audit of Tuned LightGBM on the 2,000 validation records.")

    col_m1, col_m2 = st.columns([1.1, 0.9])
    with col_m1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🎯 Confusion Matrix Breakdown (n = 2,000)</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.6rem;">
                <div style="background:#101622; border-left:3px solid #16A36A; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.72rem; color:#9CA3AF;">True Negatives (TN)</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#4ade80;">388</div>
                    <div style="font-size:0.72rem; color:#9CA3AF;">69.66% of on-time trains correctly cleared</div>
                </div>
                <div style="background:#101622; border-left:3px solid #E9A23B; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.72rem; color:#9CA3AF;">False Positives (FP)</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#fbbf24;">169</div>
                    <div style="font-size:0.72rem; color:#9CA3AF;">False alarms (30.34% of on-time trains)</div>
                </div>
                <div style="background:#101622; border-left:3px solid #DC4444; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.72rem; color:#9CA3AF;">False Negatives (FN)</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#f87171;">114</div>
                    <div style="font-size:0.72rem; color:#9CA3AF;">Missed delays (7.90% of delayed trains)</div>
                </div>
                <div style="background:#101622; border-left:3px solid #16A36A; padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.72rem; color:#9CA3AF;">True Positives (TP)</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#4ade80;">1,329</div>
                    <div style="font-size:0.72rem; color:#9CA3AF;">92.10% of delayed trains correctly caught</div>
                </div>
            </div>
            <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #D4AF37;">
                Total Correct Predictions = 1,329 + 388 = <strong>1,717 / 2,000 (85.85% Accuracy)</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">📚 Plain English Metric Explanations</div>
            <div style="font-size: 0.82rem; color: #9CA3AF; line-height: 1.5;">
                <p><strong style="color:#D4AF37;">Accuracy (85.85%):</strong> Overall percentage of correct predictions. Misleading if evaluated alone due to 72% delay imbalance.</p>
                <p><strong style="color:#D4AF37;">Precision (88.72%):</strong> When the model predicts a delay, it is right 88.7% of the time. Protects controllers from alarm fatigue.</p>
                <p><strong style="color:#D4AF37;">Recall (92.10%):</strong> Out of all actual delayed journeys, the model flags 92.1%. Vital for network punctuality safety.</p>
                <p><strong style="color:#D4AF37;">ROC-AUC (0.9121):</strong> Threshold-independent ranking capacity. 0.50 is random guessing; 0.9121 proves elite discrimination.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if os.path.exists("reports/figures/model_img_1.png"):
        st.image("reports/figures/model_img_1.png", caption="Figure 8: Receiver Operating Characteristic (ROC) Comparison and Champion Confusion Matrix", use_container_width=True)

# =============================================================================
# MODULE 9: 🔍 ERROR ANALYSIS & MISCLASSIFICATIONS
# =============================================================================
elif app_mode == "🔍 Error Analysis & Misclassifications":
    st.markdown("### 🔍 Error Analysis & Misclassifications Audit")
    st.caption("Granular diagnosis of where and why the model makes mistakes (Section 12 of PBL instructions).")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🔴 False Negatives (Missed Delays, n = 114)</div>
            <div style="font-size: 0.85rem; color: #F5F5F5; line-height: 1.55;">
                <p>A False Negative occurs when a train was predicted to arrive on time, but actually suffered a delay exceeding 15 minutes.</p>
                <strong style="color:#D4AF37;">Operational Risk:</strong> This is the most dangerous error in railway operations. Dispatchers do not reserve secondary platforms, leading to unexpected station blockages.
                <div style="margin-top: 0.6rem; color: #9CA3AF;">
                    <strong>Root Causes Identified in Error Audit:</strong>
                    <ul style="margin-top: 0.3rem;">
                        <li>Sudden local convective thunderstorms not reflected in seasonal indices.</li>
                        <li>Unforeseen en-route locomotive electrical traction failures.</li>
                        <li>Emergency cautionary speed orders imposed by permanent-way maintenance crews mid-journey.</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_e2:
        st.markdown("""
        <div class="gold-card">
            <div class="gold-card-title">🟡 False Positives (False Alarms, n = 169)</div>
            <div style="font-size: 0.85rem; color: #F5F5F5; line-height: 1.55;">
                <p>A False Positive occurs when an on-time train is incorrectly flagged as high delay risk.</p>
                <strong style="color:#D4AF37;">Operational Impact:</strong> Dispatchers may allocate unnecessary contingency buffers or hold other trains unnecessarily.
                <div style="margin-top: 0.6rem; color: #9CA3AF;">
                    <strong>Root Causes Identified in Error Audit:</strong>
                    <ul style="margin-top: 0.3rem;">
                        <li>Concentrated in Northern Railway (NR) and North Central Railway (NCR) trunk lines.</li>
                        <li>The model sees 90% zone congestion and high fog risk, predicting delay; however, skilled loco pilots and aggressive dispatch clearance occasionally allow trains to recover lost running time.</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if os.path.exists("reports/figures/model_img_2.png"):
        st.image("reports/figures/model_img_2.png", caption="Figure 9: Validation Error Breakdown Across Railway Zones and Train Categories", use_container_width=True)

# =============================================================================
# MODULE 10: 🧠 MODEL INTERPRETATION (FEATURE IMPORTANCE)
# =============================================================================
elif app_mode == "🧠 Model Interpretation (Feature Importance)":
    st.markdown("### 🧠 Model Interpretation & Feature Importance")
    st.caption("Split-based feature importance extracted directly from the trained LightGBM model artifact (`pandas_numpy_pipeline.joblib`).")

    top_feats_data = [
        {"Rank": 1, "Feature": "avg_speed_kmh (Engineered)", "Split Importance": 570, "Category": "Kinematic", "Role": "Highest discriminator of achievable timetable."},
        {"Rank": 2, "Feature": "network_vulnerability (Engineered)", "Split Importance": 309, "Category": "Infrastructure", "Role": "Corridor congestion x HDN trunk exposure."},
        {"Rank": 3, "Feature": "route_historical_ontime_pct", "Split Importance": 307, "Category": "Operational History", "Role": "Long-term route punctuality reputation."},
        {"Rank": 4, "Feature": "equipment_age_index (Engineered)", "Split Importance": 221, "Category": "Rolling Stock", "Role": "Composite loco and coach wear index."},
        {"Rank": 5, "Feature": "late_incoming_rake", "Split Importance": 220, "Category": "Turnaround", "Role": "Primary trigger of cascading secondary delays."},
        {"Rank": 6, "Feature": "loco_age_years", "Split Importance": 219, "Category": "Locomotive", "Role": "Mechanical reliability & traction motor failures."},
        {"Rank": 7, "Feature": "zone_congestion_index", "Split Importance": 169, "Category": "Network Load", "Role": "Baseline line utilization density."},
        {"Rank": 8, "Feature": "seat_utilisation_pct", "Split Importance": 154, "Category": "Passenger Load", "Role": "Station dwell time variance driver."},
        {"Rank": 9, "Feature": "composite_weather_severity (Engineered)", "Split Importance": 132, "Category": "Atmospheric", "Role": "Seasonal severity x monsoon x fog risk."},
        {"Rank": 10, "Feature": "season_severity_score", "Split Importance": 132, "Category": "Seasonal", "Role": "Baseline regional climate friction."},
        {"Rank": 11, "Feature": "maintenance_score", "Split Importance": 120, "Category": "Depot Quality", "Role": "Rolling stock inspection thoroughness."},
        {"Rank": 12, "Feature": "track_doubled", "Split Importance": 113, "Category": "Infrastructure", "Role": "Single-track meets vs continuous passing."},
        {"Rank": 13, "Feature": "scheduled_travel_hours", "Split Importance": 104, "Category": "Timetable", "Role": "Duration of operational exposure."},
        {"Rank": 14, "Feature": "coach_age_years", "Split Importance": 100, "Category": "Coaches", "Role": "Brake binding & AC generator reliability."},
        {"Rank": 15, "Feature": "historical_delay_risk (Engineered)", "Split Importance": 86, "Category": "Statistical Risk", "Role": "Inverted route punctuality probability."}
    ]
    df_top_feats = pd.DataFrame(top_feats_data)
    st.dataframe(df_top_feats, use_container_width=True)

    st.markdown("""
    <div class="gold-card" style="margin-top: 1rem;">
        <div class="gold-card-title">💡 Domain Validation of Model Decision Rules</div>
        <p style="color: #9CA3AF; font-size: 0.88rem; line-height: 1.55;">
            Crucially, <strong style="color:#D4AF37;">5 of the top 15 features are our engineered domain features</strong>. 
            The single most influential predictor is <code>avg_speed_kmh</code> (570 splits). 
            This confirms railway operational theory: if a timetable demands an average commercial speed that exceeds 
            what track conditions and signaling allow, the journey will almost certainly incur a destination delay.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists("reports/figures/model_img_3.png"):
        st.image("reports/figures/model_img_3.png", caption="Figure 10: Top 15 Split Importances in Champion Tuned LightGBM", use_container_width=True)

# =============================================================================
# MODULE 11: 📑 BATCH FLEET DELAY AUDIT
# =============================================================================
elif app_mode == "📑 Batch Fleet Delay Audit":
    st.markdown("### 📑 Operational Batch Fleet Delay Audit")
    st.caption("Audit entire train fleets simultaneously using our cached LightGBM vectorized pipeline.")

    # Generate benchmark 10-train fleet
    fleet_rows = []
    base_presets = list(DEMO_SCENARIOS.values())
    for i in range(10):
        bp = base_presets[i % len(base_presets)].copy()
        bp["train_number"] = 12000 + i * 153
        if i % 2 == 0:
            bp["distance_km"] = bp["distance_km"] + (i * 35)
            bp["scheduled_travel_hours"] = bp["scheduled_travel_hours"] + (i * 0.4)
        fleet_rows.append(bp)
    
    df_fleet_benchmark = pd.DataFrame(fleet_rows)

    st.markdown("#### 🚆 Built-In Benchmark Fleet (10 Express Services)")
    st.dataframe(df_fleet_benchmark[["train_number", "train_type", "zone", "distance_km", "scheduled_travel_hours", "season"]], use_container_width=True)

    if st.button("⚡ Execute Batch Delay Audit for Benchmark Fleet", type="primary"):
        with st.spinner("Processing batch feature engineering and vectorized scoring..."):
            probs_batch, _ = run_model_inference(df_fleet_benchmark)
            
            results_fleet = df_fleet_benchmark[["train_number", "train_type", "zone", "distance_km"]].copy()
            results_fleet["Delay Probability (%)"] = [f"{p*100:.1f}%" for p in probs_batch]
            results_fleet["Operational Status"] = [get_risk_classification(p)["status"] for p in probs_batch]
            results_fleet["Alert Level"] = [get_risk_classification(p)["alert"] for p in probs_batch]
            
            st.markdown("#### 📊 Audit Results Summary")
            st.dataframe(results_fleet, use_container_width=True)

            csv_fleet = results_fleet.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Fleet Audit Report (CSV)",
                data=csv_fleet,
                file_name="fleet_delay_audit_results.csv",
                mime="text/csv"
            )

# =============================================================================
# MODULE 12: 🗺️ NETWORK PUNCTUALITY & 16 ZONES
# =============================================================================
elif app_mode == "🗺️ Network Punctuality & 16 Zones":
    st.markdown("### 🗺️ Network Punctuality & 16 Indian Railways Zones Database")
    st.caption("Interactive operational risk and winter fog database across all 16 Indian Railways administrative zones.")

    zone_records = []
    for z_name, z_d in ZONE_DATABASE.items():
        zone_records.append({
            "Railway Zone": z_name,
            "Code": z_d["abbr"],
            "Headquarters": z_d["hq"],
            "Congestion Index": f"{z_d['congestion']*100:.0f}%",
            "Winter Fog Index": f"{z_d['fog']*100:.0f}%",
            "Operational Profile": z_d["desc"]
        })
    df_zones = pd.DataFrame(zone_records)
    st.dataframe(df_zones, use_container_width=True)

    # Plot congestion vs fog scatter
    fig_z, ax_z = plt.subplots(figsize=(10, 4.5), dpi=150)
    fig_z.patch.set_facecolor('#101622')
    ax_z.set_facecolor('#151D2B')

    x_cong = [z["congestion"] * 100 for z in ZONE_DATABASE.values()]
    y_fog = [z["fog"] * 100 for z in ZONE_DATABASE.values()]
    labels = [z["abbr"] for z in ZONE_DATABASE.values()]

    ax_z.scatter(x_cong, y_fog, color='#D4AF37', s=120, edgecolors='#F1D27A', alpha=0.85, zorder=3)
    for i, txt in enumerate(labels):
        ax_z.annotate(txt, (x_cong[i] + 0.6, y_fog[i] + 1.2), color='#F5F5F5', fontsize=8.5, fontweight='bold')

    ax_z.set_xlabel('Zone Track Congestion Index (%)', color='#9CA3AF', fontsize=10)
    ax_z.set_ylabel('Winter Fog Vulnerability (%)', color='#9CA3AF', fontsize=10)
    ax_z.set_title('Zonal Risk Matrix: Congestion vs Winter Fog Friction Across 16 IR Zones', color='#D4AF37', fontsize=11, fontweight='bold', pad=12)
    ax_z.tick_params(colors='#9CA3AF')
    ax_z.grid(True, linestyle='--', alpha=0.15, color='#CBD5E1')
    
    for spine in ax_z.spines.values():
        spine.set_color((212/255, 175/255, 55/255, 0.2))
        
    plt.tight_layout()
    st.pyplot(fig_z)
    plt.close()

# =============================================================================
# MODULE 13: 📋 ACADEMIC COMPLIANCE & 19-STAGE AUDIT
# =============================================================================
elif app_mode == "📋 Academic Compliance & 19-Stage Audit":
    st.markdown("### 📋 Academic Compliance & 19-Stage PBL Checklist")
    st.caption("Formal compliance checklist against all syllabus instructions in `MLE_PBL_Project_Instructions.pdf`.")

    stages = [
        ("1. Problem Definition", "Binary classification: is_delayed (>15 min destination delay).", "100% COMPLETE"),
        ("2. Dataset Acquisition", "Kaggle Indian Railways dataset: ir_train (1.5M), ir_test (375k).", "100% COMPLETE"),
        ("3. Dataset Understanding", "45 columns profiled: journey ID, timings, weather, rolling stock.", "100% COMPLETE"),
        ("4. Data Quality Check", "0 nulls, 0 duplicate rows/keys. Dropped is_overloaded (constant).", "100% COMPLETE"),
        ("5. Exploratory Data Analysis", "Target imbalance (72%), priority gradient, winter fog, root causes.", "100% COMPLETE"),
        ("6. Data Preprocessing", "Leakage quarantine (delay_minutes), IQR Winsorization, scaling.", "100% COMPLETE"),
        ("7. Feature Engineering", "11 domain features created: speed, stops density, weather severity, etc.", "100% COMPLETE"),
        ("8. Feature Selection", "Correlation evaluation and feature importance verification.", "100% COMPLETE"),
        ("9. Train-Test Split", "Stratified 80:20 split (8k train, 2k val) preserving 72.16% ratio.", "100% COMPLETE"),
        ("10. Baseline Model", "Dummy Classifier: 72.15% accuracy, 0.50 AUC (majority baseline).", "100% COMPLETE"),
        ("11. Model Selection", "Logistic Reg, Decision Tree, Random Forest, LightGBM evaluated.", "100% COMPLETE"),
        ("12. Model Training", "Trained on preprocessed matrix (8,111 sparse columns).", "100% COMPLETE"),
        ("13. Hyperparameter Tuning", "RandomizedSearchCV with 2-fold CV on Random Forest & LightGBM.", "100% COMPLETE"),
        ("14. Model Evaluation", "Accuracy (85.85%), Precision (88.72%), Recall (92.10%), F1, ROC-AUC.", "100% COMPLETE"),
        ("15. Model Comparison", "Official comparison table conforming to Section 14 college template.", "100% COMPLETE"),
        ("16. Error Analysis", "False Positives vs False Negatives by Zone and Train Type.", "100% COMPLETE"),
        ("17. Interpretation", "Top 15 Feature Importances chart; avg_speed_kmh ranked #1.", "100% COMPLETE"),
        ("18. Demonstration / Prediction", "Streamlit triage dashboard & 375,000 competition test inferences.", "100% COMPLETE"),
        ("19. Conclusion & Limitations", "Full report, presentation, viva defense guide, and cloud roadmap.", "100% COMPLETE")
    ]
    df_stages = pd.DataFrame(stages, columns=["Stage", "Implementation Details", "Audit Status"])
    st.dataframe(df_stages, use_container_width=True)

    st.markdown("""
    <div class="gold-card" style="margin-top: 1rem;">
        <div class="gold-card-title">👥 Academic Evaluation Details</div>
        <div style="font-size: 0.85rem; color: #9CA3AF; line-height: 1.6;">
            <div><strong>Course:</strong> ECSCI24302 – Machine Learning Essentials</div>
            <div><strong>Institution:</strong> Faculty of Engineering and Technology, Adani University</div>
            <div><strong>Academic Year:</strong> 2026–2027 | Submission Date: November 2026</div>
            <div><strong>Deliverables Produced:</strong> Word Report (DOCX), Report (PDF), Slides (PPTX), Slides (PDF), Viva Guide (MD)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
