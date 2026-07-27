# -*- coding: utf-8 -*-

import sqlite3


def normalize_digits(text):
    if text is None:
        return ""
    s = str(text)
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    western_digits = "0123456789"
    for a, w in zip(arabic_digits, western_digits):
        s = s.replace(a, w)
    return s


class Database:
    def __init__(self, path="inventory.db"):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER DEFAULT 0,
            imported INTEGER DEFAULT 0,
            sold INTEGER DEFAULT 0
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            action TEXT NOT NULL,
            amount INTEGER NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def add_item(self, name):
        name = str(name).strip()
        if not name:
            return False

        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO items(name) VALUES(?)",
                (name,)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_item(self, old_name, new_name):
        old_name = str(old_name).strip()
        new_name = str(new_name).strip()
        if not old_name or not new_name:
            return False

        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE items SET name=? WHERE name=?",
                (new_name, old_name)
            )
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def delete_item(self, name):
        name = str(name).strip()
        if not name:
            return False

        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM items WHERE name=?",
            (name,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def get_items(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT name, quantity, imported, sold
            FROM items
            ORDER BY id ASC
        """)
        return cur.fetchall()

    def get_item_names(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM items ORDER BY id ASC")
        return [row["name"] for row in cur.fetchall()]

    def add_import(self, name, amount):
        name = str(name).strip()
        amount = int(normalize_digits(amount) or 0)

        if not name or amount <= 0:
            return False

        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE items
            SET quantity = quantity + ?,
                imported = imported + ?
            WHERE name=?
            """,
            (amount, amount, name)
        )

        if cur.rowcount == 0:
            return False

        cur.execute(
            """
            INSERT INTO movements(item, action, amount)
            VALUES(?,?,?)
            """,
            (name, "وارد", amount)
        )

        self.conn.commit()
        return True

    def add_sale(self, name, amount):
        name = str(name).strip()
        amount = int(normalize_digits(amount) or 0)

        if not name or amount <= 0:
            return False

        cur = self.conn.cursor()
        cur.execute(
            "SELECT quantity FROM items WHERE name=?",
            (name,)
        )
        row = cur.fetchone()

        if not row:
            return False

        current_qty = int(row["quantity"])
        if current_qty < amount:
            return False

        cur.execute(
            """
            UPDATE items
            SET quantity = quantity - ?,
                sold = sold + ?
            WHERE name=?
            """,
            (amount, amount, name)
        )

        cur.execute(
            """
            INSERT INTO movements(item, action, amount)
            VALUES(?,?,?)
            """,
            (name, "بيع", amount)
        )

        self.conn.commit()
        return True

    def get_stock_report(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT name, quantity, imported, sold
            FROM items
            ORDER BY id ASC
        """)
        return cur.fetchall()

    def close(self):
        try:
            self.conn.close()
        except:
            pass