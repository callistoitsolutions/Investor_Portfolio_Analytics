TRUNCATE TABLE portfolio_investments;
TRUNCATE TABLE investors;

-- Insert investors (dedupe by client_id)
INSERT IGNORE INTO investors (client_id, client_name, age, gender, city, state)
SELECT DISTINCT ClientID, ClientName, Age, Gender, City, State
FROM raw_excel_data;  -- Use LOAD DATA or Python pandas.to_sql

-- Insert investments
INSERT INTO portfolio_investments (client_id, asset_type, investment_amount, annual_return_amount, investment_start_date, investment_end_date)
SELECT ClientID, AssetType, InvestmentAmountINR, AnnualReturnINR, InvestmentStartDate, InvestmentEndDate
FROM raw_excel_data;
