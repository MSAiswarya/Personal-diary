import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Establishing the MySQL connection
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aish@2001",  # Change to your MySQL password
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
        cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            print("Welcome, User!")
            return "user", user[0]  # Return user ID for diary functionality

        print("Invalid username or password.")
        return None, None

    except Error as e:
        print(f"Error during authentication: {e}")
        return None, None
    finally:
        if connection.is_connected():
            connection.close()


def create_admin(username, password):
    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        print("New Admin created successfully.")
    except Error as e:
        print(f"Failed to create admin1: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to add a diary entry
def add_diary_entry(user_id):
    entry = input("Write your diary entry: ")

    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO DiaryEntry (user_id, entry) VALUES (%s, %s)", (user_id, entry))
        connection.commit()
        print("Diary entry added successfully.")
    except Error as e:
        print(f"Failed to add diary entry: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to view diary entries
def view_diary_entries(user_id):
    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, entry, created_at FROM DiaryEntry WHERE user_id = %s", (user_id,))
        entries = cursor.fetchall()
        if entries:
            print("\nDiary Entries:")
            for entry in entries:
                print(f"ID: {entry[0]}, Date: {entry[2]}, Entry: {entry[1]}")
        else:
            print("No diary entries found.")
    except Error as e:
        print(f"Failed to fetch diary entries: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to update a diary entry
def update_diary_entry(user_id):
    view_diary_entries(user_id)
    entry_id = input("Enter the ID of the entry you want to update: ")
    new_entry = input("Enter the updated diary entry: ")

    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE DiaryEntry SET entry = %s WHERE id = %s AND user_id = %s", (new_entry, entry_id, user_id))
        connection.commit()
        if cursor.rowcount:
            print("Diary entry updated successfully.")
        else:
            print("Entry not found or you do not have permission to update it.")
    except Error as e:
        print(f"Failed to update diary entry: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function to delete a diary entry
def delete_diary_entry(user_id):
    view_diary_entries(user_id)
    entry_id = input("Enter the ID of the entry you want to delete: ")

    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM DiaryEntry WHERE id = %s AND user_id = %s", (entry_id, user_id))
        connection.commit()
        if cursor.rowcount:
            print("Diary entry deleted successfully.")
        else:
            print("Entry not found or you do not have permission to delete it.")
    except Error as e:
        print(f"Failed to delete diary entry: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Admin function to add a new user
def add_user():
    username = input("Enter new username: ")
    password = getpass("Enter new password: ")

    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        print("User added successfully.")
    except Error as e:
        print(f"Failed to add user: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Admin function to modify an existing user's password
def modify_user():
    username = input("Enter username to modify: ")
    new_password = getpass("Enter new password: ")

    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE User SET password = %s WHERE username = %s", (new_password, username))
        connection.commit()
        if cursor.rowcount:
            print("Password updated successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"Failed to modify user: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Admin function to delete a user
def delete_user():
    username = input("Enter the username to delete: ")

    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM User WHERE username = %s", (username,))
        connection.commit()
        if cursor.rowcount:
            print("User deleted successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"Failed to delete user: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Function for Admin to change a user's username and password
def change_user_credentials():
    current_username = input("Enter the current username: ")
    new_username = input("Enter the new username: ")
    new_password = getpass("Enter the new password: ")

    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        # Update username and password for the specified user
        cursor.execute("UPDATE User SET username = %s, password = %s WHERE username = %s", 
                       (new_username, new_password, current_username))
        connection.commit()
        if cursor.rowcount:
            print("Username and password updated successfully.")
        else:
            print("User not found.")
    except Error as e:
        print(f"Failed to change user credentials: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Main program with updated admin options
def main():
    # Initialize default admin and user accounts
    initialize_defaults()

    while True:
        print("\n1. Sign In")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            role, username = authenticate()
            if role == "admin":
                while True:
                    print("\nAdmin Options:")
                    print("1. Add a new user")
                    print("2. Modify user password")
                    print("3. Delete user")
                    print("4. Change username and password of a user")
                    print("5. Exit")
                    admin_choice = input("Choose an option: ")

                    if admin_choice == "1":
                        add_user()
                    elif admin_choice == "2":
                        modify_user()
                    elif admin_choice == "3":
                        delete_user()
                    elif admin_choice == "4":
                        change_user_credentials()
                    elif admin_choice == "5":
                        print("Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif role == "user":
                user_id = username  # Use user ID for diary functionality
                while True:
                    print("\nUser Options:")
                    print("1. Add Diary Entry")
                    print("2. View Diary Entries")
                    print("3. Update Diary Entry")
                    print("4. Delete Diary Entry")
                    print("5. Sign Out")
                    user_choice = input("Choose an option: ")

                    if user_choice == "1":
                        add_diary_entry(user_id)
                    elif user_choice == "2":
                        view_diary_entries(user_id)
                    elif user_choice == "3":
                        update_diary_entry(user_id)
                    elif user_choice == "4":
                        delete_diary_entry(user_id)
                    elif user_choice == "5":
                        print("Signed out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Sign-in failed. Exiting the program.")

        elif choice == "2":
            username = input("Enter a username: ")
            password = getpass("Enter a password: ")
            create_admin(username, password)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
