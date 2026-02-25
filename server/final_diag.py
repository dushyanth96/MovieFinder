import os
import mysql.connector
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

def test():
    print("--- DB Connection Diagnostic ---")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    print(f"Target: {host}:{port}")
    print(f"User: {user}")
    print(f"DB: {db_name}")
    
    try:
        print("\nAttempting connection...")
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=int(port),
            ssl_disabled=False,
            connection_timeout=10
        )
        print("✅ SUCCESS: Connected to Aiven!")
        db.close()
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
