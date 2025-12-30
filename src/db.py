import psycopg2
import constants

# Central Configuration - The only place your password exists
DB_PARAMS = {
    'host': "localhost",
    'port': "5432",
    'database': "hostel_mgmt",
    'user': "postgres",
    'password': "<password>" # Your password
}

def get_db_connection():
    """
    Creates and returns a connection to the database.
    Returns None if connection fails.
    """
    try:
        connection = psycopg2.connect(**DB_PARAMS)
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None

def login(username, password):
    """
    Checks credentials and returns the user role (STAFF or HOSTELLER).
    Returns None if login fails.
    """
    connection = None
    try:
        connection = get_db_connection()
        if not connection:
            return None
            
        cursor = connection.cursor()
        
        # simplified query
        query = "SELECT person_type FROM login WHERE username = %s AND password = %s;"
        cursor.execute(query, (username, password))
        
        row = cursor.fetchone()
        
        if row:
            person_type = row[0]
            if person_type == "staff":
                return constants.STAFF
            elif person_type == "hosteller":
                return constants.HOSTELLER
        
        return None # Login failed

    except Exception as error:
        print(f"Login Error: {error}")
        return None

    finally:
        if connection:
            connection.close()