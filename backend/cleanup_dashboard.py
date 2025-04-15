import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def cleanup_database():
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='seat_reservation'
        )
        
        cursor = connection.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Drop all tables
        for (table_name,) in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"Dropped table {table_name}")
            except Exception as e:
                print(f"Error dropping {table_name}: {e}")
        
        # Enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Commit the changes
        connection.commit()
        print("Successfully cleaned up database")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    cleanup_database() 