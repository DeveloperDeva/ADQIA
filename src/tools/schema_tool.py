"""
Schema inference and comparison tool.
Handles dataset schema extraction and change detection.
"""

import pandas as pd
from typing import Dict, List, Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)


def infer_schema(df: pd.DataFrame) -> Dict[str, str]:
    """
    Infer schema from a pandas DataFrame.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary mapping column names to dtype strings
    """
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    logger.info(f"Inferred schema with {len(schema)} columns")
    return schema


def check_schema_changes(old_schema: Dict[str, str], new_schema: Dict[str, str]) -> Dict[str, any]:
    """
    Compare two schemas and detect changes.
    
    Args:
        old_schema: Previous schema dictionary
        new_schema: Current schema dictionary
    
    Returns:
        Dictionary with changes:
        - added_columns: List of newly added column names
        - removed_columns: List of removed column names
        - changed_types: Dict of columns with type changes {col: (old_type, new_type)}
        - is_changed: Boolean indicating if any changes detected
    """
    if old_schema is None:
        logger.info("No previous schema to compare")
        return {
            'added_columns': list(new_schema.keys()),
            'removed_columns': [],
            'changed_types': {},
            'is_changed': True
        }
    
    old_cols = set(old_schema.keys())
    new_cols = set(new_schema.keys())
    
    added = list(new_cols - old_cols)
    removed = list(old_cols - new_cols)
    
    # Check for type changes in common columns
    common_cols = old_cols & new_cols
    changed_types = {}
    for col in common_cols:
        if old_schema[col] != new_schema[col]:
            changed_types[col] = (old_schema[col], new_schema[col])
    
    is_changed = bool(added or removed or changed_types)
    
    result = {
        'added_columns': added,
        'removed_columns': removed,
        'changed_types': changed_types,
        'is_changed': is_changed
    }
    
    if is_changed:
        logger.warning(f"Schema changes detected: {len(added)} added, {len(removed)} removed, {len(changed_types)} type changes")
    else:
        logger.info("No schema changes detected")
    
    return result


def get_schema_summary(schema: Dict[str, str]) -> str:
    """
    Generate a human-readable schema summary.
    
    Args:
        schema: Schema dictionary
    
    Returns:
        Formatted string summary
    """
    lines = ["Schema Summary:", "-" * 40]
    for col, dtype in schema.items():
        lines.append(f"  {col}: {dtype}")
    return "\n".join(lines)


def validate_schema(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that DataFrame contains expected columns.
    
    Args:
        df: Input DataFrame
        expected_columns: List of expected column names
    
    Returns:
        Tuple of (is_valid, missing_columns)
    """
    actual_columns = set(df.columns)
    expected_set = set(expected_columns)
    missing = list(expected_set - actual_columns)
    
    is_valid = len(missing) == 0
    
    if not is_valid:
        logger.warning(f"Schema validation failed. Missing columns: {missing}")
    else:
        logger.info("Schema validation passed")
    
    return is_valid, missing
