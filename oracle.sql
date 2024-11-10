-- ORACLE SQL
CREATE TABLE transactions (
    id NUMBER PRIMARY KEY,
    date_time TIMESTAMP,
    amount NUMBER(10,2),
    category VARCHAR2(50),
    description VARCHAR2(200),
    type VARCHAR2(20),
    CONSTRAINT type_check CHECK (type IN ('INCOME', 'EXPENSE'))
);

CREATE TABLE categories (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50),
    type VARCHAR2(20)
);

CREATE SEQUENCE trans_seq START WITH 1;

CREATE OR REPLACE PROCEDURE add_transaction(
    p_amount IN NUMBER,
    p_category IN VARCHAR2,
    p_description IN VARCHAR2,
    p_type IN VARCHAR2
) AS
BEGIN
    INSERT INTO transactions (id, date_time, amount, category, description, type)
    VALUES (trans_seq.NEXTVAL, SYSTIMESTAMP, p_amount, p_category, p_description, p_type);
    COMMIT;
END;