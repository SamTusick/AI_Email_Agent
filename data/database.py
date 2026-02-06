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
    print("Getting user with email:", email, "........")

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

def create_user(email,name):
    print("Creating user for:", name, " with email:", email, "........")
    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(""" INSERT  into users (email,name) 
                        VALUES (?,?)
                    """, (email, name))
        
        conn.commit()
        return cur.lastrowid

    except sqlite3.IntegrityError:
        print("Databse error:", email, "already exists")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_user(email, name = None, email_count = None, avg_urgency = None, common_email_type = None, common_email_topic = None, role = None):
    print("Updating user with email:", email, "........")
    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(""" UPDATE users
                        SET name = COALESCE(?, name),
                            email_count = COALESCE(?, email_count),
                            avg_urgency = COALESCE(?, avg_urgency),
                            common_email_type = COALESCE(?, common_email_type),
                            common_email_topic = COALESCE(?, common_email_topic),
                            role = COALESCE(?, role)
                        WHERE email = ?
                    """, (name, email_count, avg_urgency, common_email_type, common_email_topic, role, email))
        
        conn.commit()
        return cur.rowcount > 0
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def insert_email(id, sender_email, subject, body, email_type=None, 
                 urgency=None, sentiment=None, intent=None, 
                 actions_done=None, processed=False):
    
    print("Inserting email from", sender_email, "into database.............." )   

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(""" INSERT INTO emails
                    (id, sender_email, subject, body, email_type, urgency, sentiment, intent, actions_done, processed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id, sender_email, subject, body, email_type, urgency,
                        sentiment, intent, actions_done, processed))

        conn.commit()

        print("Email inserted successfully")
        return id

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

# USE ONLY FOR TESTING
def clear_database():
    """Clear all data but keep tables (for testing)"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Delete all data
        cur.execute("DELETE FROM emails")
        cur.execute("DELETE FROM users")
        
        conn.commit()
        print("Database cleared (tables kept)")
        
    except sqlite3.Error as e:
        print(f"Error clearing database: {e}")
    finally:
        if conn:
            conn.close()   

if __name__ == "__main__":
    init_database()