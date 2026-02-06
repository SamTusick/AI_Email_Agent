# database.py
# Initialize database schema

import sqlite3
from datetime import datetime

DB_PATH = 'agent_memory.db'

def init_database():
    # Create Tables if they dont exist

    conn = sqlite3.connect(DB_PATH) # Connect to Database
    cur = conn.cursor() # Set up DB cursor to be able to fetch and execute sql

    # USERS TABLE
    cur.execute("""CREATE TABLE IF NOT EXISTS users 
                        (
                            email TEXT PRIMARY KEY,
                            name TEXT,
                            email_count INTEGER DEFAULT 0,
                            avg_urgency REAL DEFAULT 0.5,
                            common_email_type TEXT,
                            common_email_topic TEXT,
                            role TEXT
                        )   
                """)
    
    # EMAILS TABLE
    cur.execute("""CREATE TABLE IF NOT EXISTS emails 
                        (
                            id TEXT PRIMARY KEY,
                            sender_email TEXT,
                            subject TEXT,
                            body TEXT,
                            type TEXT,
                            urgency REAL,
                            sentiment TEXT,
                            intent TEXT,
                            actions_done TEXT,
                            processed BOOLEAN DEFAULT 0,
                            FOREIGN KEY (sender_email) REFERENCES users(email) 
                        ) 
                """)
 
    conn.commit()
    conn.close()
    print("Database Initialized")

def get_user(email):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Returns dict-like rows
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * 
            FROM users
            WHERE email = ?
        """, (email,))
        
        user = cur.fetchone()
        return dict(user) if user else None  # Return as dict or None
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()