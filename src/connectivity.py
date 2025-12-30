import tkinter as tk
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'hostel_mgmt',
    'user': 'postgres',
    'password': 'xxxxxx',
    'host': 'localhost',  # or your database server address
    'port': '5432'        # default PostgreSQL port
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

try:
    # Execute a simple SQL command
    cursor.execute("SELECT version();")

    # Fetch the result
    db_version = cursor.fetchone()
    print("\nPostgreSQL Database Version:", db_version)

    # Correct way to list tables in PostgreSQL
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)

    # Fetch the result
    tables = cursor.fetchall()
    print("\nTables in database:")
    for table in tables:
        print(table[0])

    # Fetch the result
    records = cursor.fetchall()
    for rec in records:
        print(rec)

except Exception as e:
    print("Error connecting to PostgreSQL:", e)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
