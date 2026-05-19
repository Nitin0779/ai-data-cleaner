"""
DataCleaner AI — Missing Value Handler
Smart strategies for handling missing data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "auto",
    custom_strategies: Dict[str, str] = None,
) -> Tuple[pd.DataFrame, Dict]:
    """
    Handle missing values using the specified strategy.
    
    Strategies:
        auto      — median for numeric, mode for categorical
        mean      — fill numeric with column mean
        median    — fill numeric with column median
        mode      — fill all with most frequent value
        ffill     — forward fill
        bfill     — backward fill
        drop_rows — drop rows with any nulls
        drop_cols — drop columns with >50% nulls
        zero      — fill numeric with 0, categorical with 'Unknown'
    """
    df_clean = df.copy()
    report = {"strategy": strategy, "changes": [], "rows_before": len(df), "nulls_before": int(df.isnull().sum().sum())}

    if custom_strategies:
        # Apply per-column custom strategies
        for col, strat in custom_strategies.items():
            if col not in df_clean.columns:
                continue
            null_count = int(df_clean[col].isnull().sum())
            if null_count == 0:
                continue
            df_clean[col] = _apply_col_strategy(df_clean[col], strat)
            report["changes"].append({"column": col, "strategy": strat, "nulls_fixed": null_count})
    else:
        if strategy == "drop_rows":
            rows_before = len(df_clean)
            df_clean = df_clean.dropna()
            report["changes"].append({
                "column": "ALL",
                "strategy": "drop_rows",
                "nulls_fixed": rows_before - len(df_clean),
            })

        elif strategy == "drop_cols":
            cols_before = df_clean.columns.tolist()
            threshold = 0.5
            df_clean = df_clean.loc[:, df_clean.isnull().mean() < threshold]
            dropped = [c for c in cols_before if c not in df_clean.columns]
            report["changes"].append({
                "column": str(dropped),
                "strategy": "drop_cols",
                "nulls_fixed": len(dropped),
            })

        else:
            for col in df_clean.columns:
                null_count = int(df_clean[col].isnull().sum())
                if null_count == 0:
                    continue

                if strategy == "auto":
                    if pd.api.types.is_numeric_dtype(df_clean[col]):
                        col_strategy = "median"
                    else:
                        col_strategy = "mode"
                else:
                    col_strategy = strategy

                df_clean[col] = _apply_col_strategy(df_clean[col], col_strategy)
                report["changes"].append({"column": col, "strategy": col_strategy, "nulls_fixed": null_count})

    report["rows_after"] = len(df_clean)
    report["nulls_after"] = int(df_clean.isnull().sum().sum())
    return df_clean, report


def _apply_col_strategy(series: pd.Series, strategy: str) -> pd.Series:
    """Apply a single strategy to a Series."""
    s = series.copy()
    if strategy == "mean" and pd.api.types.is_numeric_dtype(s):
        return s.fillna(s.mean())
    elif strategy == "median" and pd.api.types.is_numeric_dtype(s):
        return s.fillna(s.median())
    elif strategy == "mode":
        mode_val = s.mode()
        return s.fillna(mode_val[0] if len(mode_val) > 0 else s)
    elif strategy == "ffill":
        return s.ffill()
    elif strategy == "bfill":
        return s.bfill()
    elif strategy == "zero":
        if pd.api.types.is_numeric_dtype(s):
            return s.fillna(0)
        else:
            return s.fillna("Unknown")
    elif strategy == "drop":
        return s  # handled at df level
    else:
        # Default auto fallback
        if pd.api.types.is_numeric_dtype(s):
            return s.fillna(s.median())
        else:
            mode_val = s.mode()
            return s.fillna(mode_val[0] if len(mode_val) > 0 else s)
