import os
import snowflake.connector
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def inspect_db():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        role=os.getenv('SNOWFLAKE_ROLE')
    )
    
    cur = conn.cursor()
    
    with open('schema_output.txt', 'w', encoding='utf-8') as f:
        f.write("--- TABLES ---\n")
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        for table in tables:
            f.write(table[1] + "\n")
            
        for table in tables:
            table_name = table[1]
            f.write(f"\n--- SCHEMA FOR {table_name} ---\n")
            cur.execute(f"DESCRIBE TABLE {table_name}")
            cols = cur.fetchall()
            for col in cols:
                f.write(f"{col[0]} - {col[1]}\n")
                
            f.write(f"\n--- SAMPLE FOR {table_name} ---\n")
            cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cur.fetchall()
            for row in rows:
                f.write(str(row) + "\n")
            
            f.write(f"\n--- COUNT FOR {table_name} ---\n")
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            f.write(f"Total Rows: {cur.fetchone()[0]}\n")
        
    cur.close()
    conn.close()

if __name__ == '__main__':
    inspect_db()
