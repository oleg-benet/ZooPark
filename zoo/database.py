import sqlite3 as sq

db = sq.connect('my_base.db')
cur = db.cursor()



cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT ,'
                'user_id INTEGER,'
                ' name TEXT,'
                'feedback TEXT)')

db.commit()