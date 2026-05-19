"""
DataCleaner AI — Data Profiler Utility
Generates comprehensive dataset quality metrics and scoring.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple


def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a full profile of the dataset."""
    profile = {
        "shape": df.shape,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "total_cells": df.shape[0] * df.shape[1],
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_pct": round(df.duplicated().sum() / len(df) * 100, 2) if len(df) > 0 else 0,
        "null_counts": df.isnull().sum().to_dict(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "total_nulls": int(df.isnull().sum().sum()),
        "null_rate": round(df.isnull().sum().sum() / df.size * 100, 2),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "column_types": classify_columns(df),
        "constant_columns": get_constant_columns(df),
        "high_cardinality_cols": get_high_cardinality_cols(df),
        "numeric_stats": get_numeric_stats(df),
        "quality_score": compute_quality_score(df),
        "issues": detect_issues(df),
    }
    return profile


def classify_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Classify each column as numeric, categorical, datetime, or boolean."""
    types = {}
    for col in df.columns:
        if pd.api.types.is_bool_dtype(df[col]):
            types[col] = "boolean"
        elif pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = "datetime"
        else:
            # Try to infer if it could be numeric
            try:
                pd.to_numeric(df[col].dropna())
                types[col] = "numeric_string"
            except (ValueError, TypeError):
                types[col] = "categorical"
    return types


def get_constant_columns(df: pd.DataFrame) -> List[str]:
    """Return columns with only one unique value."""
    return [col for col in df.columns if df[col].nunique() <= 1]


def get_high_cardinality_cols(df: pd.DataFrame, threshold: float = 0.9) -> List[str]:
    """Return categorical columns with very high cardinality (likely IDs)."""
    results = []
    for col in df.select_dtypes(include="object").columns:
        if df[col].nunique() / max(len(df), 1) > threshold:
            results.append(col)
    return results


def get_numeric_stats(df: pd.DataFrame) -> Dict[str, Dict]:
    """Get descriptive stats for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return {}
    stats = numeric_df.describe().to_dict()
    # Add skewness and kurtosis
    for col in numeric_df.columns:
        if col in stats:
            stats[col]["skewness"] = round(float(numeric_df[col].skew()), 3)
            stats[col]["kurtosis"] = round(float(numeric_df[col].kurtosis()), 3)
    return stats


def compute_quality_score(df: pd.DataFrame) -> int:
    """
    Compute dataset quality score from 0–100.
    Deductions for: nulls, duplicates, constant columns, type issues.
    """
    score = 100

    # Penalize nulls (up to -30)
    null_rate = df.isnull().sum().sum() / max(df.size, 1)
    score -= min(30, int(null_rate * 100))

    # Penalize duplicates (up to -15)
    dup_rate = df.duplicated().sum() / max(len(df), 1)
    score -= min(15, int(dup_rate * 50))

    # Penalize constant columns (up to -10)
    constant_count = len(get_constant_columns(df))
    score -= min(10, constant_count * 3)

    # Penalize very small datasets (up to -10)
    if len(df) < 50:
        score -= 10
    elif len(df) < 200:
        score -= 5

    # Bonus for good shape
    if df.shape[1] >= 5 and len(df) >= 500:
        score = min(100, score + 5)

    return max(0, min(100, score))


def detect_issues(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Detect all data quality issues and return structured issue list."""
    issues = []

    # Null value issues
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        null_pct = round(null_count / max(len(df), 1) * 100, 1)
        if null_count > 0:
            severity = "high" if null_pct > 30 else ("medium" if null_pct > 10 else "low")
            issues.append({
                "type": "missing_values",
                "column": col,
                "description": f"{null_count} missing values ({null_pct}%)",
                "severity": severity,
                "count": null_count,
            })

    # Duplicate rows
    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        issues.append({
            "type": "duplicates",
            "column": "ALL",
            "description": f"{dup_count} duplicate rows detected",
            "severity": "medium" if dup_count / max(len(df), 1) < 0.1 else "high",
            "count": dup_count,
        })

    # Constant columns
    for col in get_constant_columns(df):
        issues.append({
            "type": "constant_column",
            "column": col,
            "description": f"Column '{col}' has only 1 unique value — no predictive power",
            "severity": "medium",
            "count": 1,
        })

    # High cardinality columns
    for col in get_high_cardinality_cols(df):
        issues.append({
            "type": "high_cardinality",
            "column": col,
            "description": f"Column '{col}' may be an ID column (high cardinality)",
            "severity": "low",
            "count": int(df[col].nunique()),
        })

    # Numeric strings
    col_types = classify_columns(df)
    for col, t in col_types.items():
        if t == "numeric_string":
            issues.append({
                "type": "wrong_dtype",
                "column": col,
                "description": f"Column '{col}' contains numbers stored as strings",
                "severity": "medium",
                "count": 1,
            })

    return issues


def get_ml_problem_type(df: pd.DataFrame, target_col: str = None) -> str:
    """Guess the ML problem type based on dataset characteristics."""
    if target_col and target_col in df.columns:
        target = df[target_col]
        n_unique = target.nunique()
        if pd.api.types.is_numeric_dtype(target):
            if n_unique <= 10:
                return "Classification"
            return "Regression"
        else:
            if n_unique == 2:
                return "Binary Classification"
            return "Multi-class Classification"
    # No target — guess clustering
    return "Clustering / Unsupervised"


def get_feature_importance_proxy(df: pd.DataFrame) -> List[Tuple[str, float]]:
    """
    Compute a simple proxy for feature importance using variance (for numeric cols)
    and entropy (for categorical cols), normalized to 0-1.
    """
    scores = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include="object").columns

    for col in numeric_cols:
        std = df[col].std()
        mean = abs(df[col].mean()) + 1e-9
        scores[col] = min(1.0, (std / mean))  # coefficient of variation

    for col in cat_cols:
        n_unique = df[col].nunique()
        entropy_proxy = min(1.0, n_unique / max(len(df), 1) * 10)
        scores[col] = entropy_proxy

    # Normalize
    max_score = max(scores.values()) + 1e-9
    normalized = {k: round(v / max_score, 3) for k, v in scores.items()}
    return sorted(normalized.items(), key=lambda x: x[1], reverse=True)
