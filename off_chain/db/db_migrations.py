import sqlite3

con = sqlite3.connect("ADIChain")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("""CREATE TABLE Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
            );""")
'''cur.execute("""
            INSERT INTO Users VALUES
            ('1','carlo', '123456'),
            ('2', 'marco', 'qwerty')
            """)'''
con.commit()
con.close()