# Indian Railways Train Delay Prediction & Network Punctuality Analytics
## ECSCI24302 – Machine Learning Essentials: Project-Based Learning (PBL)

An end-to-end Machine Learning pipeline built to predict Indian Railways train delays (>15 minutes at destination), strictly adhering to the 19-stage syllabus guidelines in `MLE_PBL_Project_Instructions.pdf`.

---

### Project Structure

```text
D:\ML PROJECT\ml\
├── data/                                         # [Local only, gitignored]
│   ├── ir_data_dictionary.csv                    # Attribute definitions
│   ├── ir_train.csv                              # 1,500,000 training journeys (337 MB)
│   ├── ir_test.csv                               # 375,000 competition test journeys (76 MB)
│   └── ir_sample_submission.csv                  # Submission schema
│
├── artifacts/
│   └── pandas_numpy_pipeline.joblib              # Serialized Tuned LightGBM model & preprocessing metadata (~891 KB)
│
├── notebooks/
│   ├── 01_Exploratory_Data_Analysis.ipynb        # Stages 1 to 5 (Quality checks, univariate/bivariate EDA, plots)
│   ├── 02_Data_Preprocessing_and_Feature_Engineering.ipynb # Stages 6 to 9 (Leakage quarantine, 11 features, pipeline)
│   └── 03_Model_Training_Tuning_and_Evaluation.ipynb     # Stages 10 to 19 (Baseline, models, tuning, eval, demo)
│
├── reports/
│   └── Project_Report.md                         # Formal academic project report matching Section 12 guidelines
│
├── .streamlit/
│   └── config.toml                               # Streamlit theme and deployment server configuration
│
├── End_to_End_Railway_Delay_Prediction.ipynb     # Master unified notebook containing all 19 stages
├── utils.py                                      # Shared feature engineering helper functions
├── app.py                                        # Interactive Streamlit Web Application (Dispatch Mission Control)
├── requirements.txt                              # Pinned Python package dependencies for local and cloud deployment
├── .gitignore                                    # Excludes large CSVs, caches, checkpoints, and secrets
└── README.md                                     # Project guide and overview
```

---

### Notebook Outline & Stages Covered

1. **`notebooks/01_Exploratory_Data_Analysis.ipynb`**
   - **Stage 1:** Problem Definition & Formalization
   - **Stage 2:** Dataset Acquisition & Overview
   - **Stage 3:** Dataset Understanding & Feature Taxonomy
   - **Stage 4:** Data Quality Assurance (Missing values, duplicates, zero-variance identification: `is_overloaded`)
   - **Stage 5:** Exploratory Data Analysis (Target class imbalance, univariate distributions, bivariate delay analysis across train categories, zones, weather seasons, root cause diagnostics, and correlation heatmap)

2. **`notebooks/02_Data_Preprocessing_and_Feature_Engineering.ipynb`**
   - **Stage 6:** Data Preprocessing & Target Leakage Prevention (Quarantining `delay_minutes` & `primary_delay_cause`)
   - **Stage 7:** Domain Feature Engineering (11 features: `avg_speed_kmh`, `stops_density`, `composite_weather_severity`, `network_vulnerability`, `equipment_age_index`, `rake_turnaround_risk`, cyclical time features)
   - **Stage 8:** Feature Evaluation & Correlation Analysis
   - **Stage 9:** Stratified Train-Validation Splitting (80/20) & Preprocessing Pipeline (`StandardScaler` + `OneHotEncoder`)

3. **`notebooks/03_Model_Training_Tuning_and_Evaluation.ipynb`**
   - **Stage 10:** Baseline Model (`DummyClassifier` majority baseline)
   - **Stage 11:** Model Selection Justification (Logistic Regression, Decision Tree, Random Forest, LightGBM)
   - **Stage 12:** Model Training
   - **Stage 13:** Hyperparameter Tuning & Cross-Validation (Random Forest & LightGBM)
   - **Stage 14:** Multi-Metric Model Evaluation (Accuracy, Precision, Recall, F1-Score, ROC-AUC, ROC Curve, Confusion Matrix)
   - **Stage 15:** Official Model Comparison Table (Conforming to Section 14 Schema)
   - **Stage 16:** Error Analysis (False Positive and False Negative breakdown across Zones & Train Types)
   - **Stage 17:** Model Interpretation & Feature Importance (Top 15 features)
   - **Stage 18:** Test Set Inference (`ir_test.csv`) & Interactive Single-Journey Prediction Demo
   - **Stage 19:** Conclusion, Operational Limitations & Viva Voce Q&A Defense Guide

---

### How to Run Notebooks

1. **Step-by-Step Modular Workflow:**
   - Open and run [01_Exploratory_Data_Analysis.ipynb](file:///notebooks/01_Exploratory_Data_Analysis.ipynb) to view data distributions and EDA plots.
   - Open and run [02_Data_Preprocessing_and_Feature_Engineering.ipynb](file:///notebooks/02_Data_Preprocessing_and_Feature_Engineering.ipynb) to inspect preprocessing, feature formulas, and pipeline serialization.
   - Open [03_Model_Training_Tuning_and_Evaluation.ipynb](file:///notebooks/03_Model_Training_Tuning_and_Evaluation.ipynb) when ready to train, tune, and evaluate the models.

2. **Master All-in-One Notebook:**
   - Open [End_to_End_Railway_Delay_Prediction.ipynb](file:///End_to_End_Railway_Delay_Prediction.ipynb) for the complete, self-contained pipeline.

---

### 🌐 Interactive Streamlit Web Application

The project includes an operational railway dispatch analytics dashboard located in `app.py`. Built using Streamlit, LightGBM, and pure Pandas/NumPy preprocessing, it provides real-time decision support for Indian Railways train operations.

#### Key Dashboard Features:
- **🚄 Real-Time Single-Journey Predictor:** Computes delay probability (>15 min destination arrival delay) with automated domain feature engineering (`avg_speed_kmh`, `stops_density`, `composite_weather_severity`, `network_vulnerability`, `rake_turnaround_risk`, cyclical trigonometric time encodings).
- **🚨 Dispatch Directive & Alert System:** Categorizes journeys into operational risk levels conforming to the Project Report:
  - **GREEN (On-Time Expected, < 40%):** Standard timetable priority.
  - **AMBER (Moderate Delay Risk, 40% – 65%):** Advisory caution; monitor turnaround and track congestion windows.
  - **RED (High Delay Risk, > 65%):** Urgent operational intervention; priority junction clearance and relief buffer.
- **📊 Operational Batch Journey Audit:** Inspects entire train fleets simultaneously. Supports built-in 10-journey benchmark fleet demonstration and custom CSV uploads with one-click prediction download.
- **🗺️ Network Punctuality & Zone Risk Matrix:** Contrasts congestion vs winter fog vulnerability across all 16 Indian Railways administrative zones.
- **🔬 Model Architecture & Governance:** Displays the official 7-model comparative benchmark table, top 12 LightGBM feature importances, and data leakage quarantine safeguards.

---

### 🚀 Running the Streamlit App Locally

1. **Ensure your Python environment is active** (Python 3.10 to 3.13):
   ```bash
   # Optional: Create and activate a virtual environment
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

2. **Install compatible dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```
   The application will launch and open in your default browser at `http://localhost:8501`.

---

### ☁️ Deploying to Streamlit Community Cloud

The repository is structured for seamless, one-click deployment on [Streamlit Community Cloud](https://streamlit.io/cloud):

#### 1. Pre-Deployment Verification Checklist
- [x] **Lightweight Model Artifact:** `artifacts/pandas_numpy_pipeline.joblib` (~891 KB) is committed to Git.
- [x] **Zero Large Data Overhead:** The large 1.5M row dataset (`data/ir_train.csv` and `data/ir_test.csv`) is excluded via `.gitignore` and is **never** loaded at app startup.
- [x] **Reproducible Preprocessing:** `utils.py` provides exact vectorized feature formulas matching training.
- [x] **Pinned Dependencies:** `requirements.txt` specifies compatible versions for all required libraries.
- [x] **Server Settings:** `.streamlit/config.toml` configures headless mode and visual themes.

#### 2. Step-by-Step Deployment Instructions

1. **Push your code to GitHub:**
   ```bash
   git add app.py requirements.txt .gitignore .streamlit/config.toml README.md
   git commit -m "feat: prepare Indian Railways delay predictor for Streamlit Cloud deployment"
   git push origin <your-branch-name>
   ```

2. **Connect to Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   - Click **"Create app"** (or **"New app"**).
   - In the repository dropdown, select your repository (e.g. `your-username/railway-delay-prediction`).
   - Select the branch you pushed to.
   - Set **Main file path** to: `app.py`.

3. **Deploy:**
   - Click **"Deploy!"**.
   - Streamlit Cloud will automatically provision a container, install packages from `requirements.txt`, load `artifacts/pandas_numpy_pipeline.joblib`, and serve the live dashboard.
   - The app runs in low-memory mode (~50 MB RAM), well within Streamlit Cloud free-tier quotas (1 GB limit).
