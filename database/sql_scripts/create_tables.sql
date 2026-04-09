CREATE DATABASE IF NOT EXISTS investorportfolioanalytics;
USE investorportfolioanalytics;

CREATE TABLE investors (
    client_id VARCHAR(20) PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    city VARCHAR(50),
    state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE portfolio_investments (
    investment_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id VARCHAR(20),
    asset_type VARCHAR(50),
    investment_amount DECIMAL(12,2),
    annual_return_amount DECIMAL(12,2),
    investment_start_date DATE,
    investment_end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES investors(client_id)
);

CREATE TABLE asset_master (
    asset_type VARCHAR(50) PRIMARY KEY,
    risk_category VARCHAR(20)
);

INSERT INTO asset_master (asset_type, risk_category) VALUES
('Equity', 'High'), ('Mutual Fund', 'Medium'), ('Debt Fund', 'Low'),
('Gold', 'Medium'), ('Fixed Deposit', 'Low'), ('ETF', 'Medium');
