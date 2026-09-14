import sqlite3
import os
import logging
import snowflake.connector
from .snowflake_service import snowflake_service
from ..config import settings

logger = logging.getLogger(__name__)

class DBRepository:
    def __init__(self):
        self.mode = settings.DATABASE_MODE
        self.local_db_path = "local_data/supplyprescript.db"
        if self.mode == "local":
            self._init_local_db()

    def _init_local_db(self):
        os.makedirs(os.path.dirname(self.local_db_path), exist_ok=True)
        conn = sqlite3.connect(self.local_db_path)
        
        with open("database/schema.sql", "r") as f:
            schema = f.read()
        
        # SQLite doesn't support BOOLEAN natively but understands the keyword.
        conn.executescript(schema)
        conn.commit()
        conn.close()

    def execute(self, query: str, params: tuple = None):
        if self.mode == "local":
            conn = sqlite3.connect(self.local_db_path)
            try:
                cur = conn.cursor()
                if params:
                    # SQLite uses ?, Snowflake might use %s, but we can do a simple replace or just rely on parameterized.
                    # Wait, Snowflake python connector uses %s for format, or ? for qmark. Let's assume standard qmark.
                    # Standardizing on SQLite style for local demo
                    cur.execute(query.replace("%s", "?"), params)
                else:
                    cur.execute(query)
                conn.commit()
            finally:
                conn.close()
        else:
            # Snowflake
            if not snowflake_service.conn:
                snowflake_service.connect()
            cur = snowflake_service.conn.cursor()
            try:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                snowflake_service.conn.commit()
            finally:
                cur.close()

    def fetchall(self, query: str, params: tuple = None):
        if self.mode == "local":
            conn = sqlite3.connect(self.local_db_path)
            conn.row_factory = sqlite3.Row
            try:
                cur = conn.cursor()
                if params:
                    cur.execute(query.replace("%s", "?"), params)
                else:
                    cur.execute(query)
                rows = cur.fetchall()
                return [dict(ix) for ix in rows]
            finally:
                conn.close()
        else:
            if not snowflake_service.conn:
                snowflake_service.connect()
            cur = snowflake_service.conn.cursor(snowflake.connector.DictCursor)
            try:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                return cur.fetchall()
            finally:
                cur.close()

db_repository = DBRepository()
