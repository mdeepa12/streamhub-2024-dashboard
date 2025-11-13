
-- StreamHub SQL Schema + Analytics Queries (Portfolio Version)
-- Author: Deepa Mallipeddi

-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date DATE,
    plan_type TEXT,
    region TEXT
);

-- EVENTS TABLE
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    user_id INT,
    event_timestamp TIMESTAMP,
    event_name TEXT
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    txn_id SERIAL PRIMARY KEY,
    user_id INT,
    amount_usd NUMERIC(10,2),
    txn_timestamp TIMESTAMP
);

-- RETENTION & ARPU QUERIES are same as used for generating CSVs
