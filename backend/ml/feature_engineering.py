import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self, delay_threshold_days=3):
        self.delay_threshold_days = delay_threshold_days

    def add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Adding temporal features...")
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_quarter'] = df['order_date'].dt.quarter
        df['order_day'] = df['order_date'].dt.day
        df['day_of_week'] = df['order_date'].dt.dayofweek
        df['week_of_year'] = df['order_date'].dt.isocalendar().week.astype(int)
        return df

    def add_shipping_order_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Adding shipping and order features...")
        # Classification target
        df['delay_flag'] = (df['shipping_delay_days'] > self.delay_threshold_days).astype(int)
        
        # Log transforms for skewed numerical features
        df['log_sales'] = np.log1p(df['sales'])
        df['log_profit'] = np.log1p(df['profit'] - df['profit'].min() + 1)
        
        return df

    def add_historical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Adding historical operational features...")
        # To avoid data leakage, we should sort by date and compute rolling stats, 
        # or compute historical stats purely on the training set.
        # For simplicity in this demo class, we will calculate regional and category averages
        # using transform which does cause leakage IF used directly on whole dataset.
        # However, for an academic demo, we compute rolling aggregates properly.
        
        df = df.sort_values(by='order_date').reset_index(drop=True)
        
        # Group by mode and calculate expanding average duration (no future leakage)
        df['historical_mode_duration'] = df.groupby('shipping_mode')['shipping_delay_days'].transform(lambda x: x.expanding().mean().shift(1))
        df['historical_mode_duration'] = df['historical_mode_duration'].fillna(df['historical_mode_duration'].median())
        
        # Mode delay rate
        df['historical_mode_delay_rate'] = df.groupby('shipping_mode')['delay_flag'].transform(lambda x: x.expanding().mean().shift(1))
        df['historical_mode_delay_rate'] = df['historical_mode_delay_rate'].fillna(df['historical_mode_delay_rate'].median())
        
        return df
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_temporal_features(df)
        df = self.add_shipping_order_features(df)
        df = self.add_historical_features(df)
        
        # Select final features
        features = [
            'order_year', 'order_month', 'order_quarter', 'day_of_week', 'week_of_year',
            'quantity', 'log_sales', 'discount', 'log_profit',
            'historical_mode_duration', 'historical_mode_delay_rate'
        ]
        
        # Categorical features for one-hot encoding
        cat_features = ['category', 'sub_category', 'shipping_mode', 'region', 'segment']
        
        # Ensure target variables and ID columns are present
        target_cols = ['shipping_delay_days', 'delay_flag']
        id_cols = ['order_id', 'order_date', 'ship_date', 'customer_id', 'customer_name', 'product_id', 'product_name']
        
        # Filter dataframe to only these columns (if they exist)
        keep_cols = features + cat_features + target_cols + id_cols
        keep_cols = [c for c in keep_cols if c in df.columns]
        df = df[keep_cols].copy()
        
        logger.info("One-hot encoding categorical features...")
        df = pd.get_dummies(df, columns=cat_features, drop_first=True)
        
        logger.info(f"Final feature matrix shape: {df.shape}")
        return df
