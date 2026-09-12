import pytest
import pandas as pd
import numpy as np
from backend.ml.feature_engineering import FeatureEngineer
from backend.ml.train_regressor import RegressorPipeline

def test_regressor_training():
    # Mock data
    np.random.seed(42)
    df = pd.DataFrame({
        'order_date': pd.date_range(start='2023-01-01', periods=100),
        'ship_date': pd.date_range(start='2023-01-03', periods=100),
        'shipping_delay_days': np.random.randint(1, 6, 100),
        'sales': np.random.rand(100) * 1000,
        'profit': np.random.rand(100) * 100,
        'quantity': np.random.randint(1, 10, 100),
        'discount': np.random.rand(100) * 0.5,
        'category': ['Office Supplies', 'Furniture'] * 50,
        'sub_category': ['Paper', 'Chairs'] * 50,
        'shipping_mode': ['Standard Class', 'Second Class'] * 50,
        'region': ['West', 'East'] * 50,
        'segment': ['Consumer', 'Corporate'] * 50
    })
    
    fe = FeatureEngineer(delay_threshold_days=3)
    df_feat = fe.transform(df)
    
    rp = RegressorPipeline()
    metrics = rp.train(df_feat)
    
    assert 'mae' in metrics
    assert 'rmse' in metrics
    assert 'r2' in metrics
    assert rp.model is not None
