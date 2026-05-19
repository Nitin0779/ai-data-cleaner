"""
DataCleaner AI — Outlier Detector
Z-Score, IQR, and Isolation Forest anomaly detection.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def detect_outliers_zscore(
    df: pd.DataFrame, threshold: float = 3.0
) -> Tuple[pd.DataFrame, Dict]:
    """Detect outliers using Z-score method."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.Series(dtype=bool), {}

    z_scores = np.abs((numeric_df - numeric_df.mean()) / (numeric_df.std() + 1e-9))
    outlier_mask = (z_scores > threshold).any(axis=1)

    col_counts = {}
    for col in numeric_df.columns:
        col_z = np.abs((numeric_df[col] - numeric_df[col].mean()) / (numeric_df[col].std() + 1e-9))
        col_counts[col] = int((col_z > threshold).sum())

    return outlier_mask, {
        "method": "Z-Score",
        "threshold": threshold,
        "total_outliers": int(outlier_mask.sum()),
        "outlier_pct": round(outlier_mask.sum() / max(len(df), 1) * 100, 2),
        "per_column": col_counts,
    }


def detect_outliers_iqr(
    df: pd.DataFrame, multiplier: float = 1.5
) -> Tuple[pd.DataFrame, Dict]:
    """Detect outliers using IQR method."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.Series(dtype=bool), {}

    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR

    outlier_mask = ((numeric_df < lower) | (numeric_df > upper)).any(axis=1)

    col_counts = {}
    for col in numeric_df.columns:
        mask = (numeric_df[col] < lower[col]) | (numeric_df[col] > upper[col])
        col_counts[col] = int(mask.sum())

    return outlier_mask, {
        "method": "IQR",
        "multiplier": multiplier,
        "total_outliers": int(outlier_mask.sum()),
        "outlier_pct": round(outlier_mask.sum() / max(len(df), 1) * 100, 2),
        "per_column": col_counts,
        "bounds": {col: {"lower": round(float(lower[col]), 3), "upper": round(float(upper[col]), 3)}
                   for col in numeric_df.columns},
    }


def detect_outliers_isolation_forest(
    df: pd.DataFrame, contamination: float = 0.05, random_state: int = 42
) -> Tuple[pd.DataFrame, Dict]:
    """Detect outliers using Isolation Forest."""
    try:
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        return pd.Series([False] * len(df)), {"error": "scikit-learn not installed"}

    numeric_df = df.select_dtypes(include=[np.number]).dropna()
    if numeric_df.empty or len(numeric_df) < 10:
        return pd.Series([False] * len(df)), {"error": "Not enough numeric data"}

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)

    iso = IsolationForest(contamination=contamination, random_state=random_state, n_estimators=100)
    preds = iso.fit_predict(X_scaled)
    scores = iso.score_samples(X_scaled)

    # Map back to original index
    outlier_mask = pd.Series(False, index=df.index)
    outlier_mask.loc[numeric_df.index] = preds == -1

    return outlier_mask, {
        "method": "Isolation Forest",
        "contamination": contamination,
        "total_outliers": int(outlier_mask.sum()),
        "outlier_pct": round(outlier_mask.sum() / max(len(df), 1) * 100, 2),
        "anomaly_scores": scores.tolist(),
        "columns_used": numeric_df.columns.tolist(),
    }


def remove_outliers(df: pd.DataFrame, outlier_mask: pd.Series) -> Tuple[pd.DataFrame, int]:
    """Remove outlier rows from dataset."""
    rows_before = len(df)
    df_clean = df[~outlier_mask].reset_index(drop=True)
    return df_clean, rows_before - len(df_clean)
