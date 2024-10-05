import mysql.connector
from tabulate import tabulate

# Function to connect to MySQL server
def connect_to_mysql():
    while True:
        print("WELCOME TO SQL EDITOR")
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            # Attempt to connect to the database
            conn = mysql.connector.connect(
                host="localhost",  # Replace with your host if needed
                user=username,
                password=password
            )
            print("Logged in successfully!")
            return conn

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("Invalid username or password. Please try again.\n")

# Function to show and select a database
def select_database(conn, cursor):
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    if not databases:
        print("No databases found. Please create one first.")
        return None

    # Displaying databases in tabular format
    print("\nExisting databases:")
    print(tabulate(databases, headers=["Databases"], tablefmt="pretty"))

    # Asking the user to choose a database
    db_choice = int(input("\nSelect a database by number: ")) - 1
    selected_db = databases[db_choice][0]
    conn.database = selected_db
    print(f"Using database '{selected_db}'.")
    return selected_db

# Function to execute dynamic user queries (for custom queries)
def execute_dynamic_query(cursor, query):
    try:
        cursor.execute(query)
        if query.lower().startswith("select"):
            rows = cursor.fetchall()
            if rows:
                headers = [i[0] for i in cursor.description]
                print(tabulate(rows, headers=headers, tablefmt="pretty"))
            else:
                print("No data found.")
        elif query.lower().startswith(("update", "delete", "insert", "create", "drop", "truncate", "alter")):
            print(f"Query executed successfully. Affected rows: {cursor.rowcount}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main SQL editor program
conn = connect_to_mysql()
cursor = conn.cursor()

try:
    # Show existing databases and let the user choose one
    selected_db = select_database(conn, cursor)
    if not selected_db:
        raise Exception("No database selected or created. Exiting.")

    while True:
        task_list = """
        Choose an option:
          1. Show tables
          2. Create a new table
          3. Insert data into a table
          4. Update data in a table
          5. Delete data from a table
          6. Drop a table
          7. Select data (conditional query)
          8. Group by query
          9. Join tables
          10. Run a custom SQL query
          11. Exit
        """
        print(task_list)
        response = int(input("Choose any from this: "))

        # Handling all tasks via match-case
        match response:
            case 1:
                # Show all tables in the selected database
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                if tables:
                    print(tabulate(tables, headers=["Tables"], tablefmt="pretty"))
                else:
                    print("No tables found.")

            case 2:
                # Create a new table
                table_name = input("Enter table name: ")
                column_definitions = input("Enter column definitions (e.g., id INT, name VARCHAR(100)): ")
                query = f"CREATE TABLE {table_name} ({column_definitions})"
                execute_dynamic_query(cursor, query)
                conn.commit()

            case 3:
                # Insert data into a table
                table_name = input("Enter table name: ")
                columns = input("Enter column names (comma-separated): ")
                values = input("Enter values (comma-separated, matching columns): ")
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                execute_dynamic_query(cursor, query)
                conn.commit()

            case 4:
                # Update data in a table
                table_name = input("Enter table name: ")
                set_clause = input("Enter SET clause (e.g., name='John'): ")
                where_clause = input("Enter WHERE condition (e.g., id=1): ")
                query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                execute_dynamic_query(cursor, query)
                conn.commit()

            case 5:
                # Delete data from a table
                table_name = input("Enter table name: ")
                where_clause = input("Enter WHERE condition (e.g., id=1): ")
                query = f"DELETE FROM {table_name} WHERE {where_clause}"
                execute_dynamic_query(cursor, query)
                conn.commit()

            case 6:
                # Drop a table
                table_name = input("Enter table name to drop: ")
                query = f"DROP TABLE {table_name}"
                execute_dynamic_query(cursor, query)
                conn.commit()

            case 7:
                # Select data (conditional query)
                table_name = input("Enter table name: ")
                columns = input("Enter columns to select (comma-separated or * for all): ")
                where_clause = input("Enter WHERE condition (or leave blank for no condition): ")
                query = f"SELECT {columns} FROM {table_name} " + (f"WHERE {where_clause}" if where_clause else "")
                execute_dynamic_query(cursor, query)

            case 8:
                # Group by query
                table_name = input("Enter table name: ")
                group_by_column = input("Enter column to GROUP BY: ")
                query = f"SELECT {group_by_column}, COUNT(*) FROM {table_name} GROUP BY {group_by_column}"
                execute_dynamic_query(cursor, query)

            case 9:
                # Join tables
                table1 = input("Enter first table name: ")
                table2 = input("Enter second table name: ")
                join_condition = input("Enter join condition (e.g., table1.id = table2.id): ")
                query = f"SELECT * FROM {table1} JOIN {table2} ON {join_condition}"
                execute_dynamic_query(cursor, query)

            case 10:
                # Run a custom SQL query
                query = input("Enter your SQL query: ")
                execute_dynamic_query(cursor, query)

            case 11:
                # Exit the editor
                print("Exiting SQL Editor...")
                break

            case _:
                print("Invalid choice, please select a valid option.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed.")
