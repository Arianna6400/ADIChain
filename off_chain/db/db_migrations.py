import sqlite3

con = sqlite3.connect("ADIChain")
cur = con.cursor()
cur.execute("""CREATE TABLE Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            )""")
cur.execute("""
            INSERT INTO Users VALUES
            ('carlo', '123456')
            ('marco', 'qwerty')
            """)
con.commit()
con.close()