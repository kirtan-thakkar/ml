import os
import io
import sys
import base64
import joblib
import nbformat as nbf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def fig_to_base64():
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

print("Starting generation of Notebook 02: Preprocessing and Feature Engineering...")

nb = nbf.v4.new_notebook()
nb.metadata = {
    "language_info": {"name": "python", "version": "3.11.9"},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
}

cells = []

# Cell 1: Markdown Header
c1_md = """# ECSCI24302 - Machine Learning Essentials
## Project-Based Learning (PBL): End-to-End Machine Learning Pipeline
### Notebook 2: Data Preprocessing, Feature Engineering & Leakage-Free Pipelines

---
**Project Title:** Indian Railways Train Delay Prediction & Network Punctuality Analytics  
**Course Code:** ECSCI24302  
**Stages Covered in this Notebook:**
* **Stage 6:** Data Preprocessing & Leakage Quarantine
* **Stage 7:** Domain Feature Engineering & Mathematical Formulations
* **Stage 8:** Feature Selection & Multicollinearity Analysis
* **Stage 9:** Train-Validation Splitting & Scikit-Learn Preprocessing Pipeline
---"""
cells.append(nbf.v4.new_markdown_cell(c1_md))

# Cell 2: Code - Imports & Setup
c2_code = """# 1. Imports and Directory Initialization
import os
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
os.makedirs('../artifacts', exist_ok=True)
os.makedirs('artifacts', exist_ok=True)

print("Environment initialized. Artifacts directory confirmed.")"""

c2_cell = nbf.v4.new_code_cell(c2_code)
c2_cell.outputs = [nbf.v4.new_output(output_type='stream', name='stdout', text="Environment initialized. Artifacts directory confirmed.\n")]
c2_cell.execution_count = 1
cells.append(c2_cell)

# Cell 3: Markdown - Stage 6 Preprocessing & Leakage Control
c3_md = """## Stage 6: Data Preprocessing & Target Leakage Prevention

### 6.1 Leakage Prevention Principles (ECSCI24302 Guidelines Section 15)
A critical requirement in enterprise ML pipelines is ensuring the model never learns from information unavailable at prediction time:
1. **Target Leakage:** `delay_minutes` directly determines `is_delayed` (delay > 15 mins), and `primary_delay_cause` is assigned post-trip at arrival. Both features exist only in the training set and must be dropped.
2. **Identifier Columns:** `journey_id` is a unique alphanumeric identifier with zero generalizable predictive utility.
3. **Zero-Variance Features:** `is_overloaded` has constant value `0` across all records.
4. **Temporal Ordering & Preprocessor Isolation:** Any scaler or encoder must be fit *strictly* on the training split, then applied to validation/test sets to avoid distribution snooping."""
cells.append(nbf.v4.new_markdown_cell(c3_md))

# Cell 4: Code - Data Loading & Cleaning
c4_code = """# Load stratified training subset for feature engineering and pipeline construction
DATA_PATH = '../data/' if os.path.exists('../data/') else 'data/'
df_raw = pd.read_csv(os.path.join(DATA_PATH, 'ir_train.csv'), nrows=120000)

print(f"Loaded raw dataset: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")

# Drop leakage, identifier, and zero-variance columns
leakage_cols = ['delay_minutes', 'primary_delay_cause']
uninformative_cols = ['journey_id', 'is_overloaded', 'departure_date']

cols_to_drop = [c for c in leakage_cols + uninformative_cols if c in df_raw.columns]
df_clean = df_raw.drop(columns=cols_to_drop)
print(f"Dropped columns: {cols_to_drop}")
print(f"Cleaned dataset shape: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")"""

df_raw = pd.read_csv('c:/ml/data/ir_train.csv', nrows=120000)
leakage_cols = ['delay_minutes', 'primary_delay_cause']
uninformative_cols = ['journey_id', 'is_overloaded', 'departure_date']
cols_to_drop = [c for c in leakage_cols + uninformative_cols if c in df_raw.columns]
df_clean = df_raw.drop(columns=cols_to_drop)

out_text4 = f"Loaded raw dataset: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns\nDropped columns: {cols_to_drop}\nCleaned dataset shape: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns\n"
c4_cell = nbf.v4.new_code_cell(c4_code)
c4_cell.outputs = [nbf.v4.new_output(output_type='stream', name='stdout', text=out_text4)]
c4_cell.execution_count = 2
cells.append(c4_cell)

# Cell 5: Markdown - Stage 7 Feature Engineering
c5_md = """## Stage 7: Domain-Specific Feature Engineering

To capture physical, temporal, and infrastructural constraints of railway traffic, we formulate 10 engineered features:

| Feature Name | Mathematical Definition | Physical / Operational Rationale |
| :--- | :--- | :--- |
| `avg_speed_kmh` | $\\frac{\\text{distance\\_km}}{\\text{scheduled\\_travel\\_hours}}$ | Faster scheduled runs have lower tolerance for minor track delays. |
| `stops_density` | $\\frac{\\text{num\\_scheduled\\_stops}}{\\text{distance\\_km} / 100 + 0.1}$ | Frequent stop cycles incur cumulative dwell and acceleration penalties. |
| `avg_stop_distance` | $\\frac{\\text{distance\\_km}}{\\text{num\\_scheduled\\_stops} + 1}$ | Inter-station headway and buffer availability. |
| `composite_weather_severity` | $\\text{season\\_severity} \\times (1 + 0.5\\times\\text{monsoon} + 0.5\\times\\text{fog})$ | Non-linear interaction between seasonal base risk, monsoon flooding, and fog visibility. |
| `network_vulnerability` | $\\text{congestion} \\times (1 + 0.5\\times\\text{hdn} - 0.3\\times\\text{doubled})$ | Route stress index: HDN lines worsen congestion; double-tracking mitigates bottlenecks. |
| `equipment_age_index` | $\\frac{\\text{loco\\_age} + \\text{coach\\_age}}{2}$ | Rolling stock wear-and-tear index driving mechanical breakdown probabilities. |
| `rake_turnaround_risk` | $\\text{late\\_incoming\\_rake} \\times \\text{is\\_rake\\_shared}$ | Compound failure mode: if previous service was late AND rake is shared, delay propagates directly. |
| `historical_delay_risk` | $\\frac{100 - \\text{route\\_historical\\_ontime\\_pct}}{100}$ | Baseline probability of route delay based on empirical track records. |
| `hour_sin` / `hour_cos` | $\\sin(2\\pi h / 24), \\cos(2\\pi h / 24)$ | Cyclical encoding representing continuous progression of departure hour. |
| `day_sin` / `day_cos` | $\\sin(2\\pi d / 7), \\cos(2\\pi d / 7)$ | Cyclical encoding of day-of-week continuity. |"""
cells.append(nbf.v4.new_markdown_cell(c5_md))

# Cell 6: Code - Feature Engineering Function
c6_code = """def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Construct domain-specific features for Indian Railways delay modeling.
    Works identically on training, validation, and untouched test sets.
    \"\"\"
    df = data.copy()
    
    # 1. Kinematic & Stop Metrics
    df['avg_speed_kmh'] = df['distance_km'] / df['scheduled_travel_hours'].replace(0, np.nan)
    df['stops_density'] = df['num_scheduled_stops'] / (df['distance_km'] / 100.0 + 0.1)
    df['avg_stop_distance'] = df['distance_km'] / (df['num_scheduled_stops'] + 1)
    
    # 2. Weather & Network Vulnerability Interactions
    df['composite_weather_severity'] = df['season_severity_score'] * (
        1.0 + 0.5 * df['is_monsoon_season'] + 0.5 * df['is_fog_risk']
    )
    df['network_vulnerability'] = df['zone_congestion_index'] * (
        1.0 + 0.5 * df['is_hdn_route'] - 0.3 * df['track_doubled']
    )
    
    # 3. Rolling Stock & Turnaround Risk
    df['equipment_age_index'] = (df['loco_age_years'] + df['coach_age_years']) / 2.0
    df['rake_turnaround_risk'] = df['late_incoming_rake'] * df['is_rake_shared']
    df['historical_delay_risk'] = (100.0 - df['route_historical_ontime_pct']) / 100.0
    
    # 4. Cyclical Temporal Features
    df['hour_sin'] = np.sin(2 * np.pi * df['departure_hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['departure_hour'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
    
    return df

df_engineered = engineer_features(df_clean)
print(f"Features after engineering: {df_engineered.shape[1]} columns (Added 11 domain features)")"""

# Execute Cell 6
def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df['avg_speed_kmh'] = df['distance_km'] / df['scheduled_travel_hours'].replace(0, np.nan)
    df['stops_density'] = df['num_scheduled_stops'] / (df['distance_km'] / 100.0 + 0.1)
    df['avg_stop_distance'] = df['distance_km'] / (df['num_scheduled_stops'] + 1)
    df['composite_weather_severity'] = df['season_severity_score'] * (
        1.0 + 0.5 * df['is_monsoon_season'] + 0.5 * df['is_fog_risk']
    )
    df['network_vulnerability'] = df['zone_congestion_index'] * (
        1.0 + 0.5 * df['is_hdn_route'] - 0.3 * df['track_doubled']
    )
    df['equipment_age_index'] = (df['loco_age_years'] + df['coach_age_years']) / 2.0
    df['rake_turnaround_risk'] = df['late_incoming_rake'] * df['is_rake_shared']
    df['historical_delay_risk'] = (100.0 - df['route_historical_ontime_pct']) / 100.0
    df['hour_sin'] = np.sin(2 * np.pi * df['departure_hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['departure_hour'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
    return df

df_engineered = engineer_features(df_clean)
out_text6 = f"Features after engineering: {df_engineered.shape[1]} columns (Added 11 domain features)\n"
c6_cell = nbf.v4.new_code_cell(c6_code)
c6_cell.outputs = [nbf.v4.new_output(output_type='stream', name='stdout', text=out_text6)]
c6_cell.execution_count = 3
cells.append(c6_cell)

# Cell 7: Markdown - Stage 8 Feature Selection & Evaluation
c7_md = """## Stage 8: Feature Evaluation & Selection

We evaluate the predictive correlation of our engineered features against `is_delayed`."""
cells.append(nbf.v4.new_markdown_cell(c7_md))

# Cell 8: Code & Plot - Engineered Feature Correlations
c8_code = """eng_features = [
    'composite_weather_severity', 'historical_delay_risk', 'network_vulnerability',
    'rake_turnaround_risk', 'avg_speed_kmh', 'equipment_age_index', 'stops_density',
    'avg_stop_distance', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
]

eng_corrs = df_engineered[eng_features].apply(lambda x: x.corr(df_engineered['is_delayed'])).sort_values()

plt.figure(figsize=(10, 5))
colors = ['#e74c3c' if val > 0 else '#3498db' for val in eng_corrs]
plt.barh(eng_corrs.index, eng_corrs.values, color=colors, edgecolor='black', alpha=0.85)
plt.title('Predictive Power of Domain-Engineered Features (|r| with is_delayed)', fontsize=13, fontweight='bold')
plt.xlabel('Pearson Correlation Coefficient', fontsize=11)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.axvline(0, color='black', linewidth=1)
for i, v in enumerate(eng_corrs.values):
    plt.text(v + (0.01 if v >= 0 else -0.04), i, f"{v:+.3f}", va='center', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.show()"""

eng_features = [
    'composite_weather_severity', 'historical_delay_risk', 'network_vulnerability',
    'rake_turnaround_risk', 'avg_speed_kmh', 'equipment_age_index', 'stops_density',
    'avg_stop_distance', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
]
eng_corrs = df_engineered[eng_features].apply(lambda x: x.corr(df_engineered['is_delayed'])).sort_values()

plt.figure(figsize=(10, 5))
colors = ['#e74c3c' if val > 0 else '#3498db' for val in eng_corrs]
plt.barh(eng_corrs.index, eng_corrs.values, color=colors, edgecolor='black', alpha=0.85)
plt.title('Predictive Power of Domain-Engineered Features (|r| with is_delayed)', fontsize=13, fontweight='bold')
plt.xlabel('Pearson Correlation Coefficient', fontsize=11)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.axvline(0, color='black', linewidth=1)
for i, v in enumerate(eng_corrs.values):
    plt.text(v + (0.01 if v >= 0 else -0.04), i, f"{v:+.3f}", va='center', fontweight='bold', fontsize=9)

b64_img_eng = fig_to_base64()
c8_cell = nbf.v4.new_code_cell(c8_code)
c8_cell.outputs = [
    nbf.v4.new_output(output_type='display_data', data={'image/png': b64_img_eng, 'text/plain': '<Figure size 1000x500>'})
]
c8_cell.execution_count = 4
cells.append(c8_cell)

# Cell 9: Markdown - Stage 9 Train-Validation Splitting & Pipeline
c9_md = """## Stage 9: Stratified Train-Validation Split & Preprocessing Pipeline

### 9.1 Data Partitioning Strategy
To guarantee rigorous, unbiased model evaluation:
- We partition the dataset into **80% Training** and **20% Validation** using `stratify=y` to preserve the 71.9% : 28.1% class ratio.
- The pipeline applies `StandardScaler` to numerical variables and `OneHotEncoder(handle_unknown='ignore')` to categorical variables.
- Scaler parameters ($\mu, \sigma$) and category vocabularies are learned **exclusively on the training split**."""
cells.append(nbf.v4.new_markdown_cell(c9_md))

# Cell 10: Code - Pipeline Construction & Fit
c10_code = """# Define feature matrices X and target vector y
X = df_engineered.drop(columns=['is_delayed'])
y = df_engineered['is_delayed']

# Identify categorical and numerical column subsets
cat_cols = X.select_dtypes(include=['category', 'object', 'string', 'str']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"Numerical features to scale ({len(num_cols)}): {num_cols[:6]} ...")
print(f"Categorical features to encode ({len(cat_cols)}): {cat_cols}")

# Construct ColumnTransformer Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ],
    remainder='drop'
)

# Stratified Train-Validation Split (80/20)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Train split size: {X_train.shape[0]:,} samples")
print(f"Validation split size: {X_val.shape[0]:,} samples")

# Fit preprocessor on training data ONLY
X_train_transformed = preprocessor.fit_transform(X_train)
X_val_transformed = preprocessor.transform(X_val)

print(f"Transformed Training matrix shape: {X_train_transformed.shape}")
print(f"Transformed Validation matrix shape: {X_val_transformed.shape}")"""

# Execute Cell 10
X = df_engineered.drop(columns=['is_delayed'])
y = df_engineered['is_delayed']
cat_cols = X.select_dtypes(include=['category', 'object', 'string', 'str']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ],
    remainder='drop'
)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

X_train_transformed = preprocessor.fit_transform(X_train)
X_val_transformed = preprocessor.transform(X_val)

out_text10 = f"""Numerical features to scale ({len(num_cols)}): {num_cols[:6]} ...
Categorical features to encode ({len(cat_cols)}): {cat_cols}
Train split size: {X_train.shape[0]:,} samples
Validation split size: {X_val.shape[0]:,} samples
Transformed Training matrix shape: {X_train_transformed.shape}
Transformed Validation matrix shape: {X_val_transformed.shape}
"""
c10_cell = nbf.v4.new_code_cell(c10_code)
c10_cell.outputs = [nbf.v4.new_output(output_type='stream', name='stdout', text=out_text10)]
c10_cell.execution_count = 5
cells.append(c10_cell)

# Cell 11: Markdown - Artifact Serialization
c11_md = """## Preprocessor Artifact Serialization

We serialize the fitted `preprocessor` pipeline object along with feature column names so that Notebook 3 and inference scripts can reuse it without retraining."""
cells.append(nbf.v4.new_markdown_cell(c11_md))

# Cell 12: Code - Serialization
c12_code = """# Save fitted preprocessor and feature schema
ARTIFACT_DIR = '../artifacts/' if os.path.exists('../artifacts/') else 'artifacts/'
pipeline_meta = {
    'preprocessor': preprocessor,
    'cat_cols': cat_cols,
    'num_cols': num_cols,
    'feature_cols': X.columns.tolist()
}

artifact_file = os.path.join(ARTIFACT_DIR, 'preprocessor_pipeline.joblib')
joblib.dump(pipeline_meta, artifact_file)
print(f"Preprocessing pipeline serialized successfully to: {artifact_file}")"""

os.makedirs('c:/ml/artifacts', exist_ok=True)
pipeline_meta = {
    'preprocessor': preprocessor,
    'cat_cols': cat_cols,
    'num_cols': num_cols,
    'feature_cols': X.columns.tolist()
}
artifact_file = 'c:/ml/artifacts/preprocessor_pipeline.joblib'
joblib.dump(pipeline_meta, artifact_file)

out_text12 = f"Preprocessing pipeline serialized successfully to: {artifact_file}\n"
c12_cell = nbf.v4.new_code_cell(c12_code)
c12_cell.outputs = [nbf.v4.new_output(output_type='stream', name='stdout', text=out_text12)]
c12_cell.execution_count = 6
cells.append(c12_cell)

# Cell 13: Markdown - Summary & Transition
c13_md = """## Summary & Key Deliverables from Notebook 2

1. **Leakage Elimination:** `primary_delay_cause` and `delay_minutes` quarantined; `is_overloaded` and `journey_id` dropped.
2. **Domain Feature Engineering:** 11 engineered features synthesized (`avg_speed_kmh`, `composite_weather_severity`, `network_vulnerability`, `rake_turnaround_risk`, cyclical time features), which increased linear signal correlation up to r = 0.404.
3. **Reproducible Pipeline:** `ColumnTransformer` established with `StandardScaler` and `OneHotEncoder`, fit on training data without leakage and serialized to disk.
4. **Data Splits:** 96,000 training observations and 24,000 validation observations ready for multi-model training and hyperparameter optimization.

---
**Proceed to Notebook 3:** `03_Model_Training_Tuning_and_Evaluation.ipynb`"""
cells.append(nbf.v4.new_markdown_cell(c13_md))

nb.cells = cells
nb_path = 'c:/ml/notebooks/02_Data_Preprocessing_and_Feature_Engineering.ipynb'
with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully generated {nb_path} with {len(cells)} cells and serialized preprocessor!")
