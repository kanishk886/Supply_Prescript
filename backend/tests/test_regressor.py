import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from backend.ml.train_regressor import train_regressor

@patch('backend.ml.train_regressor.pd.read_sql')
@patch('backend.ml.train_regressor.joblib.dump')
@patch('backend.ml.train_regressor.version_manager.register_model')
def test_regressor_training(mock_register, mock_dump, mock_read_sql):
    # Mock data
    np.random.seed(42)
    df = pd.DataFrame({
        'delay_days': [1, 5] * 50,  # All > 0 to simulate delayed orders
        'lead_time': np.random.randint(1, 10, 100),
        'quantity': np.random.randint(1, 100, 100),
        'inventory': np.random.randint(0, 1000, 100),
        'demand': np.random.randint(10, 500, 100),
        'shipping_cost': np.random.rand(100) * 100
    })
    
    mock_read_sql.return_value = df
    
    # Should run without error
    train_regressor()
    
    # Verify it attempted to save
    mock_dump.assert_called_once()
    mock_register.assert_called_once()

