# Indian Railways Train Delay Prediction & Network Punctuality Analytics
## ECSCI24302 – Machine Learning Essentials: Project-Based Learning (PBL)

An end-to-end Machine Learning pipeline built to predict Indian Railways train delays (>15 minutes at destination), strictly adhering to the 19-stage syllabus guidelines in `MLE_PBL_Project_Instructions.pdf`.

---

### Project Structure

```text
c:\ml\
├── data\
│   ├── ir_data_dictionary.csv                    # Attribute definitions
│   ├── ir_train.csv                              # 1,500,000 training journeys (337 MB)
│   ├── ir_test.csv                               # 375,000 competition test journeys (76 MB)
│   └── ir_sample_submission.csv                  # Submission schema
│
├── notebooks\
│   ├── 01_Exploratory_Data_Analysis.ipynb        # Stages 1 to 5 (Quality checks, univariate/bivariate EDA, plots)
│   ├── 02_Data_Preprocessing_and_Feature_Engineering.ipynb # Stages 6 to 9 (Leakage quarantine, 11 features, pipeline)
│   └── 03_Model_Training_Tuning_and_Evaluation.ipynb     # Stages 10 to 19 (Baseline, models, tuning, eval, demo)
│
├── reports\
│   └── Project_Report.md                         # Formal academic project report matching Section 12 guidelines
│
├── End_to_End_Railway_Delay_Prediction.ipynb     # Master unified notebook containing all 19 stages
├── utils.py                                      # Shared feature engineering helper functions
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

### How to Run

1. **Step-by-Step Modular Workflow:**
   - Open and run [01_Exploratory_Data_Analysis.ipynb](file:///c:/ml/notebooks/01_Exploratory_Data_Analysis.ipynb) to view data distributions and EDA plots.
   - Open and run [02_Data_Preprocessing_and_Feature_Engineering.ipynb](file:///c:/ml/notebooks/02_Data_Preprocessing_and_Feature_Engineering.ipynb) to inspect preprocessing, feature formulas, and pipeline serialization.
   - Open [03_Model_Training_Tuning_and_Evaluation.ipynb](file:///c:/ml/notebooks/03_Model_Training_Tuning_and_Evaluation.ipynb) when ready to train, tune, and evaluate the models.

2. **Master All-in-One Notebook:**
   - Open [End_to_End_Railway_Delay_Prediction.ipynb](file:///c:/ml/End_to_End_Railway_Delay_Prediction.ipynb) for the complete, self-contained pipeline.
