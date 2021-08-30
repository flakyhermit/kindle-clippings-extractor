#!/usr/bin/env python3

import sqlite3

class Db:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()

        # Create tables if they do not exists
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        name TEXT,
        author TEXT);""")
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS clippings (
        clip_id INTEGER PRIMARY KEY,
        book_id INTEGER,
        FOREIGN KEY (book_id)
            REFERENCES books (book_id),
        location INTEGER,
        page INTEGER,
        highlight TEXT,
        note TEXT);""")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_book(self, book):
        self.cur.execute("INSERT books (title, author) VALUES (:title, :author)", {title: book.title, author: book.author})

    def insert_clip(self, clip):
        """Insert a clip into database."""
        self.cur.exeutemany("""INSERT into clippings(text)
        VALUES (?,?,?)""", clip)

    def check_if_exists(clip):
        """Check if clip already exists in db."""
