"""
In-memory data store for maintaining state across runs.
Stores schema and other metadata for comparison and tracking.
"""

from typing import Any, Dict, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryStore:
    """
    Simple in-memory key-value store for persisting data across agent runs.
    Used primarily for tracking schema evolution and dataset metadata.
    """
    
    def __init__(self):
        """Initialize empty memory store."""
        self._store: Dict[str, Any] = {}
        logger.info("MemoryStore initialized")
    
    def save(self, key: str, value: Any) -> None:
        """
        Save a value to the memory store.
        
        Args:
            key: Storage key identifier
            value: Value to store (must be serializable)
        """
        self._store[key] = value
        logger.debug(f"Saved to memory: {key}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from the memory store.
        
        Args:
            key: Storage key identifier
            default: Default value if key not found
        
        Returns:
            Stored value or default if key doesn't exist
        """
        value = self._store.get(key, default)
        if value is None:
            logger.debug(f"Key not found in memory: {key}")
        return value
    
    def has(self, key: str) -> bool:
        """
        Check if a key exists in the store.
        
        Args:
            key: Storage key identifier
        
        Returns:
            True if key exists, False otherwise
        """
        return key in self._store
    
    def delete(self, key: str) -> None:
        """
        Remove a key from the store.
        
        Args:
            key: Storage key identifier
        """
        if key in self._store:
            del self._store[key]
            logger.debug(f"Deleted from memory: {key}")
    
    def clear(self) -> None:
        """Clear all data from the store."""
        self._store.clear()
        logger.info("Memory store cleared")
    
    def keys(self) -> list:
        """Return list of all keys in the store."""
        return list(self._store.keys())
    
    def __repr__(self) -> str:
        return f"MemoryStore(keys={len(self._store)})"
