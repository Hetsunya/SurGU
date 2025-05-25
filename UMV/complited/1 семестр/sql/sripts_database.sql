PRAGMA foreign_keys = ON;

-- 1. Баланс счёта (сумма выплат минус налоги для каждого счёта)
SELECT 
    ia.account_id,
    ia.account_type,
    c.full_name,
    COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0) AS balance
FROM InvestmentAccount ia
JOIN Client c ON ia.client_id = c.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
GROUP BY ia.account_id, ia.account_type, c.full_name;

-- 2. Портфель (текущие активы по счетам)
SELECT 
    ia.account_id,
    ia.account_type,
    i.name AS instrument_name,
    i.category,
    SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance
FROM InvestmentAccount ia
JOIN TransactionTable tr ON ia.account_id = tr.account_id
JOIN Instrument i ON tr.instrument_id = i.instrument_id
GROUP BY ia.account_id, ia.account_type, i.instrument_id, i.name, i.category
HAVING balance > 0;

-- 3. Доходы клиента (сумма выплат по типам)
SELECT 
    c.client_id,
    c.full_name,
    p.type,
    COALESCE(SUM(p.amount), 0) AS total_payout
FROM Client c
LEFT JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
GROUP BY c.client_id, c.full_name, p.type;

-- 4. Налоговые обязательства клиента
SELECT 
    c.client_id,
    c.full_name,
    t.calculation_basis,
    COALESCE(SUM(t.amount), 0) AS total_tax,
    MIN(t.due_date) AS earliest_due_date
FROM Client c
LEFT JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
GROUP BY c.client_id, c.full_name, t.calculation_basis
HAVING total_tax > 0;

-- 5. Активные клиенты (с ненулевым портфелем или выплатами)
SELECT DISTINCT
    c.client_id,
    c.full_name,
    c.tax_status
FROM Client c
JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
WHERE EXISTS (
    SELECT 1
    FROM TransactionTable tr2
    WHERE tr2.account_id = ia.account_id
    GROUP BY tr2.account_id, tr2.instrument_id
    HAVING SUM(CASE WHEN tr2.type = 'Buy' THEN tr2.quantity ELSE -tr2.quantity END) > 0
) OR p.amount > 0;