# ECSCI24302 – Machine Learning Essentials
## PROJECT-BASED LEARNING (PBL) FINAL PROJECT REPORT

---

# End-to-End Machine Learning Project: Indian Railways Train Delay Prediction and Network Punctuality Analytics

**Course Code:** ECSCI24302 – Machine Learning Essentials  
**Academic Year:** 2026–2027  
**Submission Date:** October 2026  
**Repository Directory:** `D:\ML PROJECT\ml`  
**Project Type:** Supervised Machine Learning – Binary Classification

---

## Abstract / Project Summary

Indian Railways operates a complex transportation network in which punctuality is affected by train schedules, infrastructure, seasonal conditions, rolling-stock characteristics, congestion, and historical operational performance. This project develops an end-to-end machine learning workflow to predict the probability of a train journey being delayed.

The problem is formulated as supervised binary classification, with `is_delayed` as the target variable. The workflow includes data exploration, data cleaning, leakage prevention, feature engineering, stratified train-validation splitting, categorical encoding, numerical standardization, model development, hyperparameter tuning, model evaluation, error analysis, and test-set inference.

Four principal machine learning algorithms were explored: Logistic Regression, Decision Tree, Random Forest, and LightGBM, alongside a Dummy Classifier baseline. Tuned versions of Random Forest and LightGBM were also evaluated. To accommodate available computational resources, model development used a sample of 10,000 records from the training dataset, divided into training and validation partitions using an 80:20 stratified split.

Among the evaluated models, Tuned LightGBM achieved the highest validation accuracy of 85.85%, recall of 92.10%, and F1-score of 0.9038. Logistic Regression achieved the highest ROC-AUC of 0.9229. Tuned LightGBM was retained for the final prediction workflow based on its accuracy, recall, and F1-score.

The project also includes a single-journey prediction demonstration that produces delay probabilities and operational risk labels. A submission file containing predictions for 375,000 test journeys was generated and passed structural validation. The reported metrics represent the sampled model-development experiment and should not be interpreted as performance measurements on the entire training dataset or as proof of real-world railway forecasting accuracy.

---

## 1. Introduction

Train punctuality is an important indicator of transportation efficiency, passenger satisfaction, and railway operational performance. Delays can arise from several interacting factors, including infrastructure constraints, weather conditions, station congestion, rolling-stock availability, scheduled stops, and late incoming trains.

Machine learning provides a way to identify patterns in historical operational data and estimate the likelihood of a future journey being delayed. Such predictions may help operational teams identify journeys that require additional attention and investigate potential sources of disruption.

This project applies data analysis and machine learning techniques to the Indian Railways train-delay prediction dataset. The implementation emphasizes a reproducible workflow, leakage prevention, comparative model evaluation, and prediction generation.

---

## 2. Problem Statement and Motivation

### 2.1 Problem Statement

The objective is to develop a binary classification model that estimates whether a train journey will be delayed based on its available operational and infrastructure features.

**Target variable:** `is_delayed`

- `1`: Journey classified as delayed.
- `0`: Journey classified as on time.

The target definition used by the project is based on whether the destination arrival delay exceeds 15 minutes.

### 2.2 Objectives

1. Understand the structure and characteristics of the dataset.
2. Perform data cleaning and exploratory data analysis.
3. Prevent data leakage by excluding information unavailable at prediction time.
4. Engineer features that represent railway operating conditions.
5. Train and compare multiple classification algorithms.
6. Tune Random Forest and LightGBM using cross-validation.
7. Evaluate models using accuracy, precision, recall, F1-score, and ROC-AUC.
8. Examine classification errors and feature importance.
9. Generate predictions for the unseen test dataset.
10. Demonstrate predictions for individual train journeys.

### 2.3 Motivation

Early identification of journeys with a high predicted delay probability could support operational planning and help prioritize further investigation. The model is intended as an analytical decision-support prototype, not as a replacement for railway control systems or expert operational judgment.

---

## 3. Dataset Description and Source

### 3.1 Dataset Files

The project uses the Indian Railways train-delay prediction dataset associated with the Kaggle competition *Indian Railways: Predict Train Delay*.

The dataset files used by the project are:

| File | Purpose |
|---|---|
| `ir_train.csv` | Training dataset containing the target variable |
| `ir_test.csv` | Unlabeled test dataset used for prediction |
| `ir_data_dictionary.csv` | Documentation of dataset attributes |
| `ir_sample_submission.csv` | Reference submission structure |
| `submission.csv` | Generated predictions for the test dataset |

The repository keeps the large input CSV files in the local `data/` directory, which is excluded from Git through `.gitignore`.

### 3.2 Dataset Dimensions

The supplied dataset is described as containing approximately:

- Training dataset: 1,500,000 records and 45 columns.
- Test dataset: 375,000 records and 42 columns.

**Important distinction:** Although the full training dataset contains approximately 1.5 million records, the model-development workflow documented in this report uses a sample of 10,000 training records to accommodate available computational resources.

### 3.3 Feature Categories

The dataset contains several categories of features:

- Journey identification and train information.
- Departure date, month, day, and hour.
- Railway zone and station categories.
- Route distance and scheduled travel duration.
- Scheduled stops and track characteristics.
- Electrification and traction information.
- Weather and seasonal indicators.
- Rolling-stock age and maintenance-related information.
- Historical route punctuality and congestion indicators.

The target variable `is_delayed` is present in the training dataset but is not available as a feature in the test dataset.

---

## 4. Data Understanding and Exploratory Data Analysis

### 4.1 Target Variable

The target variable represents whether a journey is delayed or on time. The classification problem is potentially affected by class imbalance, meaning the two target classes do not necessarily occur with equal frequency.

The Dummy Classifier is included to provide a baseline against which the trained models can be compared.

### 4.2 Data Quality Checks

The preprocessing workflow performs data cleaning and feature checks through the shared functions in `utils.py`.

The project considers the following data quality issues:

1. Missing or invalid feature values.
2. Identifier columns that should not be used as predictive inputs.
3. Features with no useful variation.
4. High-cardinality categorical features.
5. Features that could cause data leakage.
6. Numerical columns requiring outlier treatment or standardization.

The complete dataset and the sampled model-development dataset should be distinguished when reporting data quality statistics. Statistics calculated on a sample must not be presented as though they were calculated over all 1.5 million training records.

### 4.3 Exploratory Analysis

The EDA workflow is intended to investigate relationships between delay outcomes and operational characteristics, including:

- Railway zones and train categories.
- Seasonal and weather-related conditions.
- Route distance and scheduled travel duration.
- Infrastructure and track characteristics.
- Incoming-rake delays.
- Historical route punctuality.

These analyses help identify patterns that may be useful for feature engineering and model interpretation. Observed associations do not, by themselves, establish that a particular feature causes train delays.

---

## 5. Data Preprocessing and Data Leakage Prevention

### 5.1 Data Cleaning

The project uses shared Pandas-based preprocessing functions from `utils.py`:

- `clean_data_pandas()`
- `engineer_features_pandas()`
- `handle_outliers_iqr_numpy()`

These functions are used to clean records, create derived features, and apply IQR-based outlier treatment to selected numerical columns.

The outlier-treatment step considers available features such as distance, scheduled travel duration, scheduled restrictions, and rolling-stock age.

### 5.2 Data Leakage Prevention

Data leakage occurs when a model uses information that would not be available at the time predictions are intended to be made.

The following attributes require special treatment:

- `delay_minutes`: Records the delay outcome and may directly reveal information used to define the target.
- `primary_delay_cause`: Describes the cause of a delay and may be assigned after the journey.

These post-event variables must not be used as predictive features when they are unavailable at prediction time. The shared cleaning function is responsible for excluding leakage-prone fields from the model feature matrix.

The target variable `is_delayed` is separated from the feature matrix before training.

### 5.3 Train-Validation Split

The model-development sample is divided using stratified sampling:

- Training partition: 80% of the 10,000-record sample.
- Validation partition: 20% of the 10,000-record sample.
- Random state: 42.
- Stratification: Based on `is_delayed`.

This gives approximately 8,000 training records and 2,000 validation records, subject to the exact split implementation.

Stratification helps preserve the target-class proportions across the two partitions.

### 5.4 Categorical Encoding

Categorical variables are encoded using Pandas `get_dummies()`.

The resulting validation features are aligned with the columns generated from the training partition. This ensures that the validation data has the same feature schema as the training data.

The high-cardinality identifier-like feature `train_number` is excluded from one-hot encoding to control memory consumption. This reduces the dimensionality of the feature matrix but may also remove useful train-specific predictive information.

### 5.5 Numerical Standardization

Numerical features are standardized using the training partition's mean and standard deviation.

The transformation is:

\[
z = \frac{x-\mu_{\text{train}}}{\sigma_{\text{train}}}
\]

where:

- \(x\) is the original feature value.
- \(\mu_{\text{train}}\) is the training mean.
- \(\sigma_{\text{train}}\) is the training standard deviation.

A zero standard deviation is handled to avoid division by zero. The same training-derived statistics are used when transforming validation and test features.

The implementation uses Pandas and NumPy operations and converts numerical columns to a floating-point representation before assigning standardized decimal values.

---

## 6. Feature Engineering and Feature Selection

Feature engineering creates derived variables that may represent meaningful railway operating conditions.

The shared feature-engineering function is `engineer_features_pandas()`.

Examples of useful derived features include:

### 6.1 Average Scheduled Speed

\[
\text{avg\_speed\_kmh}
=
\frac{\text{distance\_km}}{\text{scheduled\_travel\_hours}}
\]

This feature represents the average speed implied by the scheduled journey distance and duration. It may help distinguish short, fast journeys from longer journeys with more scheduled travel time.

### 6.2 Stop Density

\[
\text{stops\_density}
=
\frac{\text{num\_scheduled\_stops}}
{\text{distance\_km}/100+0.1}
\]

This approximates the density of scheduled stops relative to route distance.

### 6.3 Average Stop Distance

\[
\text{avg\_stop\_distance}
=
\frac{\text{distance\_km}}
{\text{num\_scheduled\_stops}+1}
\]

This represents the average distance per scheduled stop interval.

### 6.4 Weather Severity

Seasonal severity, monsoon indicators, and fog-related variables can be combined to represent environmental risk.

### 6.5 Network Vulnerability

Route congestion, high-density network indicators, and track characteristics can help represent infrastructure-related vulnerability.

### 6.6 Rolling-Stock Age

Locomotive and coach ages can be combined to describe the age profile of the equipment used for a journey.

### 6.7 Historical Delay Risk

Historical on-time performance can be transformed into a risk-oriented feature:

\[
\text{historical\_delay\_risk}
=
\frac{100-\text{route\_historical\_ontime\_pct}}{100}
\]

A lower historical on-time percentage corresponds to a higher value of this derived risk measure.

The actual set of engineered features used by the final model is determined by the implementation in `utils.py` and the resulting feature matrix.

---

## 7. Machine Learning Methodology

### 7.1 Algorithms Evaluated

The project evaluates a baseline classifier and multiple supervised classification algorithms.

**1. Dummy Classifier**

Provides a simple reference model that predicts according to a baseline strategy. It helps determine whether more sophisticated models provide useful discrimination.

**2. Logistic Regression**

A linear classification algorithm that estimates class probabilities using a logistic function. It provides a useful baseline for comparing linear decision boundaries against nonlinear models.

**3. Decision Tree**

A tree-based classifier that learns decision rules through recursive feature splits. It can model nonlinear relationships but may overfit if its complexity is not controlled.

**4. Random Forest**

An ensemble of decision trees that combines predictions from multiple trees. It can capture nonlinear patterns but may require substantial memory and computation.

**5. LightGBM**

A gradient-boosted tree algorithm designed for efficient learning on tabular datasets. It builds trees sequentially, with each stage attempting to improve the current ensemble.

**6. Tuned Random Forest and Tuned LightGBM**

Hyperparameter tuning is performed for the two ensemble algorithms to explore alternative configurations.

### 7.2 Computational Configuration

To reduce memory usage and prevent excessive computation, the current model-development configuration uses:

- A 10,000-record training sample.
- A stratified 80:20 training-validation split.
- Pandas-based one-hot encoding.
- Exclusion of `train_number` from the one-hot encoded feature matrix.
- Numerical standardization using training statistics.
- Reduced randomized hyperparameter searches.

Consequently, the current reported metrics describe this computationally constrained experiment and may differ from results obtained by training on the complete dataset.

---

## 8. Model Evaluation Metrics

The following metrics are used to evaluate classification performance.

### 8.1 Accuracy

The proportion of all predictions that are correct.

\[
\text{Accuracy}
=
\frac{TP+TN}{TP+TN+FP+FN}
\]

Accuracy provides an overall summary but may be misleading when the target classes are imbalanced.

### 8.2 Precision

The proportion of predicted positive cases that are actually positive.

\[
\text{Precision}
=
\frac{TP}{TP+FP}
\]

Higher precision means fewer false alarms among journeys predicted to be delayed.

### 8.3 Recall

The proportion of actual positive cases correctly identified by the model.

\[
\text{Recall}
=
\frac{TP}{TP+FN}
\]

Higher recall means the model identifies a greater proportion of delayed journeys.

### 8.4 F1-Score

The harmonic mean of precision and recall.

\[
F_1 =
2 \times
\frac{\text{Precision}\times\text{Recall}}
{\text{Precision}+\text{Recall}}
\]

The F1-score balances the precision and recall of the positive class.

### 8.5 ROC-AUC

ROC-AUC measures how effectively a model ranks positive examples above negative examples across classification thresholds.

A score near 0.5 indicates discrimination similar to random ranking, while a higher score indicates stronger ranking discrimination.

---

## 9. Hyperparameter Tuning

Randomized search with cross-validation is used to tune Random Forest and LightGBM.

The final reduced tuning configuration uses:

- Two candidate parameter combinations per randomized search.
- Two-fold cross-validation.
- ROC-AUC as the tuning objective.
- A tuning sample of up to 10,000 training-partition records.
- Fixed random state for reproducibility.

### 9.1 Random Forest

The search explores selected values for parameters such as:

- `n_estimators`
- `max_depth`
- `min_samples_split`

The best estimator returned by the randomized search is subsequently fitted on the available training partition and evaluated on the validation partition.

### 9.2 LightGBM

The search explores selected values for parameters such as:

- `learning_rate`
- `num_leaves`
- `max_depth`

The best estimator returned by the search is subsequently fitted on the available training partition and evaluated on the validation partition.

The exact best parameters and cross-validation scores should be taken from the successfully executed notebook output. Earlier tuning configurations and interrupted searches are not used as evidence for the final reported metrics.

---

## 10. Results and Model Comparison

The following results were obtained from the model-comparison table in Notebook 3. They represent the validation performance of the current sampled model-development experiment.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Dummy Baseline | 0.7215 | 0.7215 | 1.0000 | 0.8382 | 0.5000 |
| Logistic Regression | 0.8570 | 0.8901 | 0.9148 | 0.9023 | 0.9229 |
| Decision Tree | 0.8130 | 0.8585 | 0.8870 | 0.8725 | 0.8593 |
| Random Forest | 0.7730 | 0.7640 | 0.9917 | 0.8631 | 0.8831 |
| LightGBM | 0.8560 | 0.8889 | 0.9148 | 0.9016 | 0.9152 |
| Tuned Random Forest | 0.7870 | 0.7783 | 0.9854 | 0.8697 | 0.8854 |
| Tuned LightGBM | **0.8585** | 0.8872 | **0.9210** | **0.9038** | 0.9121 |

### 10.1 Results Interpretation

**Tuned LightGBM**

- Achieved the highest validation accuracy of 85.85%.
- Achieved the highest recall of 92.10%.
- Achieved the highest F1-score of 0.9038.
- Achieved a ROC-AUC of 0.9121.

**Logistic Regression**

- Achieved validation accuracy of 85.70%.
- Achieved an F1-score of 0.9023.
- Achieved the highest ROC-AUC of 0.9229.

**Decision Tree**

- Achieved validation accuracy of 81.30%.
- Achieved a ROC-AUC of 0.8593.
- Demonstrates the ability to model nonlinear relationships but performed below the strongest alternatives in this experiment.

**Random Forest**

- Achieved validation accuracy of 77.30%.
- Achieved recall of 99.17%.
- Its high recall is accompanied by lower precision and accuracy compared with the leading models.

**Dummy Baseline**

- Achieved accuracy of 72.15%.
- Achieved ROC-AUC of 0.5000.
- Provides a useful reference for understanding the performance of the trained models.

### 10.2 Selected Model

Tuned LightGBM is selected for the final prediction workflow because it achieved the highest validation accuracy, recall, and F1-score among the evaluated models.

Logistic Regression achieved the highest ROC-AUC. This indicates that the best model depends on the evaluation objective: Tuned LightGBM performed best on several threshold-based metrics, while Logistic Regression showed stronger overall ranking discrimination.

The difference between the leading models is relatively small, and the results should be interpreted cautiously because model development used a 10,000-record sample.

---

## 11. Error Analysis

Error analysis examines the types of mistakes made by the classifier.

The Notebook 3 workflow includes an analysis of validation predictions and their associated railway zones and train categories.

### 11.1 False Positives

A false positive occurs when a journey is predicted to be delayed but its actual target is on time.

Potential operational implications include unnecessary alerts, additional investigation, or inefficient allocation of operational resources.

### 11.2 False Negatives

A false negative occurs when a journey is predicted to be on time but its actual target indicates a delay.

False negatives may be particularly important when the objective is to identify journeys requiring early operational attention.

### 11.3 Error Analysis by Railway Zone and Train Type

The analysis groups misclassified validation journeys by:

- `zone_abbr`
- `train_type`
- Error category

These groupings can help identify segments where further investigation may be useful.

Specific conclusions about which zones or train types have the most errors should be reported only after examining the actual generated charts and counts. Error counts should also be interpreted in relation to the number of journeys in each group.

---

## 12. Model Interpretation and Feature Importance

Feature importance helps identify which input variables contribute most to the fitted tree-based model's split decisions.

The project includes a LightGBM feature-importance visualization based on the trained model's `feature_importances_` attribute.

Feature importance can help investigate whether the model relies on operationally meaningful variables, such as:

- Historical route punctuality.
- Seasonal and weather indicators.
- Route congestion.
- Scheduled travel duration and distance.
- Incoming-rake status.
- Rolling-stock characteristics.

The actual ranking must be taken from the generated feature-importance output. Feature importance alone does not establish causation and should not be interpreted as proof that changing a feature will change the delay outcome.

---

## 13. Final Predictions and Single-Journey Demonstration

### 13.1 Test-Set Inference

The selected Tuned LightGBM model was used to generate predictions for the test dataset.

The generated output file is:

`data/submission.csv`

The file contains two columns:

- `journey_id`: The identifier of the test journey.
- `is_delayed`: The predicted probability that the journey belongs to the delayed class.

### 13.2 Submission Validation

The generated submission passed the following structural checks:

| Validation Check | Result |
|---|---|
| File exists | Passed |
| Number of rows | 375,000 |
| Number of columns | 2 |
| Expected column names | Passed |
| Missing journey IDs | 0 |
| Missing predictions | 0 |
| Duplicate journey IDs | 0 |
| Minimum predicted probability | 0.0223 |
| Maximum predicted probability | 0.9949 |

The predicted values are within the valid probability range of 0 to 1.

These checks establish that the generated file has the expected structure and valid numerical predictions. They do not establish the predictive accuracy of the model on the unlabeled test dataset.

### 13.3 Single-Journey Prediction Demonstration

The project includes a function named `predict_single_journey()`.

The function accepts a dictionary describing a journey, applies the cleaning and feature-engineering workflow, aligns the features with the trained model's expected columns, and generates a predicted delay probability.

The demonstration uses three operational risk labels:

- **ON-TIME EXPECTED:** Probability below 40%.
- **MODERATE DELAY RISK:** Probability from 40% through 65%.
- **HIGH DELAY RISK:** Probability above 65%.

These thresholds are demonstration rules selected by the project implementation, not official Indian Railways operational thresholds.

The executed demonstration produced the following outputs:

| Demonstration Scenario | Predicted Delay Probability | Operational Status | Alert |
|---|---:|---|---|
| Vande Bharat Express, Northern Railway | 3.3% | ON-TIME EXPECTED | GREEN |
| Mail/Express, Eastern Railway | 98.7% | HIGH DELAY RISK | RED |

These are predictions from the trained model for the supplied example inputs. They are illustrative outputs and should not be interpreted as verified forecasts for actual train services.

---

## 14. Project Limitations and Future Improvements

### 14.1 Limited Training Sample

The current model-development experiment uses 10,000 training records rather than the entire 1.5-million-record training dataset.

**Future improvement:** Train and evaluate models on progressively larger samples or the full dataset using an appropriate memory-efficient pipeline.

### 14.2 High-Cardinality Feature Exclusion

The `train_number` feature is excluded from one-hot encoding to avoid an excessive number of columns and high memory consumption.

**Future improvement:** Investigate alternative representations, such as carefully designed categorical encodings or models with native categorical-feature support.

### 14.3 Computational Constraints

Hyperparameter tuning uses a reduced search configuration to limit runtime.

**Future improvement:** Explore larger search spaces, more cross-validation folds, and systematic model selection on suitable hardware.

### 14.4 Lack of Real-Time Operational Telemetry

The current workflow relies on the supplied dataset and its available features.

**Future improvement:** Investigate integration of real-time train-location information, updated timetable data, and operational telemetry, subject to data availability and permission.

### 14.5 Weather Resolution

Weather-related features may not capture localized or rapidly changing conditions.

**Future improvement:** Investigate the use of more detailed weather observations and time-aligned environmental data.

### 14.6 Generalization and Calibration

The validation results are based on a sampled dataset. The reported submission probabilities have not been independently validated against labels for the test dataset.

**Future improvement:** Evaluate performance on additional held-out data and assess probability calibration before using predicted probabilities for operational decisions.

### 14.7 Model Artifact Reproducibility

The preprocessing and model artifacts must remain consistent with the final training workflow.

**Future improvement:** Save the fitted model together with its exact feature schema, encoding rules, scaling statistics, and version information. Verify that a fresh process can load the artifact and reproduce predictions.

---

## 15. Viva Voce Preparation

### Q1. Why is accuracy alone insufficient for evaluating this model?

**Answer:** Accuracy summarizes the proportion of correct predictions, but it does not describe the types of errors a model makes. Precision measures the reliability of positive predictions, recall measures how many actual delayed journeys are identified, F1-score balances precision and recall, and ROC-AUC measures ranking discrimination across classification thresholds. These metrics provide a more complete view of model performance.

### Q2. What is data leakage?

**Answer:** Data leakage occurs when a model uses information that would not be available at the time of prediction. In this project, post-event fields such as `delay_minutes` and `primary_delay_cause` must be excluded from predictive features when they reveal information about the completed journey. Training-derived encoding and scaling parameters should also be reused for validation and test data rather than learned from those partitions.

### Q3. Why was the dataset sampled?

**Answer:** The original dataset is large, and high-cardinality one-hot encoding can consume substantial memory. A 10,000-record sample was used to complete the model-development workflow within the available computational resources. The limitation is that the resulting metrics may not represent performance on the full dataset.

### Q4. Why use stratified train-validation splitting?

**Answer:** Stratified splitting attempts to preserve the target-class proportions in both partitions. This makes the validation comparison more representative of the sampled data's class distribution.

### Q5. What is the difference between precision and recall?

**Answer:** Precision measures the proportion of predicted delayed journeys that are actually delayed. Recall measures the proportion of actual delayed journeys that the model correctly identifies. High precision reduces false alarms, while high recall reduces missed delays.

### Q6. Why use LightGBM?

**Answer:** LightGBM is a gradient-boosted decision-tree algorithm designed for efficient learning on tabular data. It can capture nonlinear relationships and interactions among features. In this experiment, Tuned LightGBM achieved the highest validation accuracy, recall, and F1-score, although Logistic Regression achieved a higher ROC-AUC.

### Q7. What is ROC-AUC?

**Answer:** ROC-AUC summarizes a model's ability to rank positive cases above negative cases across different classification thresholds. A value of 0.5 indicates random ranking, while higher values indicate stronger discrimination.

### Q8. What is the purpose of hyperparameter tuning?

**Answer:** Hyperparameter tuning explores model configurations to find settings that improve a chosen evaluation objective. In this project, RandomizedSearchCV was used to evaluate selected Random Forest and LightGBM configurations using ROC-AUC and cross-validation.

### Q9. What does a false negative mean in this project?

**Answer:** A false negative occurs when the model predicts that a journey will be on time, but the actual target indicates that it is delayed. This can be important because the model fails to flag a journey that may require attention.

### Q10. Does a valid submission file prove that the model is accurate?

**Answer:** No. Submission validation checks the file structure, row count, required columns, missing values, duplicate identifiers, and probability range. Predictive accuracy on the unlabeled test dataset cannot be calculated without the corresponding ground-truth labels.

### Q11. Why does the project exclude `train_number` from one-hot encoding?

**Answer:** A train number can have many distinct values, creating a large number of dummy columns. Excluding it reduces memory consumption. However, the exclusion may remove potentially useful information, so alternative encodings could be explored in future work.

### Q12. Which model was selected and why?

**Answer:** Tuned LightGBM was selected for the final prediction workflow because it achieved the highest validation accuracy of 85.85%, recall of 92.10%, and F1-score of 0.9038 among the evaluated models. Logistic Regression achieved the highest ROC-AUC of 0.9229, so the model choice depends on the evaluation objective.

---

## 16. Conclusion

This project demonstrates an end-to-end machine learning workflow for predicting Indian Railways train delays using structured operational data. It covers data preparation, leakage prevention, feature engineering, categorical encoding, numerical standardization, model training, hyperparameter tuning, validation, error analysis, feature importance, and test-set prediction.

The current sampled experiment shows that Tuned LightGBM provides the highest validation accuracy, recall, and F1-score among the evaluated models, while Logistic Regression achieves the highest ROC-AUC. The generated submission contains 375,000 predictions and passes structural validation.

The primary limitations are the use of a 10,000-record model-development sample, the exclusion of a high-cardinality feature, and the reduced hyperparameter search. Further work should evaluate larger training samples, investigate alternative categorical representations, verify artifact reproducibility, and assess model calibration and generalization.

The project therefore serves as a practical demonstration of a complete machine learning pipeline while identifying clear directions for improving predictive reliability and computational efficiency.

---

*Report prepared for ECSCI24302 – Machine Learning Essentials, Project-Based Learning submission.*