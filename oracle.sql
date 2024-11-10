CREATE TABLE users (
    id NUMBER PRIMARY KEY,
    username VARCHAR2(50) UNIQUE,
    password_hash VARCHAR2(256),
    email VARCHAR2(100),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE accounts (
    id NUMBER PRIMARY KEY,
    user_id NUMBER,
    bank_name VARCHAR2(50),
    account_number VARCHAR2(50),
    balance NUMBER(15,2),
    last_synced TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE goals (
    id NUMBER PRIMARY KEY,
    user_id NUMBER,
    name VARCHAR2(100),
    target_amount NUMBER(15,2),
    current_amount NUMBER(15,2),
    deadline DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE achievements (
    id NUMBER PRIMARY KEY,
    user_id NUMBER,
    badge_name VARCHAR2(50),
    points NUMBER,
    earned_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);