import pyodbc


class SQLDatabase:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            return []

    def execute_transaction(self, queries):
        try:
            self.cursor.execute("BEGIN TRANSACTION")
            for query in queries:
                self.cursor.execute(query)
            self.cursor.execute("COMMIT")
            return True
        except pyodbc.Error as e:
            print(f"Error executing transaction: {e}")
            self.cursor.execute("ROLLBACK")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# # Example usage
# connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=your_database_name;UID=your_username;PWD=your_password"
# database = SQLDatabase(connection_string)

# # Connect to the database
# database.connect()

# # Execute a query
# rows = database.execute_query("SELECT * FROM your_table_name")
# print(rows)

# # Execute a transaction
# queries = [
#     "INSERT INTO your_table_name (column1, column2) VALUES ('value1', 'value2')",
#     "UPDATE your_table_name SET column1='new_value' WHERE column2='value2'"
# ]
# success = database.execute_transaction(queries)
# if success:
#     print("Transaction executed successfully!")
# else:
#     print("Transaction failed.")

# # Disconnect from the database
# database.disconnect()
