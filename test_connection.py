from sqlalchemy import create_engine, text
from config.db_config import CONNECTION_STRING

# Create engine
engine = create_engine(CONNECTION_STRING)

try:
    with engine.connect() as conn:
        # Use text() for SQL string
        result = conn.execute(text("SELECT 1"))
        print("✅ Connection successful:", result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)
