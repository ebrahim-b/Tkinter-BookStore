import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS bookshop (id INTEGER PRIMARY KEY, title text, author text, year integer, isbn integer)")
        self.conn.commit()

    def fetch(self, title=''):
        self.cur.execute("SELECT * FROM bookshop WHERE title LIKE ?", ('%'+title+'%',))
        rows = self.cur.fetchall()
        return rows

    def fetch2(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert(self, title, author, year, isbn):
        self.cur.execute("INSERT INTO bookshop VALUES (NULL, ?, ?, ?, ?)",(title, author, year, isbn))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM bookshop WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE bookshop SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?",
                         (title, author, year, isbn, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()