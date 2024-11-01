import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Establishing the MySQL connection
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aish@2001",
            database="Personal_Diary"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Initialize default admin and user accounts if they do not exist
def initialize_defaults():
    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()

        # Insert default admin if not exists
        cursor.execute("SELECT * FROM Admin WHERE username = %s", ('admin123',))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO Admin (username, password) VALUES (%s, %s)", ('admin123', 'adminpass'))
            print("Default admin account created.")

        # Insert default user if not exists
        cursor.execute("SELECT * FROM User WHERE username = %s", ('user1',))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", ('user1', 'userpass'))
            print("Default user account created.")

        # Commit changes to the database
        connection.commit()

    except Error as e:
        print(f"Error during initialization: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Authentication function with exception handling
def authenticate():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return None, None

    try:
        cursor = connection.cursor()

        # Check if the user is an Admin
        cursor.execute("SELECT * FROM Admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        if admin:
            print("Welcome, Admin!")
            return "admin", username

        # Check if the user is a regular User
