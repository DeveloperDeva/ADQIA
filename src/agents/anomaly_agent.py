"""
Anomaly Agent - Detects outliers and anomalies in numeric data.
"""

import pandas as pd
from typing import Dict
from src.tools import stats_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AnomalyAgent:
    """
    Agent responsible for anomaly and outlier detection.
    Uses z-score based statistical methods for numeric columns.
    """
    
    def __init__(self, z_threshold: float = 3.0):
        """
        Initialize the AnomalyAgent.
        
        Args:
            z_threshold: Z-score threshold for outlier detection (default: 3.0)
        """
        self.z_threshold = z_threshold
        logger.info(f"AnomalyAgent initialized with z_threshold={z_threshold}")
    
    def run(self, df: pd.DataFrame, z_thresh: float = None) -> Dict[str, any]:
        """
        Perform anomaly detection on numeric columns.
        
        Args:
            df: Input DataFrame to analyze
            z_thresh: Optional z-score threshold (overrides instance default)
        
        Returns:
            Dictionary with anomaly results:
            - outliers: Dict mapping numeric columns to outlier counts
            - summary_stats: Dict with mean, std, min, max for numeric columns
        """
        threshold = z_thresh if z_thresh is not None else self.z_threshold
        logger.info(f"Starting anomaly detection with z-threshold={threshold}")
        
        # Detect outliers using z-score
        outliers = stats_tool.detect_outliers_zscore(df, z_threshold=threshold)
        
        # Get summary statistics for numeric columns
        summary_stats = stats_tool.get_summary_stats(df)
        
        results = {
            'outliers': outliers,
            'summary_stats': summary_stats,
            'z_threshold': threshold
        }
        
        # Log summary
        total_outliers = sum(outliers.values())
        logger.info(f"Anomaly detection complete: {total_outliers} total outliers across {len(outliers)} columns")
        
        return results
    
    def detect_high_cardinality(self, df: pd.DataFrame, threshold: float = 0.9) -> Dict[str, int]:
        """
        Detect columns with unusually high cardinality.
        
        Args:
            df: Input DataFrame
            threshold: Uniqueness ratio threshold (default: 0.9)
        
        Returns:
            Dictionary mapping high-cardinality columns to unique counts
        """
        high_card = stats_tool.detect_cardinality_issues(df, threshold)
        
        if high_card:
            logger.warning(f"High cardinality detected in {len(high_card)} columns")
        
        return high_card
