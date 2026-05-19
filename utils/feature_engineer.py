"""
DataCleaner AI — Feature Engineering Utility
Label encoding, one-hot encoding, scaling, and PCA.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


def label_encode(df: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, Dict]:
    """Apply label encoding to specified columns."""
    from sklearn.preprocessing import LabelEncoder
    df_enc = df.copy()
    mappings = {}
    for col in columns:
        if col in df_enc.columns:
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col].astype(str))
            mappings[col] = {str(cls): int(idx) for idx, cls in enumerate(le.classes_)}
    return df_enc, mappings


def one_hot_encode(df: pd.DataFrame, columns: List[str], drop_first: bool = False) -> pd.DataFrame:
    """Apply one-hot encoding to specified columns."""
    return pd.get_dummies(df, columns=columns, drop_first=drop_first, dtype=int)


def scale_features(
    df: pd.DataFrame,
    columns: List[str],
    method: str = "standard"
) -> Tuple[pd.DataFrame, Any]:
    """
    Scale numeric features.
    Methods: standard, minmax, robust
    """
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
    df_scaled = df.copy()
    scalers = {"standard": StandardScaler(), "minmax": MinMaxScaler(), "robust": RobustScaler()}
    scaler = scalers.get(method, StandardScaler())
    valid_cols = [c for c in columns if c in df_scaled.columns and pd.api.types.is_numeric_dtype(df_scaled[c])]
    if valid_cols:
        df_scaled[valid_cols] = scaler.fit_transform(df_scaled[valid_cols])
    return df_scaled, scaler


def apply_pca(
    df: pd.DataFrame,
    n_components: int = 2,
    columns: List[str] = None
) -> Tuple[pd.DataFrame, Any, np.ndarray]:
    """
    Apply PCA dimensionality reduction.
    Returns transformed DataFrame, fitted PCA object, and explained variance ratios.
    """
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    valid_cols = [c for c in columns if c in df.columns]
    if len(valid_cols) < 2:
        raise ValueError("Need at least 2 numeric columns for PCA")

    X = df[valid_cols].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    n_components = min(n_components, len(valid_cols), len(X))
    pca = PCA(n_components=n_components, random_state=42)
    components = pca.fit_transform(X_scaled)

    # Build result DataFrame
    col_names = [f"PC{i+1}" for i in range(n_components)]
    pca_df = pd.DataFrame(components, columns=col_names, index=X.index)

    return pca_df, pca, pca.explained_variance_ratio_


def fix_datatypes(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Auto-fix columns with wrong datatypes (e.g., numeric stored as strings)."""
    df_fixed = df.copy()
    fixed_cols = []
    for col in df_fixed.select_dtypes(include="object").columns:
        try:
            converted = pd.to_numeric(df_fixed[col])
            df_fixed[col] = converted
            fixed_cols.append(col)
        except (ValueError, TypeError):
            pass
    return df_fixed, fixed_cols


def remove_constant_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Remove columns with only one unique value."""
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    return df.drop(columns=constant_cols), constant_cols


def remove_duplicate_rows(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """Remove duplicate rows."""
    before = len(df)
    df_clean = df.drop_duplicates().reset_index(drop=True)
    return df_clean, before - len(df_clean)
