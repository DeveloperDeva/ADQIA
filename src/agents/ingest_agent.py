"""
Ingest Agent - Handles CSV and Excel file loading and schema inference.
"""

import pandas as pd
from typing import Tuple, Dict
from src.tools import schema_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)


class IngestAgent:
    """
    Agent responsible for data ingestion and schema extraction.
    Loads CSV and Excel files and returns DataFrame with inferred schema.
    """
    
    def __init__(self):
        """Initialize the IngestAgent."""
        logger.info("IngestAgent initialized")
    
    def run(self, filepath: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
        """
        Load a CSV or Excel file and infer its schema.
        
        Args:
            filepath: Path to the CSV or Excel file
        
        Returns:
            Tuple of (DataFrame, schema_dict)
            - DataFrame: Loaded data
            - schema_dict: Dictionary mapping column names to dtype strings
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        logger.info(f"Starting ingestion of file: {filepath}")
        
        try:
            # Detect file type and load accordingly
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath)
                logger.info(f"Successfully loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            elif filepath.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
                logger.info(f"Successfully loaded Excel file with {len(df)} rows and {len(df.columns)} columns")
            else:
                raise ValueError(f"Unsupported file format. Please use CSV (.csv) or Excel (.xlsx, .xls) files.")
            
            # Infer schema
            schema = schema_tool.infer_schema(df)
            logger.info(f"Schema inferred: {list(schema.keys())}")
            
            return df, schema
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {filepath}")
            raise
        except ValueError as e:
            logger.error(f"Invalid file format: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during ingestion: {e}")
            raise
    
    def validate_file(self, filepath: str) -> bool:
        """
        Validate that file exists and is readable.
        
        Args:
            filepath: Path to validate
        
        Returns:
            True if file is valid, False otherwise
        """
        import os
        
        if not os.path.exists(filepath):
            logger.warning(f"File does not exist: {filepath}")
            return False
        
        if not filepath.lower().endswith('.csv'):
            logger.warning(f"File is not a CSV: {filepath}")
            return False
        
        logger.info(f"File validation passed: {filepath}")
        return True
