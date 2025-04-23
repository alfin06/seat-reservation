import pymysql

def create_database():
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root'
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Create database
        cursor.execute('CREATE DATABASE IF NOT EXISTS seat_reservation')
        
        print("Database created successfully!")
        
    except pymysql.Error as e:
        print(f"Error creating database: {e}")
        
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database() 