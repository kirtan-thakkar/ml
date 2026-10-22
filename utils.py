import numpy as np
import pandas as pd

def clean_data_pandas(df: pd.DataFrame, is_train: bool = True) -> pd.DataFrame:
    """
    Data cleaning using pure Pandas:
    - Removes zero-variance constant features ('is_overloaded')
    - Removes random unique identifiers ('journey_id')
    - Removes unneeded raw string dates ('departure_date')
    - Quarantines target leakage columns on train ('delay_minutes', 'primary_delay_cause')
    """
    data = df.copy()
    drop_cols = ['is_overloaded', 'departure_date']
    if is_train:
        drop_cols.extend(['delay_minutes', 'primary_delay_cause'])
    
    existing_drops = [c for c in drop_cols if c in data.columns]
    data = data.drop(columns=existing_drops)
    return data

def engineer_features_pandas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct domain-specific features using 100% pure Pandas and NumPy vectorized operations.
    Works consistently on train, validation, and untouched test sets.
    """
    data = df.copy()
    
    # 1. Kinematic & Stop Metrics (Vectorized Pandas division)
    data['avg_speed_kmh'] = data['distance_km'] / data['scheduled_travel_hours'].replace(0, np.nan)
    data['stops_density'] = data['num_scheduled_stops'] / (data['distance_km'] / 100.0 + 0.1)
    data['avg_stop_distance'] = data['distance_km'] / (data['num_scheduled_stops'] + 1)
    
    # 2. Weather & Network Vulnerability Interactions (Pandas arithmetic)
    data['composite_weather_severity'] = data['season_severity_score'] * (
        1.0 + 0.5 * data['is_monsoon_season'] + 0.5 * data['is_fog_risk']
    )
    data['network_vulnerability'] = data['zone_congestion_index'] * (
        1.0 + 0.5 * data['is_hdn_route'] - 0.3 * data['track_doubled']
    )
    
    # 3. Rolling Stock & Turnaround Risk
    data['equipment_age_index'] = (data['loco_age_years'] + data['coach_age_years']) / 2.0
    data['rake_turnaround_risk'] = data['late_incoming_rake'] * data['is_rake_shared']
    data['historical_delay_risk'] = (100.0 - data['route_historical_ontime_pct']) / 100.0
    
    # 4. Cyclical Trigonometric Time Encodings using NumPy (sin/cos of 2*pi*t/T)
    data['hour_sin'] = np.sin(2.0 * np.pi * data['departure_hour'] / 24.0)
    data['hour_cos'] = np.cos(2.0 * np.pi * data['departure_hour'] / 24.0)
    data['day_sin'] = np.sin(2.0 * np.pi * data['day_of_week'] / 7.0)
    data['day_cos'] = np.cos(2.0 * np.pi * data['day_of_week'] / 7.0)
    
    return data

# Backward compatibility alias
engineer_features = engineer_features_pandas

def handle_outliers_iqr_numpy(df: pd.DataFrame, numerical_cols: list, factor: float = 1.5) -> pd.DataFrame:
    """
    Robust outlier treatment using pure NumPy & Pandas IQR (Interquartile Range) clipping.
    Caps extreme anomalies without dropping valuable data rows.
    """
    data = df.copy()
    for col in numerical_cols:
        if col in data.columns and np.issubdtype(data[col].dtype, np.number):
            q25 = data[col].quantile(0.25)
            q75 = data[col].quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - factor * iqr
            upper_bound = q75 + factor * iqr
            data[col] = np.clip(data[col], lower_bound, upper_bound)
    return data

def encode_categoricals_pandas(train_df: pd.DataFrame, val_or_test_df: pd.DataFrame, cat_cols: list):
    """
    Categorical One-Hot Encoding using pure Pandas pd.get_dummies().
    Aligns columns strictly to ensure zero leakage and identical feature alignment.
    """
    train_encoded = pd.get_dummies(train_df, columns=cat_cols, drop_first=False, dtype=np.int8)
    val_encoded = pd.get_dummies(val_or_test_df, columns=cat_cols, drop_first=False, dtype=np.int8)
    
    # Align val/test columns to match train exactly (filling unseen categories with 0)
    val_encoded = val_encoded.reindex(columns=train_encoded.columns, fill_value=0)
    return train_encoded, val_encoded

def scale_features_numpy(X_train: pd.DataFrame, X_val: pd.DataFrame, num_cols: list):
    """
    Manual Z-score Standardization using pure NumPy & Pandas:
    Z = (X - mean) / std
    mean and std are learned strictly on the training set to prevent data leakage.
    """
    train_scaled = X_train.copy()
    val_scaled = X_val.copy()
    
    # Compute mean and standard deviation strictly on training set using Pandas/NumPy
    train_mean = train_scaled[num_cols].mean()
    train_std = train_scaled[num_cols].std().replace(0, 1.0)
    
    # Vectorized NumPy / Pandas Z-score transformation
    train_scaled[num_cols] = (train_scaled[num_cols] - train_mean) / train_std
    val_scaled[num_cols] = (val_scaled[num_cols] - train_mean) / train_std
    
    scaling_params = {'mean': train_mean, 'std': train_std}
    return train_scaled, val_scaled, scaling_params
