-- SQLite schema for Loto6 collector

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS draws (
  draw_no INTEGER PRIMARY KEY,
  draw_date TEXT NOT NULL,
  number1 INTEGER NOT NULL,
  number2 INTEGER NOT NULL,
  number3 INTEGER NOT NULL,
  number4 INTEGER NOT NULL,
  number5 INTEGER NOT NULL,
  number6 INTEGER NOT NULL,
  bonus INTEGER NOT NULL,
  source TEXT NOT NULL,
  source_url TEXT,
  retrieved_at TEXT NOT NULL,
  checksum TEXT NOT NULL,
  verified INTEGER NOT NULL DEFAULT 0,
  verification_source TEXT,
  verification_at TEXT,
  conflict_reason TEXT
);

CREATE TABLE IF NOT EXISTS raw_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_no INTEGER,
  source TEXT NOT NULL,
  path_or_url TEXT NOT NULL,
  checksum TEXT NOT NULL,
  stored_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT NOT NULL,
  draw_no INTEGER,
  message TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conflicts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_no INTEGER NOT NULL,
  primary_payload TEXT NOT NULL,
  secondary_payload TEXT,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL,
  resolved INTEGER NOT NULL DEFAULT 0
);
