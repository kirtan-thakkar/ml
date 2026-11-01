"""
Automated Test Suite for Indian Railways Train Delay Prediction & Network Punctuality Analytics
ECSCI24302 - Machine Learning Essentials Master Audit
Tests artifact loading, preprocessing, feature engineering, pipeline inference, and edge cases.
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd
import joblib

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import utils


class TestArtifactIntegrity(unittest.TestCase):
    """Test 1: Verifies artifact presence, structure, metadata and bounds."""

    @classmethod
    def setUpClass(cls):
        cls.artifact_path = os.path.join(ROOT_DIR, "artifacts", "pandas_numpy_pipeline.joblib")
        assert os.path.exists(cls.artifact_path), f"Artifact missing at {cls.artifact_path}"
        cls.pipeline = joblib.load(cls.artifact_path)

    def test_artifact_keys(self):
        expected_keys = {'model', 'train_mean', 'train_std', 'feature_columns', 'cat_cols', 'num_cols', 'iqr_bounds'}
        self.assertTrue(expected_keys.issubset(set(self.pipeline.keys())),
                        f"Missing required keys. Found: {self.pipeline.keys()}")

    def test_model_capabilities(self):
        model = self.pipeline['model']
        self.assertTrue(hasattr(model, 'predict_proba'), "Model must have predict_proba method")
        self.assertTrue(hasattr(model, 'predict'), "Model must have predict method")

    def test_iqr_bounds_specification(self):
        iqr_bounds = self.pipeline.get('iqr_bounds', {})
        self.assertIsInstance(iqr_bounds, dict, "iqr_bounds must be a dictionary in artifact")
        
        # Verify that utils.handle_outliers_iqr_numpy properly clips extreme values
        df_outliers = pd.DataFrame({'distance_km': [100.0, 200.0, 300.0, 400.0, 5000.0]})
        clipped = utils.handle_outliers_iqr_numpy(df_outliers, ['distance_km'])
        self.assertLess(clipped['distance_km'].max(), 5000.0, "Extreme outlier must be clipped")

    def test_feature_columns_dimension(self):
        cols = self.pipeline['feature_columns']
        self.assertEqual(len(cols), 8111, "Trained pipeline must have exactly 8,111 sparse features")


class TestDataCleaningAndQuarantine(unittest.TestCase):
    """Test 2: Verifies target leakage quarantine and constant column dropping."""

    def setUp(self):
        self.raw_sample = pd.DataFrame([{
            'train_number': 12951,
            'is_overloaded': 0,
            'journey_id': 'JRN-998822',
            'departure_date': '2024-03-15',
            'delay_minutes': 45.0,
            'primary_delay_cause': 'Signal Failure',
            'distance_km': 1385.0,
            'scheduled_travel_hours': 16.0,
            'num_scheduled_stops': 8
        }])

    def test_leakage_and_id_quarantine(self):
        cleaned = utils.clean_data_pandas(self.raw_sample, is_train=True)
        self.assertNotIn('is_overloaded', cleaned.columns, "Constant zero-variance column must be dropped")
        self.assertNotIn('delay_minutes', cleaned.columns, "delay_minutes is target leakage and must be dropped")
        self.assertNotIn('primary_delay_cause', cleaned.columns, "primary_delay_cause is target leakage and must be dropped")
        self.assertNotIn('departure_date', cleaned.columns, "Raw date string must be dropped")


class TestFeatureEngineering(unittest.TestCase):
    """Test 3: Verifies mathematical feature derivations (kinematics, vulnerability, cyclical time)."""

    def setUp(self):
        self.df = pd.DataFrame([{
            'distance_km': 1200.0,
            'scheduled_travel_hours': 15.0,
            'num_scheduled_stops': 10,
            'season_severity_score': 0.8,
            'is_monsoon_season': 1,
            'is_fog_risk': 0,
            'zone_congestion_index': 0.85,
            'is_hdn_route': 1,
            'track_doubled': 1,
            'loco_age_years': 10.0,
            'coach_age_years': 8.0,
            'late_incoming_rake': 1,
            'is_rake_shared': 1,
            'route_historical_ontime_pct': 75.0,
            'departure_hour': 6,
            'day_of_week': 3
        }])

    def test_engineered_derivations(self):
        eng = utils.engineer_features_pandas(self.df)
        
        # 1. Kinematics
        expected_speed = 1200.0 / 15.0  # 80 km/h
        self.assertAlmostEqual(eng['avg_speed_kmh'].iloc[0], expected_speed, delta=0.01)
        
        # 2. Network vulnerability
        expected_vuln = 0.85 * (1.0 + 0.5 * 1 - 0.3 * 1) # 0.85 * 1.2 = 1.02
        self.assertAlmostEqual(eng['network_vulnerability'].iloc[0], expected_vuln, delta=0.01)
        
        # 3. Equipment age index
        self.assertAlmostEqual(eng['equipment_age_index'].iloc[0], 9.0, delta=0.01)
        
        # 4. Cyclical time
        expected_sin = np.sin(2.0 * np.pi * 6 / 24.0) # sin(pi/2) = 1.0
        self.assertAlmostEqual(eng['hour_sin'].iloc[0], expected_sin, delta=0.01)


class TestInferencePipeline(unittest.TestCase):
    """Test 4: Verifies full model pipeline inference on realistic inputs."""

    @classmethod
    def setUpClass(cls):
        cls.artifact_path = os.path.join(ROOT_DIR, "artifacts", "pandas_numpy_pipeline.joblib")
        cls.pipeline = joblib.load(cls.artifact_path)
        cls.model = cls.pipeline['model']
        cls.train_mean = cls.pipeline['train_mean']
        cls.train_std = cls.pipeline['train_std']
        cls.feature_columns = cls.pipeline['feature_columns']
        cls.cat_cols = cls.pipeline['cat_cols']
        cls.num_cols = cls.pipeline['num_cols']
        cls.iqr_bounds = cls.pipeline.get('iqr_bounds', {})

    def _run_pipeline(self, raw_dict):
        df_in = pd.DataFrame([raw_dict])
        df_clean = utils.clean_data_pandas(df_in, is_train=False)
        if "train_number" in df_clean.columns:
            df_clean = df_clean.drop(columns=["train_number"], errors="ignore")
        if self.iqr_bounds:
            df_clean = utils.handle_outliers_iqr_numpy(df_clean, list(self.iqr_bounds.keys()))
        df_eng = utils.engineer_features_pandas(df_clean)
        usable_cat = [c for c in self.cat_cols if c in df_eng.columns]
        df_encoded = pd.get_dummies(df_eng, columns=usable_cat, dtype=np.uint8)
        df_proc = df_encoded.reindex(columns=self.feature_columns, fill_value=0)
        valid_num = [c for c in self.num_cols if c in df_proc.columns]
        df_proc[valid_num] = (
            df_proc[valid_num].astype(np.float32) - self.train_mean[valid_num]
        ) / self.train_std[valid_num]
        
        prob = float(self.model.predict_proba(df_proc)[0, 1])
        pred = int(prob >= 0.50)
        return prob, pred

    def test_vande_bharat_preset(self):
        vb_data = {
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
            "late_incoming_rake": 0, "is_special_train": 0, "route_historical_ontime_pct": 88.5
        }
        prob, pred = self._run_pipeline(vb_data)
        self.assertLess(prob, 0.25, "Vande Bharat priority service should have low delay probability")
        self.assertEqual(pred, 0, "Prediction should be 0 (On-time)")

    def test_monsoon_mail_preset(self):
        monsoon_data = {
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
            "late_incoming_rake": 1, "is_special_train": 1, "route_historical_ontime_pct": 42.0
        }
        prob, pred = self._run_pipeline(monsoon_data)
        self.assertGreater(prob, 0.75, "Monsoon delayed train should have high delay probability")
        self.assertEqual(pred, 1, "Prediction should be 1 (Delayed)")

    def test_unseen_and_outlier_inputs(self):
        outlier_data = {
            "train_number": 99999, "train_type": "Special Experimental Train",
            "year": 2025, "month": 12, "day_of_week": 7, "departure_hour": 23,
            "is_weekend": 1, "is_night_departure": 1, "is_peak_hour": 0, "is_festival_season": 0,
            "season": "Winter/Fog", "zone": "Alien Railway (AR)", "zone_abbr": "AR",
            "source_station_category": "Z", "destination_station_category": "Z",
            "distance_km": 4500,  # Extreme outlier distance (>1466 km capped)
            "num_scheduled_stops": 50, "scheduled_travel_hours": 80.0,
            "track_doubled": 0, "is_hdn_route": 0, "traction_type": "Steam",
            "is_electrified": 0, "psr_count": 15, "is_circular_route": 1, "is_monsoon_season": 0,
            "is_fog_risk": 1, "fog_risk_score": 0.95, "zone_fog_index": 0.95, "zone_congestion_index": 0.95,
            "season_severity_score": 0.95, "loco_age_years": 45.0, "coach_age_years": 40.0,
            "has_lhb_coaches": 0, "is_rake_shared": 1, "maintenance_score": 1.0, "seat_utilisation_pct": 120.0,
            "late_incoming_rake": 1, "is_special_train": 1, "route_historical_ontime_pct": 10.0
        }
        prob, pred = self._run_pipeline(outlier_data)
        self.assertTrue(0.0 <= prob <= 1.0, "Probability must remain within [0, 1]")
        self.assertIn(pred, [0, 1], "Prediction must be binary 0 or 1")


class TestMetricsAndEvaluation(unittest.TestCase):
    """Test 5: Verifies evaluation metric formulas and confusion matrix math."""

    def test_confusion_matrix_metrics(self):
        # Actual validation results: TP = 1329, TN = 388, FP = 169, FN = 114 (total = 2000)
        tp = 1329
        tn = 388
        fp = 169
        fn = 114
        total = tp + tn + fp + fn
        self.assertEqual(total, 2000)

        accuracy = (tp + tn) / total
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

        self.assertAlmostEqual(accuracy, 0.8585, places=4)
        self.assertAlmostEqual(precision, 0.8872, places=4)
        self.assertAlmostEqual(recall, 0.9210, places=4)
        self.assertAlmostEqual(f1, 0.9038, places=4)


class TestRiskClassification(unittest.TestCase):
    """Test 6: Verifies operational delay risk thresholds."""

    def _classify_risk(self, prob):
        pct = prob * 100.0
        if pct > 65.0:
            return "HIGH DELAY RISK"
        elif pct >= 40.0:
            return "MODERATE DELAY RISK"
        else:
            return "ON-TIME EXPECTED"

    def test_risk_threshold_brackets(self):
        self.assertEqual(self._classify_risk(0.15), "ON-TIME EXPECTED")
        self.assertEqual(self._classify_risk(0.39), "ON-TIME EXPECTED")
        self.assertEqual(self._classify_risk(0.40), "MODERATE DELAY RISK")
        self.assertEqual(self._classify_risk(0.55), "MODERATE DELAY RISK")
        self.assertEqual(self._classify_risk(0.65), "MODERATE DELAY RISK")
        self.assertEqual(self._classify_risk(0.66), "HIGH DELAY RISK")
        self.assertEqual(self._classify_risk(0.98), "HIGH DELAY RISK")


if __name__ == '__main__':
    unittest.main()
