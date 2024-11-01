import mysql.connector
from mysql.connector import Error

# Database connection configuration
db_config = {
    'host': 'localhost',
    'database': 'personal_diary',
    'user': 'root ',
    'password': 'aish@2001'  # Replace with your actual password
}

# Set up the database and tables (this is typically done only once)
def setup_database():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                date DATE NOT NULL
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to add an entry
def add_entry(title, content, date):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (title, content, date) VALUES (%s, %s, %s)', (title, content, date))
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to view all entries
def view_entries():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entries')
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to delete an entry
def delete_entry(entry_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM entries WHERE id = %s', (entry_id,))
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to update an entry
def update_entry(entry_id, title, content, date):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('UPDATE entries SET title = %s, content = %s, date = %s WHERE id = %s', (title, content, date, entry_id))
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Main menu
def menu():
    print("Welcome to the Personal Diary Application")

    while True:
        print("\n1. Add Entry")
        print("2. View Entries")
        print("3. Delete Entry")
        print("4. Update Entry")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            content = input("Enter content: ")
            date = input("Enter date (YYYY-MM-DD): ")
            add_entry(title, content, date)
            print("Entry added successfully!")

        elif choice == '2':
            entries = view_entries()
            if entries:
                for entry in entries:
                    print(f"ID: {entry[0]}, Title: {entry[1]}, Content: {entry[2]}, Date: {entry[3]}")
            else:
                print("No entries found.")

        elif choice == '3':
            entry_id = int(input("Enter the ID of the entry to delete: "))
            delete_entry(entry_id)
            print("Entry deleted successfully!")

        elif choice == '4':
            entry_id = int(input("Enter the ID of the entry to update: "))
            title = input("Enter new title: ")
            content = input("Enter new content: ")
            date = input("Enter new date (YYYY-MM-DD): ")
            update_entry(entry_id, title, content, date)
            print("Entry updated successfully!")

        elif choice == '5':
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    setup_database()
    menu()
