import sqlite3

# Initializing the SQLite database
DB_NAME = "tasks.db"

def init_db():
    """"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tasks(
                       id TEXT PRIMARY KEY,
                       title TEXT NOT NULL,
                       description TEXT,
                       priority INTEGER DEFAULT 0,
                       completed INTEGER DEFAULT 0
                   )
                   """)
    conn.commit()
    conn.close()
    
def get_connection():
    """"""
    return sqlite3.connect(DB_NAME)
    
init_db()