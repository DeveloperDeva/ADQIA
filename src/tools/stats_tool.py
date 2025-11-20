"""
Statistical analysis tools for data quality and anomaly detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)


def detect_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """
    Detect missing values in each column.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary mapping column names to missing value counts
    """
    missing = df.isnull().sum()
    missing_dict = {col: int(count) for col, count in missing.items() if count > 0}
    
    if missing_dict:
        logger.info(f"Missing values detected in {len(missing_dict)} columns")
    else:
        logger.info("No missing values detected")
    
    return missing_dict


def calculate_null_fraction(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate the fraction of null values per column.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary mapping column names to null fractions (0.0 to 1.0)
    """
    null_fraction = df.isnull().sum() / len(df)
    return {col: float(frac) for col, frac in null_fraction.items() if frac > 0}


def detect_duplicates(df: pd.DataFrame) -> int:
    """
    Count duplicate rows in DataFrame.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Number of duplicate rows
    """
    duplicates = df.duplicated().sum()
    logger.info(f"Found {duplicates} duplicate rows")
    return int(duplicates)


def detect_outliers_zscore(df: pd.DataFrame, z_threshold: float = 3.0) -> Dict[str, int]:
    """
    Detect outliers using z-score method for numeric columns.
    
    Args:
        df: Input DataFrame
        z_threshold: Z-score threshold for outlier detection (default: 3.0)
    
    Returns:
        Dictionary mapping numeric column names to outlier counts
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    
    for col in numeric_cols:
        # Skip columns with all NaN or single value
        if df[col].notna().sum() < 2:
            continue
        
        mean = df[col].mean()
        std = df[col].std()
        
        # Skip if std is 0 (all values are the same)
        if std == 0:
            continue
        
        z_scores = np.abs((df[col] - mean) / std)
        outlier_count = (z_scores > z_threshold).sum()
        
        if outlier_count > 0:
            outliers[col] = int(outlier_count)
    
    if outliers:
        logger.info(f"Outliers detected in {len(outliers)} columns")
    else:
        logger.info("No outliers detected")
    
    return outliers


def get_summary_stats(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate summary statistics for numeric columns.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary mapping column names to their summary statistics
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary = {}
    
    for col in numeric_cols:
        if df[col].notna().sum() > 0:
            summary[col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'median': float(df[col].median()),
                'count': int(df[col].notna().sum())
            }
    
    logger.info(f"Generated summary statistics for {len(summary)} numeric columns")
    return summary


def get_value_counts(df: pd.DataFrame, column: str, top_n: int = 10) -> Dict[str, int]:
    """
    Get value counts for a categorical column.
    
    Args:
        df: Input DataFrame
        column: Column name
        top_n: Number of top values to return
    
    Returns:
        Dictionary mapping values to their counts
    """
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found in DataFrame")
        return {}
    
    value_counts = df[column].value_counts().head(top_n)
    return {str(k): int(v) for k, v in value_counts.items()}


def detect_cardinality_issues(df: pd.DataFrame, high_cardinality_threshold: float = 0.9) -> Dict[str, int]:
    """
    Detect columns with high cardinality (mostly unique values).
    
    Args:
        df: Input DataFrame
        high_cardinality_threshold: Fraction of unique values to flag (default: 0.9)
    
    Returns:
        Dictionary mapping high-cardinality columns to unique value counts
    """
    high_cardinality = {}
    
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        
        if total_count > 0:
            uniqueness = unique_count / total_count
            if uniqueness > high_cardinality_threshold:
                high_cardinality[col] = unique_count
    
    if high_cardinality:
        logger.info(f"High cardinality detected in {len(high_cardinality)} columns")
    
    return high_cardinality
