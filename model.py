import sqlite3

def create_table():
    # Connect to the database
    conn = sqlite3.connect("mydata_db.db")
    cursor = conn.cursor()

    # Create a new table with the correct schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mydata (
            id INTEGER PRIMARY KEY,
            surname TEXT,
            email TEXT,
            street TEXT,
            apartment TEXT,
            city TEXT
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

create_table()

