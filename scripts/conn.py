import pyodbc

def create_connection():
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=#Replace your database name;"
        "Database=msdb;"  # 🔑 SQL Agent Jobs live here
        "UID=<User>;"
        "PWD=<Password>;"
        "Persist Security Info=True;"
        "Encrypt=True;"
        "TrustServerCertificate=True;"
        "Command Timeout=0;"
    )

    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print("DB Connection Error:", e)
        return None
