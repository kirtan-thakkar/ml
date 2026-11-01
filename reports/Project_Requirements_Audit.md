# ECSCI24302: Machine Learning Essentials — Project Requirements Audit
## Project Title: Indian Railways Train Delay Prediction & Network Punctuality Analytics
### Institution: Faculty of Engineering and Technology, Adani University
### Academic Year: 2026–2027 | Evaluation Date: November 2026

---

## Executive Audit Summary

This document provides a systematic, item-by-item verification audit against the official **19-Stage Machine Learning Pipeline** and **Minimum Technical Requirements** outlined in `MLE_PBL_Project_Instructions.pdf`.

* **Overall Syllabus Compliance Score:** **100% (All 19 Stages Verified & Implemented)**
* **Model Artifact Integrity:** Verified (`artifacts/pandas_numpy_pipeline.joblib`, 891 KB)
* **Code Reproducibility:** Verified (`01_Exploratory_Data_Analysis.ipynb`, `02_Data_Preprocessing_and_Feature_Engineering.ipynb`, `03_Model_Training_Tuning_and_Evaluation.ipynb`)
* **Test Set Verification:** Verified (`data/submission.csv`, 375,000 predictions, 100% structural audit pass)
* **Interactive Deployment:** Verified (`app.py`, Streamlit Community Cloud compliant with Deep Dark + Elegant Gold UI)

---

## PART 1: 19-Stage Machine Learning Pipeline Audit

| Stage | Syllabus Requirement | Implementation Evidence & Code Verification | Status |
|:---:|---|---|:---:|
| **1** | **Problem Definition**<br>Define real-world problem, objective, inputs, target/output, and expected outcome. | Defined supervised binary classification for `is_delayed` (>15 min destination arrival delay). 45 pre-departure operational inputs mapped to probability and triage risk tiers.<br>*Evidence: Notebook 1 Cell 1; Project Report Section 2.* | **PASSED** |
| **2** | **Dataset Acquisition**<br>Obtain dataset from Kaggle/UCI, document name, source, link, size, and license. | Kaggle Indian Railways dataset: `ir_train.csv` (1.5M rows, 45 cols, 337 MB), `ir_test.csv` (375k rows, 42 cols, 76 MB), `ir_data_dictionary.csv`.<br>*Evidence: Notebook 1 Cell 3; README Section 5.* | **PASSED** |
| **3** | **Dataset Understanding**<br>Describe observations, features, target, data types, categoricals/numericals, identifiers. | Detailed taxonomy across 8 operational domains: Journey ID, Departure Timings, Route Geography, Infrastructure, Rolling Stock, Weather, Operational History, Target.<br>*Evidence: Notebook 1 Cell 3–5; Report Section 3.3.* | **PASSED** |
| **4** | **Data Quality Check**<br>Check missing values, duplicates, inconsistent values, invalid entries, and outliers. | Zero missing values across 45 features; zero duplicate rows; zero duplicate keys. Identified zero-variance constant column `is_overloaded` (0 for all rows) and dropped it.<br>*Evidence: Notebook 1 Cell 7.* | **PASSED** |
| **5** | **Exploratory Data Analysis**<br>Univariate/bivariate analysis with visualizations. Identify patterns and relationships. | Discovered 72.16% class imbalance; analyzed train priority delay gradient (Vande Bharat ~18% vs Passenger ~88%); identified northern zonal bottlenecks (NR/NCR >78%) and winter fog friction.<br>*Evidence: Notebook 1 Cells 9–17 (Figures 1–5).* | **PASSED** |
| **6** | **Data Preprocessing**<br>Handle missing values, duplicates, outliers, categoricals, and data quality issues. | Enforced strict target leakage quarantine (`delay_minutes` & `primary_delay_cause` removed). Applied NumPy IQR Winsorization on `distance_km` (1,466 km) and `scheduled_travel_hours` (24.9 hrs).<br>*Evidence: Notebook 2 Cells 3–4; utils.py.* | **PASSED** |
| **7** | **Feature Engineering**<br>Create, transform, combine, encode, scale features with operational explanations. | Formulated 11 domain features in `utils.py`: `avg_speed_kmh`, `stops_density`, `avg_stop_distance`, `composite_weather_severity`, `historical_delay_risk`, `network_vulnerability`, `rake_turnaround_risk`, `equipment_age_index`, `congestion_delay_ratio`, `hour_sin`, `hour_cos`.<br>*Evidence: Notebook 2 Cell 5; utils.py.* | **PASSED** |
| **8** | **Feature Selection**<br>Identify relevant features using statistical or model-based techniques. | Calculated Pearson correlations of engineered features with `is_delayed`. Feature importance from LightGBM confirmed 5 engineered features in Top 15 predictors.<br>*Evidence: Notebook 2 Cell 7; Notebook 3 Cell 16.* | **PASSED** |
| **9** | **Train-Test Split**<br>Divide data into training and testing sets. Use validation data / cross-validation. | Executed 80:20 stratified split (8,000 train, 2,000 validation records) with fixed random seed 42, preserving exact 72.16% class ratio. Scalers fit solely on training split.<br>*Evidence: Notebook 2 Cell 9; Notebook 3 Cell 3.* | **PASSED** |
| **10** | **Baseline Model**<br>Build a simple baseline to provide a reference benchmark. | Implemented `DummyClassifier(strategy='most_frequent')`. Proved that 72.15% accuracy represents zero intelligence (ROC-AUC = 0.5000), exposing the class imbalance trap.<br>*Evidence: Notebook 3 Cell 6; Report Section 8.* | **PASSED** |
| **11** | **Model Selection**<br>Select at least three suitable ML algorithms with justification. | Selected and evaluated 5 distinct algorithm families: Dummy Baseline, Logistic Regression (linear boundary), Decision Tree (Gini splits), Random Forest (bagging), and LightGBM (gradient boosting).<br>*Evidence: Notebook 3 Cell 6.* | **PASSED** |
| **12** | **Model Training**<br>Train the selected models using training data. | Fitted all candidate algorithms on 8,000-record training matrix with 8,111 sparse features. Captured training runtimes and convergence metrics.<br>*Evidence: Notebook 3 Cell 6.* | **PASSED** |
| **13** | **Hyperparameter Tuning**<br>Tune important hyperparameters using validation or cross-validation. | Executed `RandomizedSearchCV` with 2-fold CV optimizing ROC-AUC on Random Forest (`n_est=80, depth=16, split=5`, CV AUC=0.8826) and LightGBM (`lr=0.05, leaves=63, depth=6`, CV AUC=0.9089).<br>*Evidence: Notebook 3 Cell 8.* | **PASSED** |
| **14** | **Model Evaluation**<br>Evaluate final models using problem-appropriate classification metrics. | Multi-metric validation framework: Accuracy (85.85%), Precision (88.72%), Recall (92.10%), F1-Score (0.9038), and ROC-AUC (0.9121). Supported by ROC curves and confusion matrix.<br>*Evidence: Notebook 3 Cells 10 & 22.* | **PASSED** |
| **15** | **Model Comparison**<br>Compare models in one table; discuss performance, complexity, and practical trade-offs. | Compiled official Model Comparison Table conforming to Section 14 guidelines. Justified Tuned LightGBM as champion based on safety recall and sub-15ms latency.<br>*Evidence: Notebook 3 Cell 12; Report Section 10.* | **PASSED** |
| **16** | **Error Analysis**<br>Investigate incorrect predictions and identify operational reasons. | Quantified confusion matrix: TP=1,329, TN=388, FP=169, FN=114. Diagnosed False Positives (high-congestion zones where drivers recovered time) and False Negatives (unforeseen en-route traction failures).<br>*Evidence: Notebook 3 Cell 14; Report Section 11.* | **PASSED** |
| **17** | **Model Interpretation**<br>Explain important features, model behavior, and meaningful patterns. | Extracted LightGBM split importances: `avg_speed_kmh` ranked #1 (570 splits), followed by `network_vulnerability` (309 splits) and `route_historical_ontime_pct` (307 splits).<br>*Evidence: Notebook 3 Cell 16; Report Section 12.* | **PASSED** |
| **18** | **Final Demonstration**<br>Demonstrate final model on unseen input or interactive application. | Generated predictions for all 375,000 test journeys (`data/submission.csv`, verified). Deployed interactive Streamlit web dashboard (`app.py`) with Green/Amber/Red triage.<br>*Evidence: Notebook 3 Cells 19–21; app.py.* | **PASSED** |
| **19** | **Conclusion & Future Work**<br>Summarize methodology, findings, limitations, and future improvements. | Synthesized end-to-end findings, transparently stated 10k sampling and static telemetry limitations, and detailed 4-step distributed cloud roadmap.<br>*Evidence: Report Sections 14–15; Slide 12.* | **PASSED** |

---

## PART 2: Minimum Technical Requirements Audit

* **[x] Exploratory Data Analysis (EDA):** Univariate, bivariate, class distribution, and correlation heatmaps generated and documented.
* **[x] Missing Value Handling:** Audited across all 45 columns; confirmed 0 missing values; documented in report and app.
* **[x] Outlier Identification & Treatment:** NumPy IQR Winsorization implemented on continuous columns (`distance_km` capped at 1,466 km, `scheduled_travel_hours` capped at 24.9 hrs).
* **[x] Categorical Encoding:** One-hot encoding implemented via Pandas with strict schema column alignment (reindex with fill_value=0). High-cardinality `train_number` excluded to prevent 5,000+ sparse dummy columns.
* **[x] Feature Scaling:** Z-score standardization applied using training mean and std only.
* **[x] At Least Three ML Models:** 5 model families evaluated (Baseline, Logistic Regression, Decision Tree, Random Forest, LightGBM).
* **[x] Baseline Model:** `DummyClassifier(strategy='most_frequent')` trained and evaluated.
* **[x] Hyperparameter Tuning:** Performed via `RandomizedSearchCV` on Random Forest and LightGBM with 2-fold cross-validation.
* **[x] Cross-Validation:** 2-fold CV executed during hyperparameter search optimizing ROC-AUC.
* **[x] Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix calculated.
* **[x] Final Model Comparison Table:** Formatted according to Section 14 college template.
* **[x] Error Analysis:** False Positives vs False Negatives breakdown across railway zones and train categories analyzed.
* **[x] Limitations & Academic Integrity:** Explicitly stated hardware sampling (10k records), static timetable scope, and Kaggle origin citation.

---

## PART 3: Data Leakage Quarantine Verification

Data leakage occurs when an algorithm is exposed to target or future information that would be unavailable in real-world deployment at departure time. The project audited and resolved the following:

1. `delay_minutes`: Continuous arrival delay duration recorded upon journey completion.
   * *Status:* Quarantined. Removed from feature matrix before training.
2. `primary_delay_cause`: Diagnostic label assigned after journey completion.
   * *Status:* Quarantined. Removed from feature matrix before training.
3. Feature Scaling Statistics:
   * *Status:* Mean and standard deviation computed strictly on the training partition ($n=8,000$); applied to validation and test sets without refitting.
4. Categorical Schema Alignment:
   * *Status:* Training feature columns preserved; validation and test sets reindexed to match training schema.

---

## Conclusion
The project satisfies all syllabus guidelines, assessment criteria, and technical deliverables required by Adani University for ECSCI24302 Machine Learning Essentials.
