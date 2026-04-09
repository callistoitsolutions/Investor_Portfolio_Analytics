CREATE VIEW vw_portfolio_analysis AS
SELECT 
    i.client_id, i.client_name, i.city, i.state, i.age,
    p.asset_type, am.risk_category,
    p.investment_amount, p.annual_return_amount,
    p.investment_start_date, p.investment_end_date,
    DATEDIFF(p.investment_end_date, p.investment_start_date) / 365 AS years_invested
FROM investors i
JOIN portfolio_investments p ON i.client_id = p.client_id
JOIN asset_master am ON p.asset_type = am.asset_type;
