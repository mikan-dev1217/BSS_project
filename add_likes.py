import sqlite3
db=sqlite3.connect("database.db")
db.execute("ALTER TABLE posts ADD COLUMN likes INTEGER DEFAULT 0;")
db.commit()
db.close()