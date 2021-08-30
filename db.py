#!/usr/bin/env python3

import sqlite3

class Db:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()

        # Create tables if they do not exists
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT);""")
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS clippings (
        clip_id INTEGER PRIMARY KEY,
        location INTEGER,
        page INTEGER,
        timestamp INTEGER,
        highlight TEXT,
        note TEXT,
        book_id INTEGER,
        FOREIGN KEY (book_id) REFERENCES books (book_id));""")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_book_id (self, title, author):
        self.cur.execute("""SELECT book_id, author, title
                            FROM books
                            WHERE title=? AND author=?""",
                         (title, author))
        _id = self.cur.fetchone()
        return _id

    def insert_book(self, title, author):
        self.cur.execute("""SELECT book_id, author, title
                            FROM books
                            WHERE title=? AND author=?""",
                         (title, author))
        result = self.cur.fetchone()
        if result:
            raise Exception('Book already exists with id: %s' % result[0])
        self.cur.execute("""INSERT INTO books (title, author)
                            VALUES (?, ?)""", (title, author))
        self.conn.commit()
        _id = self.cur.execute("""SELECT book_id FROM books WHERE title=? AND author=?""",
                                  (title, author)).fetchone()
        return _id

    def insert_clip(self, clip):
        """Insert a clip into database."""
        self.cur.exeute("""INSERT into
                           clippings(location, page, timestamp, highlight, note, book_id)
                           VALUES (?,?,?,?,?,?)""", clip)
        self.conn.commit()

    def insert_clips(self, clips):
        """Insert many clips"""
        self.cur.exeutemany("""INSERT into
                           clippings(location, page, timestamp, highlight, note, book_id)
                           VALUES (?,?,?,?,?,?)""", clips)
        self.conn.commit()

    # Functions to print the database tables
    def print_clips(self):
        results = self.cur.execute("""SELECT * FROM clippings""").fetchall()
        print(results)

    def print_books(self):
        results = self.cur.execute("""SELECT * FROM books""").fetchall()
        print(results)
