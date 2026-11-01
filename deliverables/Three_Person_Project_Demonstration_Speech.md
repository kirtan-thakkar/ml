# Three-Person Live Project Demonstration & Presentation Speech
### Course: ECSCI24302 – Machine Learning Essentials (PBL Academic Year 2026–2027)
**Project Title:** Indian Railways Train Delay Prediction & Network Punctuality Analytics  
**Institution:** Faculty of Engineering & Technology, Adani University  
**Team Members:**  
1. **Dhruv** (Team Lead — Introduction, Problem Definition, Dataset Overview & Live Predictor Demo)  
2. **Darshi** (Team Member — Dataset Understanding, EDA, Preprocessing Pipeline & Feature Engineering)  
3. **Kirtan** (Team Member — Model Benchmarks, LightGBM Tuning, Confusion Matrix, Error Analysis & Conclusion)  
**Total Estimated Time:** 7 to 9 minutes (approx. 2.5 to 3 minutes per speaker)

---

## 🎭 Presentation & Live Demo Master Cue Sheet

```
+---------------------------------------------------------------------------------------------------------+
| SPEAKER    | TIME     | PPT SLIDES COVERED         | LIVE STREAMLIT APP MODULES DEMONSTRATED             |
+---------------------------------------------------------------------------------------------------------+
| 1. Dhruv   | 2.5 min  | Slide 1 (Title & Team)     | • 🏠 Module 1: Overview & Mission Control           |
|            |          | Slide 2 (Problem & Obj.)   | • 🎯 Module 2: Train Delay Predictor (Preset 1 & 2)  |
|            |          | Slide 3 (Dataset Overview) |                                                     |
+---------------------------------------------------------------------------------------------------------+
| 2. Darshi  | 2.5 min  | Slide 4 (EDA & Insights)   | • 🔍 Module 4: Exploratory Data Analysis (EDA)      |
|            |          | Slide 5 (Preprocessing)    | • ⚙️ Module 5: Data Preprocessing & Pipeline        |
|            |          | Slide 6 (Feature Eng.)     | • 🧬 Module 6: Feature Engineering & Selection      |
+---------------------------------------------------------------------------------------------------------+
| 3. Kirtan  | 3.0 min  | Slide 7 (Workflow/Baseline)| • 🧪 Module 7: Model Development & Benchmarks       |
|            |          | Slide 8 (Tuning)           | • 📊 Module 8: Evaluation Metrics & Confusion Matrix|
|            |          | Slide 9 (Comparison Table) | • 🚨 Module 9: Error Analysis & Misclassifications  |
|            |          | Slide 10 (Confusion Matrix)| • 💡 Module 10: Model Interpretation (Feature Imp.) |
|            |          | Slide 11 (Error/Limits)    |                                                     |
|            |          | Slide 12 (Conclusion & Q&A)|                                                     |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🎙️ PART 1: DHRUV — INTRODUCTION, PROBLEM DEFINITION & PREDICTOR DEMO
*(Target Speaking Duration: 2.5 minutes)*

### [SHOW PPT SLIDE 1: Title & Team Details]

> **Dhruv speaks:**  
> "Good morning respected faculty members, evaluators, and colleagues.  
> 
> My name is **Dhruv**, and along with my team members **Darshi** and **Kirtan**, we are excited to present our Machine Learning Essentials project: **'Indian Railways Train Delay Prediction and Network Punctuality Analytics'**.  
> 
> We have structured our presentation and live system demonstration into three smooth parts. I will introduce our real-world problem and demonstrate our live prediction engine; Darshi will explain our data preprocessing and feature engineering; and Kirtan will walk through our model comparisons, LightGBM tuning, and error diagnostics."

---

### [SHOW PPT SLIDE 2: Problem Statement & Project Objectives]

> **Dhruv speaks:**  
> "Indian Railways operates one of the largest rail transportation networks in the world, carrying over 23 million passengers daily across 68,000 route kilometers. However, network congestion, weather disruptions like dense winter fog, and rolling stock turnaround delays often cause severe operational bottlenecks.  
> 
> In traditional railway management, delays are handled reactively—station masters only realize a train is delayed after it gets stuck at a signal or junction.  
> 
> Our machine learning objective is to transform this into **proactive delay risk forecasting**. Specifically, we formulate a binary classification problem: predicting whether a passenger train will suffer an arrival delay exceeding **15 minutes** at its final destination terminus.  
> 
> If the delay is more than 15 minutes, the target is labeled `1` for Delayed; otherwise, `0` for On-Time, strictly adhering to Ministry of Railways punctuality standards."

---

### [SHOW PPT SLIDE 3: Dataset Overview & Quality Assessment]

> **Dhruv speaks:**  
> "Our project is built upon comprehensive Indian Railways operational records sourced from Kaggle. The full dataset contains over 1.5 million train journey rows across 45 raw features.  
> 
> For our experimental research and model development, we used a stratified sample of 10,000 operational records, followed by a rigorous 80/20 train-test split.  
> 
> We observed a natural class imbalance: approximately **72.16% of journeys in the historical record experienced delays**, while **27.84% arrived on-time**.  
> 
> During initial data inspection, we identified constant zero-variance features like `is_overloaded`, which we pruned. More importantly, we identified direct target leakage columns—such as `delay_minutes` and `primary_delay_cause`—which are recorded *after* a train arrives. We strictly quarantined these leakage features so our models only make predictions using information available prior to departure.  
> 
> Now, let me switch to our live interactive web platform to demonstrate how this works in real time."

---

### [SWITCH TO LIVE WEB APP: Module 1 — 🏠 Overview & Mission Control]

> **Dhruv speaks:**  
> "Here on screen is our live web application, built with Streamlit using an enterprise Deep Dark and Elegant Gold design system.  
> 
> On this **Overview & Mission Control** dashboard, railway operators can immediately see key network telemetry: our 10,000 experimental dataset records, the 85.85% validation accuracy of our champion LightGBM model, and the 16 operational railway zones monitored across India."

---

### [SWITCH TO LIVE WEB APP: Module 2 — 🎯 Train Delay Predictor]

> **Dhruv speaks:**  
> "Now, let us navigate to our core prediction engine: the **Train Delay Predictor**.  
> 
> To demonstrate the system's sensitivity, we have pre-configured two realistic operational scenarios."

#### [ACTION: In Preset Scenarios dropdown, click Preset 1: Premier Vande Bharat Express]
> **Dhruv speaks:**  
> "First, let's select **Preset 1: Premier Vande Bharat Express**.  
> Notice the parameters: 130 km/h average speed, Northern Railway (NR) corridor, clear weather, modern LHB rake, zero incoming rake delay, and an 88.5% historical route punctuality track record.  
> Let me click **'Run ML Delay Prediction'**."

#### [ACTION: Click 'Run ML Delay Prediction']
> **Dhruv speaks:**  
> "The model returns an estimated delay probability of **3.3%**, generating a **GREEN: ON-TIME EXPECTED** status. The system recommends standard priority dispatch."

#### [ACTION: In Preset Scenarios dropdown, click Preset 2: Monsoon Mail/Express]
> **Dhruv speaks:**  
> "Now, let's test a high-friction bottleneck scenario: **Preset 2: Howrah–Amritsar Mail in Heavy Monsoon**.  
> Here we have a slow 38 km/h schedule, Eastern Railway zone with 88% congestion, single-track bottlenecks, 24 halts, heavy monsoon rainfall, and a late incoming turnaround rake.  
> Let me click **'Run ML Delay Prediction'** again."

#### [ACTION: Click 'Run ML Delay Prediction']
> **Dhruv speaks:**  
> "The probability spikes immediately to **98.7%**, triggering a **RED ALERT: HIGH DELAY RISK**. The system automatically advises operational dispatchers to prioritize junction clearance and arrange relief buffers.  
> 
> Every prediction is automatically logged into our session audit history.  
> 
> Now, I hand over the presentation to **Darshi**, who will explain our exploratory data analysis, data cleaning, and feature engineering pipeline."

---

## 🎙️ PART 2: DARSHI — DATASET UNDERSTANDING, EDA, PREPROCESSING & FEATURE ENGINEERING
*(Target Speaking Duration: 2.5 minutes)*

### [SHOW PPT SLIDE 4: Exploratory Data Analysis & Key Insights]

> **Darshi speaks:**  
> "Thank you, Dhruv. Good morning everyone. I am **Darshi**, and I will explain how we analyzed and prepared our data for machine learning.  
> 
> Raw real-world data cannot be fed directly into machine learning algorithms. Before training any model, we must thoroughly understand feature distributions, patterns, and anomalies.  
> 
> During Exploratory Data Analysis, we uncovered three critical operational insights:  
> 1. **Kinematic Speed Threshold:** Trains operating at an average speed below **50 km/h** had an **88.4% delay probability**, whereas trains maintaining over **75 km/h** had less than a **15% delay rate**.  
> 2. **Zonal Network Friction:** Northern Railway (NR), North Central Railway (NCR), and Eastern Railway (ER) experience severe congestion indices exceeding 0.85, primarily exacerbated by winter fog in the Indo-Gangetic plains.  
> 3. **Cascading Turnaround Impact:** When a shared rake arrives late at an origin station (`late_incoming_rake = 1`), the likelihood of downstream journey delay surges to **91.2%**, proving that delays cascade across network schedules."

---

### [SHOW PPT SLIDE 5: Data Preprocessing & Outlier Treatment]

> **Darshi speaks:**  
> "To prepare this data reliably, we built a 4-stage preprocessing architecture using pure Pandas and NumPy:  
> 
> 1. **Zero-Variance Dropping:** Features like `is_overloaded` were identical for all records and provided zero analytical value, so they were removed.  
> 2. **Leakage Quarantine:** As Dhruv highlighted, features recorded post-journey were isolated to guarantee zero target leakage.  
> 3. **Outlier Treatment via NumPy IQR Winsorization:** Rather than deleting rows with extreme journey distances or hours—which would discard valuable train journeys—we calculated Interquartile Range (IQR) bounds strictly on the training set:  
>    - `distance_km` was capped at **1,466 km**.  
>    - `scheduled_travel_hours` was capped at **24.9 hours**.  
> 4. **Feature Encoding & Scaling:** High-cardinality categorical variables like train types and railway zones were one-hot encoded into sparse binary columns, and continuous features were standardized using training-set mean and variance."

---

### [SHOW PPT SLIDE 6: Feature Engineering & Selection Methodology]

> **Darshi speaks:**  
> "Feature engineering is where domain knowledge meets machine learning. We engineered 5 high-impact railway features:  
> 
> 1. **`avg_speed_kmh`:** Scheduled distance divided by travel hours.  
> 2. **`network_vulnerability`:** Zonal congestion weighted by high-density route flags and track doubling.  
> 3. **`equipment_age_index`:** Combined average age of locomotive and passenger coaches.  
> 4. **`rake_turnaround_risk`:** Interaction between shared rakes and late incoming arrivals.  
> 5. **Cyclical Time Trigonometry:** Because hour 23 and hour 0 are consecutive in real time, we encoded departure hours and weekdays into sine and cosine components: `hour_sin` and `hour_cos`.  
> 
> Now, let me demonstrate these preprocessing steps directly in our web application."

---

### [SWITCH TO LIVE WEB APP: Module 4 — 🔍 Exploratory Data Analysis (EDA)]

> **Darshi speaks:**  
> "In **Module 4: Exploratory Data Analysis**, operators can inspect the empirical target distribution chart, showing our 72% delayed versus 28% on-time baseline split, alongside the correlation matrix demonstrating the strong inverse relationship between average speed and delay probability."

---

### [SWITCH TO LIVE WEB APP: Module 5 — ⚙️ Data Preprocessing & Pipeline]

> **Darshi speaks:**  
> "In **Module 5: Data Preprocessing**, we display the complete 4-stage data pipeline architecture. Operators can view our exact NumPy IQR Winsorization bounds and inspect the data leakage quarantine protocol that protects our model against future-information bias."

---

### [SWITCH TO LIVE WEB APP: Module 6 — 🧬 Feature Engineering & Selection]

> **Darshi speaks:**  
> "Finally, in **Module 6: Feature Engineering**, we present the mathematical formulas and operational rationale for all five engineered domain features.  
> 
> With our dataset thoroughly cleaned, engineered, and encoded into 8,111 aligned sparse columns, it was ready for model training.  
> 
> I now hand over to **Kirtan**, who will explain our algorithm benchmarks, LightGBM tuning, error analysis, and project conclusions."

---

## 🎙️ PART 3: KIRTAN — MODEL BENCHMARKS, EVALUATION, ERROR ANALYSIS & CONCLUSION
*(Target Speaking Duration: 3.0 minutes)*

### [SHOW PPT SLIDE 7: Machine Learning Workflow & Baseline Model]

> **Kirtan speaks:**  
> "Thank you, Darshi. Good morning respected evaluators. I am **Kirtan**, and I will walk you through our model development, benchmark evaluations, error diagnostics, and practical takeaways.  
> 
> In machine learning, an advanced model must never be deployed without first benchmarking against a simple reference model.  
> 
> We implemented a **Dummy Majority-Class Baseline Classifier**, which always predicts the majority class—that a train will be delayed. Because 72.15% of records are delayed, the baseline achieves 72.15% accuracy and 100% recall, but has a **ROC-AUC of exactly 0.5000** and a Precision of only 72.15%. It has zero discriminative power. Any viable ML model had to significantly outperform this baseline."

---

### [SHOW PPT SLIDE 8: Model Development & Hyperparameter Tuning]

> **Kirtan speaks:**  
> "We trained and evaluated four distinct supervised learning algorithms representing diverse mathematical families:  
> 1. **Decision Tree (CART):** Highly interpretable, single decision rule hierarchy.  
> 2. **Random Forest:** Ensemble bagging of 150 de-correlated trees to reduce variance.  
> 3. **L2-Regularized Logistic Regression:** Linear probabilistic boundary with calibrated sigmoid scoring.  
> 4. **LightGBM (Light Gradient Boosting Machine):** Advanced gradient boosting using leaf-wise tree growth and histogram-based binning.  
> 
> For LightGBM, we performed hyperparameter tuning across learning rate, tree depth, and regularizers. The optimal configuration was:  
> - `learning_rate: 0.05`  
> - `num_leaves: 31`  
> - `n_estimators: 200`  
> - `subsample: 0.8`  
> - `colsample_bytree: 0.8`"

---

### [SHOW PPT SLIDE 9: Performance Comparison & Benchmark Analysis]

> **Kirtan speaks:**  
> "Here is our definitive model benchmark table evaluated on the untouched validation set of 2,000 journeys:  
> 
> - **Baseline Dummy:** 72.15% Accuracy | 0.5000 ROC-AUC  
> - **Decision Tree:** 81.30% Accuracy | 0.8593 ROC-AUC  
> - **Random Forest:** 78.70% Accuracy | 0.8854 ROC-AUC  
> - **Logistic Regression:** 85.70% Accuracy | **0.9229 ROC-AUC**  
> - **Tuned LightGBM (Champion):** **85.85% Accuracy | 88.72% Precision | 92.10% Recall | 0.9038 F1-Score | 0.9121 ROC-AUC**  
> 
> While Logistic Regression achieved a slightly higher ROC-AUC, **LightGBM delivered the highest overall accuracy (85.85%), highest Recall (92.10%), and highest F1-score (0.9038)**, making it our definitive champion model."

---

### [SHOW PPT SLIDE 10: Model Evaluation, ROC-AUC & Confusion Matrix]

> **Kirtan speaks:**  
> "Looking at the Confusion Matrix for LightGBM across 2,000 test journeys at a standard 0.50 threshold:  
> - **True Positives:** 1,329 delayed trains correctly flagged.  
> - **True Negatives:** 388 on-time trains correctly identified.  
> - **False Positives:** 169 on-time trains predicted as delayed (8.45% error rate).  
> - **False Negatives:** 114 delayed trains predicted as on-time (5.70% error rate).  
> 
> In passenger railway dispatching, a **False Negative is far more hazardous than a False Positive**—because missing a delayed train creates unscheduled platform congestion, while a False Positive simply leads to precautionary monitoring. Achieving a **92.10% Recall** ensures that over 9 out of 10 delayed trains are successfully caught before arriving."

---

### [SHOW PPT SLIDE 11: Error Analysis, Limitations & Future Work]

> **Kirtan speaks:**  
> "During error analysis, we examined the 114 False Negatives. They predominantly occurred during sudden unforeseen events—such as unexpected signal failure or localized weather changes—which cannot be anticipated from pre-departure scheduled data alone.  
> 
> **Key Limitations:**  
> 1. Our model operates on pre-departure schedules; it does not currently ingest live GPS telemetry during the journey.  
> 2. Punctuality is subject to dynamic cascading delays from shared freight corridors.  
> 
> **Future Work:** Integrating live GPS feeds and IoT track-sensor telemetry to enable dynamic mid-journey delay re-estimation.  
> 
> Let me quickly show these evaluation tools in our live application."

---

### [SWITCH TO LIVE WEB APP: Module 7, 8, 9, 10 — Benchmarks, Confusion Matrix & Feature Importance]

> **Kirtan speaks:**  
> "In **Module 7: Model Benchmarks**, operators can view the side-by-side performance bar chart confirming LightGBM's superior F1-score.  
> 
> In **Module 8: Evaluation Metrics**, we built an **interactive threshold explorer**. If a railway division is especially risk-averse, operators can adjust the decision threshold from 0.50 down to 0.35, pushing Recall above 96%.  
> 
> In **Module 9: Error Analysis**, we break down the causes of misclassification with actionable operational mitigations.  
> 
> And in **Module 10: Feature Importance**, our tree-split ranking confirms that our top predictors are:  
> 1. `avg_speed_kmh` (570 splits)  
> 2. `network_vulnerability` (309 splits)  
> 3. `route_historical_ontime_pct` (307 splits)  
> 4. `equipment_age_index` (221 splits)  
> 5. `late_incoming_rake` (220 splits)  
> 
> All five top features were engineered by our team!"

---

### [SHOW PPT SLIDE 12: Project Conclusion & Q&A]

> **Kirtan speaks:**  
> "To conclude: our team has developed an end-to-end Machine Learning pipeline that:  
> 1. Accurately predicts train arrival delays with **85.85% accuracy and 92.10% recall**.  
> 2. Quarantines data leakage and prevents overfitting with rigorous IQR Winsorization.  
> 3. Deploys a fully functional, tested 13-module web application for real-time dispatch decision support.  
> 
> On behalf of Dhruv, Darshi, and myself, thank you for your time and guidance. We are now open to your questions."

---

## 📋 Speaker Summary Card for Viva Day

| Speaker | Primary Responsibilities | Key Numbers to Remember |
| :--- | :--- | :--- |
| **Dhruv** | Intro, Problem Definition, Dataset Scope, Live Predictor Demo | • 15 min delay threshold (`is_delayed`)<br/>• 10,000 experimental sample (80/20 split)<br/>• 72.16% delayed vs 27.84% on-time<br/>• Vande Bharat: 3.3% risk; Monsoon: 98.7% risk |
| **Darshi** | EDA Findings, Data Preprocessing, IQR Winsorization, 5 Domain Features | • Speed < 50 km/h: 88.4% delayed; Speed > 75 km/h: <15%<br/>• Distance capped at 1,466 km; Hours capped at 24.9 hrs<br/>• 8,111 sparse one-hot encoded columns<br/>• Dropped `is_overloaded`, quarantined `delay_minutes` |
| **Kirtan** | Algorithms, Tuning, Benchmark Table, Confusion Matrix, Error Analysis | • Baseline: 72.15% acc, 0.5000 AUC<br/>• Logistic Reg: 85.70% acc, 0.9229 AUC<br/>• Champion LightGBM: **85.85% acc, 92.10% recall, 0.9038 F1**<br/>• TP=1,329, TN=388, FP=169, FN=114<br/>• Top split features: `avg_speed_kmh` (570), `network_vulnerability` (309) |
