import snowflake.connector
import pandas as pd
from typing import Optional, List, Dict, Any
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class SnowflakeService:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = snowflake.connector.connect(
                user=settings.SNOWFLAKE_USER,
                password=settings.SNOWFLAKE_PASSWORD,
                account=settings.SNOWFLAKE_ACCOUNT,
                warehouse=settings.SNOWFLAKE_WAREHOUSE,
                database=settings.SNOWFLAKE_DATABASE,
                schema=settings.SNOWFLAKE_SCHEMA,
                role=settings.SNOWFLAKE_ROLE
            )
            logger.info("Successfully connected to Snowflake.")
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            raise e

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor(snowflake.connector.DictCursor)
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def fetch_pandas(self, query: str) -> pd.DataFrame:
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            # fetchall to avoid requiring pandas extra in snowflake-connector initially
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(rows, columns=columns)
        finally:
            if cursor:
                cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()

snowflake_service = SnowflakeService()
