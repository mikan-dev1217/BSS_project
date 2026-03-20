import sqlite3
db=sqlite3.connect("database.db")
db.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
db.execute("""
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    post_id INTEGER,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT (DATETIME('now','localtime'))
)
""")
db.commit()
db.close()