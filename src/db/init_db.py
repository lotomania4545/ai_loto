#!/usr/bin/env python3
"""
Initialize SQLite DB using schema.sql.

Usage:
  python src/db/init_db.py
  python src/db/init_db.py data/test.db
"""
import os
import sys
import argparse
import sqlite3


def init_db(db_path: str = "data/loto6.db"):
    # Ensure directory exists
    dirpath = os.path.dirname(os.path.abspath(db_path))
    if dirpath and not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath, exist_ok=True)
        except Exception as e:
            print(f"ERROR: Unable to create directory '{dirpath}': {e}", file=sys.stderr)
            sys.exit(1)

    # Locate schema.sql relative to this file
    here = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(here, "schema.sql")
    if not os.path.exists(schema_path):
        print(f"ERROR: schema.sql not found at expected path: {schema_path}", file=sys.stderr)
        sys.exit(1)

    # Read schema
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
    except Exception as e:
        print(f"ERROR: Failed to read schema.sql: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize DB (will create file if not exists). Do not destroy existing DB.
    try:
        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"ERROR: SQLite error while initializing DB '{db_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error while initializing DB '{db_path}': {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            conn.close()
        except Exception:
            pass

    print(f"Initialized database at: {db_path}")
    return db_path


def parse_args():
    p = argparse.ArgumentParser(description="Initialize Loto6 SQLite DB from schema.sql")
    p.add_argument("db_path", nargs="?", default="data/loto6.db", help="Path to sqlite DB file (default: data/loto6.db)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    init_db(args.db_path)
