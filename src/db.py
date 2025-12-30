import constants
import psycopg2



def getConnection():
    try:
        # Database connection parameters
        host = "localhost"  # or your host
        database = "hms"
        user = "hms_user"
        password = "pass8967"
        # Attempt to connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
    except Exception as error:
        return None
    return connection

def closeConnection(connection):
    try:
        connection.close()
    except Exception as error:
        print("Unable to close database connection")

def login(user,password):
    connection = None
    try:
        # Attempt to connect to the PostgreSQL database
        connection = getConnection()
        cursor = connection.cursor()
        query ="SELECT person_type FROM login where username= %s and password = %s ;"
        data =(user,password)
        cursor.execute(query,data)
        rows = cursor.fetchall()
        if rows[0][0] == "staff":
            return constants.STAFF
        if rows[0][0] == "hosteller":
            return constants.HOSTELLER


    except Exception as error:
        print(f"Error while connecting to PostgreSQL: {error}")

    finally:
        # Close the connection
        closeConnection(connection)

login("john_doe","password123")