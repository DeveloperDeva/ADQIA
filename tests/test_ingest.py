"""
Tests for IngestAgent.
"""

import pytest
import pandas as pd
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.ingest_agent import IngestAgent


class TestIngestAgent:
    """Test suite for IngestAgent."""
    
    @pytest.fixture
    def agent(self):
        """Create IngestAgent instance for testing."""
        return IngestAgent()
    
    @pytest.fixture
    def sample_csv_path(self):
        """Return path to sample CSV file."""
        return os.path.join("data", "sample_sales.csv")
    
    def test_agent_initialization(self, agent):
        """Test that IngestAgent initializes properly."""
        assert agent is not None
        assert isinstance(agent, IngestAgent)
    
    def test_run_with_valid_file(self, agent, sample_csv_path):
        """Test ingestion of valid CSV file."""
        if not os.path.exists(sample_csv_path):
            pytest.skip(f"Sample file not found: {sample_csv_path}")
        
        df, schema = agent.run(sample_csv_path)
        
        # Check DataFrame is returned
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert len(df.columns) > 0
        
        # Check schema is returned
        assert isinstance(schema, dict)
        assert len(schema) > 0
        assert all(isinstance(k, str) for k in schema.keys())
        assert all(isinstance(v, str) for v in schema.values())
    
    def test_schema_inference(self, agent, sample_csv_path):
        """Test that schema is correctly inferred."""
        if not os.path.exists(sample_csv_path):
            pytest.skip(f"Sample file not found: {sample_csv_path}")
        
        df, schema = agent.run(sample_csv_path)
        
        # Check that schema matches DataFrame columns
        assert set(schema.keys()) == set(df.columns)
        
        # Check that dtypes are strings
        for col in df.columns:
            assert schema[col] == str(df[col].dtype)
    
    def test_run_with_nonexistent_file(self, agent):
        """Test that FileNotFoundError is raised for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            agent.run("nonexistent_file.csv")
    
    def test_validate_file_exists(self, agent, sample_csv_path):
        """Test file validation for existing file."""
        if not os.path.exists(sample_csv_path):
            pytest.skip(f"Sample file not found: {sample_csv_path}")
        
        is_valid = agent.validate_file(sample_csv_path)
        assert is_valid is True
    
    def test_validate_file_not_exists(self, agent):
        """Test file validation for nonexistent file."""
        is_valid = agent.validate_file("nonexistent.csv")
        assert is_valid is False
    
    def test_validate_file_wrong_extension(self, agent):
        """Test file validation for non-CSV file."""
        is_valid = agent.validate_file("some_file.txt")
        assert is_valid is False
    
    def test_sample_data_structure(self, agent, sample_csv_path):
        """Test that sample data has expected structure."""
        if not os.path.exists(sample_csv_path):
            pytest.skip(f"Sample file not found: {sample_csv_path}")
        
        df, schema = agent.run(sample_csv_path)
        
        # Check for expected columns in sample_sales.csv
        expected_columns = ['order_id', 'date', 'product', 'price', 'quantity', 'region', 'customer_id']
        assert all(col in df.columns for col in expected_columns)
    
    def test_handles_missing_values(self, agent, sample_csv_path):
        """Test that ingestion handles files with missing values."""
        if not os.path.exists(sample_csv_path):
            pytest.skip(f"Sample file not found: {sample_csv_path}")
        
        df, schema = agent.run(sample_csv_path)
        
        # Should successfully load even with missing values
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
