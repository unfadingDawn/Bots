import datetime
import sqlite3


def insert_comment(id: int, date: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("INSERT INTO comments VALUES (?, ?)", (id, date))


def delete_comment(id: int):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM comments WHERE id = ?", (id,))


def delete_comment_with_date(date: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM comments WHERE date = ?", (date,))


def get_comments():
    with sqlite3.connect("comments.db") as conn:
        return conn.execute("SELECT * FROM comments").fetchall()


def get_date(id: int):
    with sqlite3.connect("comments.db") as conn:
        result = conn.execute("SELECT * FROM comments WHERE id = ?", (id,)).fetchone()
        if result is not None:
            return result[1]


def comment_exists(date: str):
    with sqlite3.connect("comments.db") as conn:
        result = conn.execute("SELECT * FROM comments WHERE date = ?", (date,)).fetchone()
        if result is not None:
            return True
        return False


def clear_db():
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM comments WHERE date = ?",
                     ((datetime.date.today() - datetime.timedelta(days=2)).isoformat(),))


def insert_like(user: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("INSERT INTO likes VALUES (?)", (user,))


def delete_like(user: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM likes WHERE user = ?", (user,))


def get_likes():
    with sqlite3.connect("comments.db") as conn:
        return conn.execute("SELECT * FROM likes").fetchall()


def like_exists(name: str):
    with sqlite3.connect("comments.db") as conn:
        result = conn.execute("SELECT * FROM likes WHERE user = ?", (name,)).fetchone()
        if result is not None:
            return True
        return False


def insert_signal(id: int, pair: str, date: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("INSERT INTO signals VALUES (?, ?, ?)", (id, pair, date))


def delete_signal(id: int):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM signals WHERE id = ?", (id,))


def get_signals():
    with sqlite3.connect("comments.db") as conn:
        return conn.execute("SELECT * FROM signals").fetchall()


def signal_exists(id: int):
    with sqlite3.connect("comments.db") as conn:
        result = conn.execute("SELECT * FROM signals WHERE id = ?", (id,)).fetchone()
        if result is not None:
            return True
        return False

def insert_succsignal(id: int, pair: str, date: str):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("INSERT INTO succ_signals VALUES (?, ?, ?)", (id, pair, date))


def delete_succsignal(id: int):
    with sqlite3.connect("comments.db") as conn:
        conn.execute("DELETE FROM succ_signals WHERE id = ?", (id,))


def get_succsignals():
    with sqlite3.connect("comments.db") as conn:
        return conn.execute("SELECT * FROM succ_signals").fetchall()


def succsignal_exists(id: int):
    with sqlite3.connect("comments.db") as conn:
        result = conn.execute("SELECT * FROM succ_signals WHERE id = ?", (id,)).fetchone()
        if result is not None:
            return True
        return False

