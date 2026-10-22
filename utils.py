import numpy as np
import pandas as pd

def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Construct domain-specific features for Indian Railways delay modeling.
    Works identically on training, validation, and untouched test sets.
    """
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
