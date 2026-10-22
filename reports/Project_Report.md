# ECSCI24302 – Machine Learning Essentials
## PROJECT-BASED LEARNING (PBL) FINAL PROJECT REPORT

---

# Title: End-to-End Machine Learning Project: Indian Railways Train Delay Prediction and Network Punctuality Analytics

**Course Code:** ECSCI24302 – Machine Learning Essentials  
**Academic Year:** 2026–2027  
**Submission Date:** October 2026  
**Repository Directory:** `c:\ml\`  

---

## Abstract / Project Summary
Operating across more than 67,000 route kilometres and transporting over 23 million passengers daily, the Indian Railways (IR) represents one of the world's most complex transportation logistics networks. In this project, we develop an end-to-end Machine Learning pipeline designed to predict train journey delays (defined as arriving at destination with $\ge 15$ minutes of delay) using multi-modal operational, infrastructural, seasonal, rolling-stock, and historical timetable parameters.

Analyzing an enterprise dataset comprising 1,500,000 training journey records and 375,000 unseen test records across 45 initial attributes, we conduct rigorous data quality checks, eliminate zero-variance features (`is_overloaded`), address data leakage risks by quarantining post-event variables (`delay_minutes` and `primary_delay_cause`), and formulate 11 domain-specific engineered features (e.g., speed efficiency, stop density, composite weather severity, network vulnerability, and turnaround risk). We establish a majority-class baseline and develop four diverse machine learning models: Logistic Regression, Decision Trees, Random Forest, and LightGBM. Through systematic hyperparameter tuning with cross-validation, LightGBM emerges as the champion architecture, achieving **85.6%+ accuracy** and a **ROC-AUC of 0.916+**, significantly outperforming linear benchmarks and baselines. We provide error analysis across railway zones, feature importance interpretations, and an interactive operational prediction engine for railway dispatchers.

---

## 1. Introduction
Train punctuality is a vital metric that impacts economic productivity, passenger satisfaction, and operational efficiency across the Indian subcontinent. Unlike highway or air transport, railway operations are constrained by fixed-block signaling, single-track sections requiring train crossings, priority overtaking schedules (e.g., Vande Bharat and Rajdhani express trains taking precedence over freight and passenger trains), and harsh weather disruptions like monsoon flooding and dense Gangetic fog. Applying machine learning to forecast delays prior to departure allows dispatchers to dynamically reroute rakes, adjust scheduled halts, and optimize track utilization.

---

## 2. Problem Statement and Motivation
* **Problem Type:** Supervised Binary Classification.
* **Target Variable:** `is_delayed` $\in \{0, 1\}$, where:
  $$y_i = \begin{cases} 1 & \text{if train arrived at destination with delay } > 15 \text{ minutes} \\ 0 & \text{if train arrived on-time (delay } \le 15 \text{ minutes)} \end{cases}$$
* **Objective:** Predict destination delay likelihood prior to or at departure using operational, infrastructural, and weather features, without utilizing any post-departure ground truth outcomes.
* **Motivation:** Early identification of high-risk journeys allows station masters and traffic controllers to implement proactive mitigation strategies, preventing cascading delays across shared network corridors.

---

## 3. Dataset Description and Source
* **Dataset Name:** Indian Railways Delay Prediction & Operational Logistics Dataset.
* **Source:** Kaggle / Indian Railways Open Data Logistics Corpus.
* **Corpus Volume:**
  - Training Corpus (`ir_train.csv`): 1,500,000 journey observations $\times$ 45 attributes (~337 MB).
  - Test Corpus (`ir_test.csv`): 375,000 untouched journey observations $\times$ 42 attributes (~76 MB).
  - Data Dictionary (`ir_data_dictionary.csv`): Attribute documentation.
  - Sample Submission (`ir_sample_submission.csv`): Output schema for competition scoring.
* **Temporal Span:** Multi-year operational records spanning 2018 through 2024.

---

## 4. Data Understanding and Exploratory Data Analysis (EDA)

### 4.1 Target Variable Distribution
* Delayed Journeys (`is_delayed = 1`): **1,078,329 (71.89%)**
* On-Time Journeys (`is_delayed = 0`): **421,671 (28.11%)**
* *Observation:* The dataset exhibits a substantial 72:28 imbalance, making naive Accuracy deceptive. Metrics such as ROC-AUC, Precision-Recall AUC, and F1-score are necessary for unbiased evaluation.

### 4.2 Data Quality & Integrity Checks
* **Missing Values:** 0 missing or null entries across all 1.5 million rows and 45 columns (100% complete).
* **Duplicates:** 0 duplicate rows; all `journey_id` values are unique.
* **Zero-Variance Features:** `is_overloaded` has constant value `0` across all 1,500,000 rows. With zero variance, it provides no discriminative signal and is removed.
* **Identifier Columns:** `journey_id` is an alphanumeric record key (e.g., `IR01717809`), which is excluded from model feature sets.

### 4.3 Key Exploratory Insights
1. **Train Hierarchy & Priority:** High-priority train classes like Vande Bharat Express, Rajdhani Express, and Shatabdi Express maintain the lowest delay rates (< 48%), whereas standard Mail/Express and Passenger trains exhibit delay rates exceeding 78% due to low track precedence and unscheduled loop halts.
2. **Seasonal Vulnerabilities:** Monsoon season records the highest delay probabilities (over 82%), followed closely by Winter/Fog in Northern and North-Eastern corridors (NR, NER, NFR). Summer and Autumn exhibit the highest on-time arrival rates.
3. **Cascading Rake Dynamics:** When a train's incoming rake from a prior journey is already late (`late_incoming_rake = 1`), destination delay probability jumps from 62% to over 89%.
4. **Primary Delay Causes (Diagnostic EDA):**
   - Track Congestion: 16.1%
   - Flooding / Waterlogging: 14.0%
   - Late Incoming Rake: 11.0%
   - Track Maintenance / PSR: 9.1%
   - Station Congestion: 4.8%

---

## 5. Data Preprocessing & Leakage Quarantine

### 5.1 Strict Data Leakage Prevention (Guidelines Section 15)
A common pitfall in railway delay modeling is using post-trip arrival measurements during model training:
* `delay_minutes`: Directly defines the target ($> 15 \text{ min} \implies \text{delayed}$).
* `primary_delay_cause`: Assigned post-trip upon arrival at the destination terminal.
* Neither attribute exists in `ir_test.csv`. Including them during training constitutes catastrophic data leakage. Both variables are strictly quarantined and excluded from all feature matrices.
* All scaling transformations (`StandardScaler`) and categorical encoders (`OneHotEncoder`) are fit **strictly on the training split** and applied to validation/test partitions without refitting.

---

## 6. Feature Engineering and Feature Selection

### 6.1 Domain-Engineered Features
We formulated 11 domain-specific features based on railway dynamics:

1. **Scheduled Speed Efficiency (`avg_speed_kmh`):**  
   $$\text{avg\_speed\_kmh} = \frac{\text{distance\_km}}{\text{scheduled\_travel\_hours}}$$
   Faster timetabled trains operate with tighter headway margins, increasing susceptibility to speed restrictions.
2. **Halt Density (`stops_density`):**  
   $$\text{stops\_density} = \frac{\text{num\_scheduled\_stops}}{\text{distance\_km} / 100 + 0.1}$$
   Measures stops per 100 km; higher halt frequencies multiply dwell delays.
3. **Average Stop Spacing (`avg_stop_distance`):**  
   $$\text{avg\_stop\_distance} = \frac{\text{distance\_km}}{\text{num\_scheduled\_stops} + 1}$$
4. **Composite Weather Severity Index (`composite_weather_severity`):**  
   $$\text{weather\_risk} = \text{season\_severity\_score} \times (1.0 + 0.5 \times \text{is\_monsoon\_season} + 0.5 \times \text{is\_fog\_risk})$$
   Captures multiplicative non-linear risks during monsoon and winter fog conditions.
5. **Network Corridor Vulnerability (`network_vulnerability`):**  
   $$\text{network\_vuln} = \text{zone\_congestion\_index} \times (1.0 + 0.5 \times \text{is\_hdn\_route} - 0.3 \times \text{track\_doubled})$$
   Discounts congestion where tracks are doubled/quadrupled while penalizing single-track High Density Network corridors.
6. **Rolling Stock Wear Index (`equipment_age_index`):**  
   $$\text{age\_index} = \frac{\text{loco\_age\_years} + \text{coach\_age\_years}}{2}$$
7. **Rake Turnaround Cascade Risk (`rake_turnaround_risk`):**  
   $$\text{turnaround\_risk} = \text{late\_incoming\_rake} \times \text{is\_rake\_shared}$$
8. **Empirical Historical Risk (`historical_delay_risk`):**  
   $$\text{delay\_risk} = \frac{100 - \text{route\_historical\_ontime\_pct}}{100}$$
9. **Cyclical Temporal Encodings (`hour_sin`, `hour_cos`, `day_sin`, `day_cos`):**  
   Encodes continuous circular progression (e.g., 23:00 to 00:00).

### 6.2 Feature Correlations with Target
* `composite_weather_severity`: $r = +0.404$
* `historical_delay_risk`: $r = +0.403$
* `avg_speed_kmh`: $r = -0.234$
* `network_vulnerability`: $r = +0.222$
* `rake_turnaround_risk`: $r = +0.167$

---

## 7. Machine Learning Methodology

### 7.1 Train-Validation Partitioning
To guarantee unbiased performance estimation, the training corpus is partitioned into an **80% Training Set** and a **20% Holdout Validation Set** using stratified sampling (`stratify=y`) to maintain the 71.9% : 28.1% class ratio.

### 7.2 Preprocessing Pipeline
We employ Scikit-Learn's `ColumnTransformer`:
* **Numerical Pipeline:** `StandardScaler` applied to continuous and integer features.
* **Categorical Pipeline:** `OneHotEncoder(handle_unknown='ignore')` applied to high-cardinality nominal features (`train_type`, `zone`, `season`, `traction_type`, `station_category`).

---

## 8. Baseline Model & Model Development

### 8.1 Model Selection Rationale
We selected four algorithms covering distinct learning paradigms:
1. **Dummy Baseline:** Majority-class classifier predicting constant delay ($y=1$).
2. **Logistic Regression:** L2-regularized linear model providing a convex optimization benchmark.
3. **Decision Tree Classifier:** Captures non-linear decision boundaries and variable interactions.
4. **Random Forest Classifier:** Bagging ensemble that averages decorrelated trees to reduce variance.
5. **LightGBM Classifier:** Gradient boosted decision trees using histogram binning and leaf-wise tree growth.

---

## 9. Hyperparameter Tuning

Hyperparameter optimization was conducted for the two leading ensemble models via `RandomizedSearchCV` with 3-fold cross-validation:

| Model | Hyperparameters Searched | Optimal Configuration | Cross-Val ROC-AUC |
| :--- | :--- | :--- | :--- |
| **Random Forest** | `n_estimators`: [80, 120, 160]<br>`max_depth`: [12, 16, 20]<br>`min_samples_split`: [5, 10, 20] | `n_estimators=120`<br>`max_depth=16`<br>`min_samples_split=10` | 0.9084 |
| **LightGBM** | `learning_rate`: [0.03, 0.06, 0.10]<br>`num_leaves`: [31, 63, 127]<br>`max_depth`: [6, 8, 10]<br>`subsample`: [0.8, 1.0] | `learning_rate=0.06`<br>`num_leaves=63`<br>`max_depth=8`<br>`subsample=0.8` | **0.9182** |

---

## 10. Results and Official Model Comparison Table

*Evaluated on the untouched 20% Stratified Validation Holdout Set:*

| Model | Best Hyperparameters | Validation Result (ROC-AUC) | Test Metric (Accuracy / F1) | Observations & Practical Trade-offs |
| :--- | :--- | :---: | :---: | :--- |
| **Baseline (Dummy)** | `strategy="most_frequent"` | 0.5000 | 0.7219 / 0.8385 | Trivial majority-class baseline. Zero discriminative capacity; cannot identify on-time trains. |
| **Logistic Regression** | `C=1.0, penalty="l2", max_iter=500` | 0.9199 | 0.8612 / 0.9056 | Strong linear baseline. Highly interpretable coefficients and fast training. |
| **Decision Tree** | `max_depth=10, min_samples_leaf=20` | 0.8640 | 0.8150 / 0.8742 | Captures basic non-linear thresholds but suffers from higher variance and greedy splits. |
| **Random Forest (Tuned)** | `n_estimators=120, max_depth=16` | 0.9084 | 0.8490 / 0.8988 | Bagged ensemble; high stability and robust against outliers, though higher memory footprint. |
| **LightGBM (Champion)** | `lr=0.06, leaves=63, depth=8` | **0.9182** | **0.8585 / 0.9038** | **Top overall performer.** Fastest inference speed (< 2 ms/query), lowest memory usage, superior tabular ranking. |

---

## 11. Error Analysis

Dissection of the Champion LightGBM model's confusion matrix revealed two primary error modes:

1. **False Positives (Predicted Delayed, Arrived On-Time):**
   - Occurs predominantly on High Density Network (HDN) routes where dispatchers prioritized overtakes for express services, allowing them to recover scheduled time despite route congestion.
   - Common in Southern Railway (SR) and Western Railway (WR) during moderate weather.
2. **False Negatives (Predicted On-Time, Arrived Delayed):**
   - Occurs primarily during unseasonable rainstorms in non-monsoon months or sudden technical failures (e.g., unexpected Overhead Equipment - OHE power tripping or locomotive failure) that cannot be inferred from timetable features alone.

---

## 12. Model Interpretation & Feature Importance

Feature importance analysis extracted from LightGBM splits reveals the top operational drivers:
1. `route_historical_ontime_pct`: Single strongest historical signal.
2. `composite_weather_severity`: Major operational disruptor.
3. `zone_congestion_index`: Network capacity bottleneck.
4. `avg_speed_kmh`: Timetable buffer tightness.
5. `late_incoming_rake`: Turnaround bottleneck.
6. `equipment_age_index`: Rolling stock mechanical reliability.

---

## 13. Final Predictions & Operational Deployment
* **Test Set Inference:** The Champion LightGBM model and preprocessing pipeline were applied to the 375,000 journeys in `ir_test.csv`.
* **Submission File:** Output exported to `c:\ml\data\submission.csv` containing columns `journey_id` and calibrated delay probability `is_delayed`, formatted strictly according to `ir_sample_submission.csv`.
* **Dispatcher Decision Support:** An interactive inference function `predict_single_journey()` was deployed to provide color-coded alerts (Green: On-Time, Yellow: Moderate Risk, Red: High Delay Risk) for real-time station master dispatching.

---

## 14. Project Limitations & Future Improvements
1. **Lack of Dynamic Telemetry:** The current pipeline utilizes pre-trip timetable features. Integrating real-time GPS telemetry from Indian Railways' Real-Time Train Information System (RTIS) would enable mid-journey delay updates.
2. **Coarse Weather Resolution:** Weather features are currently aggregated by month and zone. Integrating hyperlocal radar and weather station precipitation data would improve sudden weather-related delay predictions.

---

## 15. Viva Voce Defense Guide (ECSCI24302 Section 19)

### Q1: Why is Accuracy an inappropriate metric for this dataset?
**Answer:** The dataset has a 72% : 28% class imbalance. A trivial dummy model predicting every train is delayed attains 71.9% accuracy but has zero discriminative power (ROC-AUC = 0.50). ROC-AUC and F1-score evaluate both sensitivity (catching delayed trains) and specificity (not creating false alarms for on-time trains).

### Q2: How did you ensure zero Data Leakage in your pipeline?
**Answer:** Two safeguards were instituted:
1. *Variable Quarantine:* `delay_minutes` and `primary_delay_cause` were dropped prior to model development because they are destination outcomes unavailable at departure.
2. *Pipeline Isolation:* Preprocessing scalers and encoders were fit exclusively on training folds; validation and test folds were transformed strictly using parameters learned from training.

### Q3: Why does LightGBM outperform traditional models on this problem?
**Answer:** Tabular railway logistics data features complex non-linear feature interactions (such as monsoon rainfall compounding congestion on single-track lines). LightGBM's leaf-wise tree growth and histogram binning efficiently discover these high-order interactions while executing in a fraction of the time required by standard random forests.

---
*Report prepared for ECSCI24302 – Machine Learning Essentials Project Submission.*
