import sqlite3

# Initialize the SQLite database
conn = sqlite3.connect('medi_ar.db')
cursor = conn.cursor()

# Create a table for storing AR image target details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ImageTargets (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
