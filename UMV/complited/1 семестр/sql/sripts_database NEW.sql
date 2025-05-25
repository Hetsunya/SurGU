PRAGMA foreign_keys = ON;

-- Автоматическое управление портфелем:
   -- Задача: Показать портфель и уведомить, если доля одного инструмента > 50%.
WITH Portfolio AS (
    SELECT 
        ia.account_id,
        i.instrument_id,
        i.name,
        i.category,
        i.current_price,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS total_value
    FROM InvestmentAccount ia
    JOIN TransactionTable tr ON ia.account_id = tr.account_id
    JOIN Instrument i ON tr.instrument_id = i.instrument_id
    GROUP BY ia.account_id, i.instrument_id, i.name, i.category, i.current_price
    HAVING balance > 0
),
AccountTotal AS (
    SELECT account_id, SUM(total_value) AS account_value
    FROM Portfolio
    GROUP BY account_id
)
SELECT 
    p.account_id,
    p.instrument_id,
    p.name,
    p.category,
    p.balance,
    p.total_value,
    (p.total_value / at.account_value * 100) AS percentage,
    CASE WHEN (p.total_value / at.account_value * 100) > 50 THEN 'Warning: Instrument share exceeds 50%' ELSE '' END AS notification
FROM Portfolio p
JOIN AccountTotal at ON p.account_id = at.account_id
ORDER BY p.account_id, p.total_value DESC;

-- Автоматизированная оценка финансового положения:
    --Задача: Баланс счёта (выплаты минус налоги) и текущая стоимость портфеля.
WITH Portfolio AS (
    SELECT 
        ia.account_id,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS portfolio_value
    FROM InvestmentAccount ia
    LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
    LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
    GROUP BY ia.account_id
    HAVING SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) > 0
)
SELECT 
    ia.account_id,
    c.full_name,
    COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0) AS account_balance,
    COALESCE(pf.portfolio_value, 0) AS portfolio_value,
    (COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0) + COALESCE(pf.portfolio_value, 0)) AS total_wealth
FROM InvestmentAccount ia
JOIN Client c ON ia.client_id = c.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
LEFT JOIN Portfolio pf ON ia.account_id = pf.account_id
GROUP BY ia.account_id, c.full_name, pf.portfolio_value;

-- 3. Автоматизированное управление клиентскими профилями:

    --Задача: Профиль клиента (данные, счета, история операций, выплаты).
SELECT 
    c.client_id,
    c.full_name,
    c.tax_status,
    c.email,
    c.phone,
    c.registration_date,
    COUNT(DISTINCT ia.account_id) AS account_count,
    COALESCE(SUM(p.amount), 0) AS total_payout,
    COUNT(DISTINCT tr.transaction_id) AS transaction_count
FROM Client c
LEFT JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
GROUP BY c.client_id, c.full_name, c.tax_status, c.email, c.phone, c.registration_date;

-- Поддержание коммуникации с клиентами:

   -- Задача: Уведомления о состоянии портфеля и ожидаемых выплатах.
SELECT 
    c.client_id,
    c.full_name,
    CASE 
        WHEN i.expected_payout_date <= date('now', '+7 days') THEN 'Expected payout for ' || i.name || ' on ' || i.expected_payout_date
        WHEN (SELECT SUM(CASE WHEN tr2.type = 'Buy' THEN tr2.quantity ELSE -tr2.quantity END) * i.current_price /
                 SUM(CASE WHEN tr2.type = 'Buy' THEN tr2.quantity ELSE -tr2.quantity END) * i.current_price * 100 > 50
                 FROM TransactionTable tr2 WHERE tr2.account_id = ia.account_id GROUP BY tr2.instrument_id) THEN
                 'Warning: Instrument ' || i.name || ' exceeds 50% of portfolio'
        ELSE 'No notifications'
    END AS notification
FROM Client c
JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
WHERE i.expected_payout_date <= date('now', '+7 days')
   OR (SELECT SUM(CASE WHEN tr2.type = 'Buy' THEN tr2.quantity ELSE -tr2.quantity END) * i.current_price /
          SUM(CASE WHEN tr2.type = 'Buy' THEN tr2.quantity ELSE -tr2.quantity END) * i.current_price * 100 > 50
          FROM TransactionTable tr2 WHERE tr2.account_id = ia.account_id GROUP BY tr2.instrument_id)
GROUP BY c.client_id, c.full_name, i.name, i.expected_payout_date;
