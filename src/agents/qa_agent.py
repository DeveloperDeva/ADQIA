"""
QA Agent - Performs data quality checks.
"""

import pandas as pd
from typing import Dict
from src.tools import stats_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)


class QAAgent:
    """
    Agent responsible for data quality assessment.
    Detects missing values, duplicates, and calculates null fractions.
    """
    
    def __init__(self):
        """Initialize the QAAgent."""
        logger.info("QAAgent initialized")
    
    def run(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Perform comprehensive data quality checks.
        
        Args:
            df: Input DataFrame to analyze
        
        Returns:
            Dictionary with QA results:
            - missing_values: Dict mapping columns to missing value counts
            - duplicate_rows: Integer count of duplicate rows
            - null_fraction: Dict mapping columns to null fraction (0.0-1.0)
        """
        logger.info("Starting data quality assessment")
        
        # Detect missing values
        missing_values = stats_tool.detect_missing_values(df)
        
        # Calculate null fractions
        null_fraction = stats_tool.calculate_null_fraction(df)
        
        # Detect duplicate rows
        duplicate_rows = stats_tool.detect_duplicates(df)
        
        results = {
            'missing_values': missing_values,
            'duplicate_rows': duplicate_rows,
            'null_fraction': null_fraction
        }
        
        # Log summary
        logger.info(f"QA complete: {len(missing_values)} columns with missing values, "
                   f"{duplicate_rows} duplicate rows")
        
        return results
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Get general data summary statistics.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Dictionary with summary information
        """
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'categorical_columns': len(df.select_dtypes(include=['object']).columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        logger.info(f"Data summary: {summary['total_rows']} rows, {summary['total_columns']} columns")
        
        return summary
