#!/usr/bin/env python3
"""
Database initialization script.
This script creates the database and all tables from schema.sql
"""

import sqlite3
import os

DATABASE = 'database.db'
SCHEMA_FILE = 'schema.sql'

def init_database():
    """Initialize the database with schema"""
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        response = input(f"Database '{DATABASE}' already exists. Delete and recreate? (y/n): ")
        if response.lower() == 'y':
            os.remove(DATABASE)
            print(f"Deleted existing database '{DATABASE}'")
        else:
            print("Keeping existing database.")
            return
    
    # Create database and execute schema
    print(f"Creating database '{DATABASE}'...")
    conn = sqlite3.connect(DATABASE)
    
    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()
        conn.executescript(schema)
    
    conn.close()
    print(f"Database '{DATABASE}' initialized successfully!")
    print("\nTables created:")
    print("  - User")
    print("  - Post")
    print("  - Like")
    print("  - Comment")
    print("  - Events")
    print("  - Resources")
    print("  - Message")

if __name__ == '__main__':
    if not os.path.exists(SCHEMA_FILE):
        print(f"Error: Schema file '{SCHEMA_FILE}' not found!")
        exit(1)
    
    init_database()


