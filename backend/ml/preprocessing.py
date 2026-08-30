import pandas as pd
import numpy as np
import logging
from ..app.services.snowflake_service import snowflake_service

logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self):
        pass

    def load_data(self) -> pd.DataFrame:
        """Load data from MetricMind Snowflake database."""
        logger.info("Loading data from Snowflake: FCT_SALES")
        query = "SELECT * FROM FCT_SALES"
        df = snowflake_service.fetch_pandas(query)
        logger.info(f"Loaded {len(df)} rows.")
        return df
        
    def validate_quality(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement data quality validation."""
        logger.info("Validating data quality...")
        
        # Report before cleaning
        total_rows = len(df)
        total_cols = len(df.columns)
        missing_values = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        logger.info(f"Initial shape: {total_rows}x{total_cols}")
        logger.info(f"Missing values: {missing_values}")
        logger.info(f"Duplicate rows: {duplicate_rows}")
        
        return df

    def handle_dates_and_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implement date and duplicate handling."""
        logger.info("Handling dates and duplicates...")
        
        # Drop duplicates
        df = df.drop_duplicates()
        
        # Handle missing values - drop rows where critical dates are missing
        df = df.dropna(subset=['Order.Date', 'Ship.Date'])
        
        # Date parsing
        # Snowflake might return datetime objects, but ensure they are pandas datetime
        df['Order.Date'] = pd.to_datetime(df['Order.Date'], errors='coerce')
        df['Ship.Date'] = pd.to_datetime(df['Ship.Date'], errors='coerce')
        
        # Drop invalid dates
        df = df.dropna(subset=['Order.Date', 'Ship.Date'])
        
        # Calculate target variable: shipping_delay_days
        df['shipping_delay_days'] = (df['Ship.Date'] - df['Order.Date']).dt.days
        
        # Remove negative delays (data anomaly)
        df = df[df['shipping_delay_days'] >= 0]
        
        # Rename columns to standard names
        df = df.rename(columns={
            'Order.ID': 'order_id',
            'Order.Date': 'order_date',
            'Ship.Date': 'ship_date',
            'Ship.Mode': 'shipping_mode',
            'Customer.ID': 'customer_id',
            'Customer.Name': 'customer_name',
            'Product.ID': 'product_id',
            'Product.Name': 'product_name',
            'Shipping.Cost': 'shipping_cost'
        })
        
        # Standardize column names to lower case
        df.columns = [col.lower() for col in df.columns]
        
        # Convert numeric columns to float to avoid decimal.Decimal issues
        numeric_cols = ['sales', 'profit', 'discount', 'quantity', 'shipping_cost']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)
        
        logger.info(f"Cleaned shape: {df.shape}")
        return df

    def run_pipeline(self) -> pd.DataFrame:
        df = self.load_data()
        df = self.validate_quality(df)
        df = self.handle_dates_and_duplicates(df)
        return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pipeline = DataPipeline()
    df_clean = pipeline.run_pipeline()
    print(df_clean[['order_id', 'order_date', 'ship_date', 'shipping_delay_days']].head())
