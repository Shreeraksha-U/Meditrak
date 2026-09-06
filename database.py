import sqlite3
import pandas as pd

from datetime import datetime

DB_PATH = "meditrak.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            store TEXT,
            medicine TEXT,
            item_id TEXT,
            category TEXT,
            price REAL,
            promotion INTEGER,
            holiday INTEGER,
            forecast_date TEXT,
            day_of_week TEXT,
            month TEXT,
            is_weekend INTEGER,
            predicted_units REAL,
            demand_level TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# USER QUERIES
# -------------------------------

def create_user(username, password_hash, salt):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (username, password_hash, salt, datetime.now().isoformat())
        )
        conn.commit()
        success = True

    except sqlite3.IntegrityError:
        success = False

    conn.close()
    return success


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


# -------------------------------
# PREDICTION HISTORY QUERIES
# -------------------------------

def save_prediction(
    username,
    store,
    medicine,
    item_id,
    category,
    price,
    promotion,
    holiday,
    forecast_date,
    day_of_week,
    month,
    is_weekend,
    predicted_units,
    demand_level
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            username, store, medicine, item_id, category, price,
            promotion, holiday, forecast_date, day_of_week, month,
            is_weekend, predicted_units, demand_level, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username, store, medicine, item_id, category, price,
            int(promotion), int(holiday), forecast_date, day_of_week, month,
            int(is_weekend), predicted_units, demand_level,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_predictions(username=None):
    conn = get_connection()

    if username:
        query = "SELECT * FROM predictions WHERE username = ? ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn, params=(username,))
    else:
        query = "SELECT * FROM predictions ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df


def delete_prediction(prediction_id, username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM predictions WHERE id = ? AND username = ?",
        (prediction_id, username)
    )

    conn.commit()
    conn.close()
