"""
Tests for QAAgent.
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.qa_agent import QAAgent


class TestQAAgent:
    """Test suite for QAAgent."""
    
    @pytest.fixture
    def agent(self):
        """Create QAAgent instance for testing."""
        return QAAgent()
    
    @pytest.fixture
    def clean_df(self):
        """Create a clean DataFrame with no quality issues."""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'score': [85.5, 90.0, 88.5, 92.0, 87.5]
        })
    
    @pytest.fixture
    def messy_df(self):
        """Create a DataFrame with quality issues."""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 2],  # Duplicate row (id=2)
            'name': ['Alice', 'Bob', None, 'David', 'Bob'],  # Missing value
            'age': [25, 30, 35, None, 30],  # Missing value
            'score': [85.5, 90.0, 88.5, 92.0, 90.0]
        })
    
    @pytest.fixture
    def sample_csv_df(self):
        """Load sample CSV file as DataFrame."""
        csv_path = os.path.join("data", "sample_sales.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        return None
    
    def test_agent_initialization(self, agent):
        """Test that QAAgent initializes properly."""
        assert agent is not None
        assert isinstance(agent, QAAgent)
    
    def test_run_on_clean_data(self, agent, clean_df):
        """Test QA on clean data with no issues."""
        results = agent.run(clean_df)
        
        # Check structure
        assert 'missing_values' in results
        assert 'duplicate_rows' in results
        assert 'null_fraction' in results
        
        # Should have no issues
        assert len(results['missing_values']) == 0
        assert results['duplicate_rows'] == 0
        assert len(results['null_fraction']) == 0
    
    def test_run_on_messy_data(self, agent, messy_df):
        """Test QA on data with quality issues."""
        results = agent.run(messy_df)
        
        # Should detect missing values
        assert len(results['missing_values']) > 0
        assert 'name' in results['missing_values']
        assert 'age' in results['missing_values']
        
        # Should detect duplicates
        assert results['duplicate_rows'] > 0
        
        # Should calculate null fractions
        assert len(results['null_fraction']) > 0
    
    def test_missing_value_detection(self, agent, messy_df):
        """Test missing value detection accuracy."""
        results = agent.run(messy_df)
        
        missing = results['missing_values']
        
        # Check counts
        assert missing['name'] == 1
        assert missing['age'] == 1
    
    def test_duplicate_detection(self, agent, messy_df):
        """Test duplicate row detection."""
        results = agent.run(messy_df)
        
        # Should detect 1 duplicate (row with id=2 appears twice)
        assert results['duplicate_rows'] == 1
    
    def test_null_fraction_calculation(self, agent, messy_df):
        """Test null fraction calculation."""
        results = agent.run(messy_df)
        
        null_frac = results['null_fraction']
        
        # Check fractions (1 out of 5 rows = 0.2)
        assert null_frac['name'] == pytest.approx(0.2, rel=1e-9)
        assert null_frac['age'] == pytest.approx(0.2, rel=1e-9)
    
    def test_get_data_summary(self, agent, clean_df):
        """Test data summary generation."""
        summary = agent.get_data_summary(clean_df)
        
        assert 'total_rows' in summary
        assert 'total_columns' in summary
        assert 'numeric_columns' in summary
        assert 'categorical_columns' in summary
        
        assert summary['total_rows'] == 5
        assert summary['total_columns'] == 4
    
    def test_sample_csv_analysis(self, agent, sample_csv_df):
        """Test QA on sample sales CSV."""
        if sample_csv_df is None:
            pytest.skip("Sample CSV not found")
        
        results = agent.run(sample_csv_df)
        
        # Should detect missing values in sample_sales.csv
        assert isinstance(results['missing_values'], dict)
        assert isinstance(results['duplicate_rows'], int)
        
        # Sample has missing values in 'price' and 'region'
        if len(results['missing_values']) > 0:
            assert 'price' in results['missing_values'] or 'region' in results['missing_values']
        
        # Sample has 1 duplicate row
        assert results['duplicate_rows'] >= 1
    
    def test_empty_dataframe(self, agent):
        """Test QA on empty DataFrame."""
        empty_df = pd.DataFrame()
        results = agent.run(empty_df)
        
        assert results['missing_values'] == {}
        assert results['duplicate_rows'] == 0
        assert results['null_fraction'] == {}
    
    def test_all_missing_column(self, agent):
        """Test QA on DataFrame with column of all missing values."""
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [None, None, None]
        })
        
        results = agent.run(df)
        
        assert 'col2' in results['missing_values']
        assert results['missing_values']['col2'] == 3
        assert results['null_fraction']['col2'] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
