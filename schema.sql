CREATE TABLE Manager (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_name VARCHAR(255) NOT NULL
);

CREATE TABLE InvestmentFund (
    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    manager_id INTEGER NOT NULL,
    description VARCHAR(255) NOT NULL,
    nav FLOAT NOT NULL,
    date_of_creation VARCHAR(20) DEFAULT (strftime('%Y-%m-%d', 'now')),
    performance FLOAT NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
);