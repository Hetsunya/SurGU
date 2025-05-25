-- Расчёт дивидендов
-- Описание: Создание выплат дивидендов и налоговых обязательств для инструментов с expected_payout_date <= текущей даты
-- Шаг 1: Создание выплат и налоговых обязательств
INSERT INTO Payout (transaction_id, type, amount, payout_date)
SELECT 
    tr.transaction_id,
    'Dividends' AS type,
    SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.expected_payout_per_unit AS amount,
    i.expected_payout_date AS payout_date
FROM Instrument i
JOIN TransactionTable tr ON i.instrument_id = tr.instrument_id
JOIN InvestmentAccount ia ON tr.account_id = ia.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id 
    AND p.type = 'Dividends' 
    AND p.payout_date = i.expected_payout_date
WHERE i.expected_payout_per_unit IS NOT NULL 
  AND i.expected_payout_per_unit > 0
  AND i.expected_payout_date IS NOT NULL 
  AND i.expected_payout_date <= '2025-05-09'
  AND p.payout_id IS NULL
GROUP BY ia.account_id, i.instrument_id, i.name, i.expected_payout_per_unit, i.expected_payout_date, tr.transaction_id
HAVING SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) > 0
RETURNING payout_id, transaction_id, amount, payout_date;

-- Шаг 2: Создание налоговых обязательств для новых выплат
INSERT INTO TaxObligation (payout_id, amount, due_date, calculation_basis)
SELECT 
    p.payout_id,
    p.amount * (CASE WHEN c.tax_status = 'Resident' THEN 0.13 ELSE 0.30 END) AS tax_amount,
    date(p.payout_date, '+30 days') AS due_date,
    'НДФЛ ' || (CASE WHEN c.tax_status = 'Resident' THEN '13' ELSE '30' END) || '% на дивиденды (' || i.name || ')' AS calculation_basis
FROM Payout p
JOIN TransactionTable tr ON p.transaction_id = tr.transaction_id
JOIN InvestmentAccount ia ON tr.account_id = ia.account_id
JOIN Client c ON ia.client_id = c.client_id
JOIN Instrument i ON tr.instrument_id = i.instrument_id
WHERE p.type = 'Dividends'
  AND p.payout_date = i.expected_payout_date
  AND NOT EXISTS (
      SELECT 1 
      FROM TaxObligation t 
      WHERE t.payout_id = p.payout_id
  );

-- Получение списка выплат
-- Описание: Получение всех выплат с информацией о счёте и инструменте
SELECT 
    p.payout_id, 
    p.transaction_id, 
    ia.account_id, 
    i.name AS instrument_name, 
    p.type, 
    p.amount, 
    p.payout_date
FROM Payout p
JOIN TransactionTable tr ON p.transaction_id = tr.transaction_id
JOIN InvestmentAccount ia ON tr.account_id = ia.account_id
JOIN Instrument i ON tr.instrument_id = i.instrument_id;

-- Получение выплат с налогами для главного экрана
-- Описание: Получение выплат с информацией о налогах
SELECT 
    p.payout_id,
    p.transaction_id,
    ia.account_id,
    i.name AS instrument_name,
    p.type,
    p.amount,
    p.payout_date,
    COALESCE(t.amount, 0) AS tax_amount,
    COALESCE(t.due_date, '') AS tax_due_date,
    COALESCE(t.calculation_basis, '') AS tax_calculation_basis
FROM Payout p
JOIN TransactionTable tr ON p.transaction_id = tr.transaction_id
JOIN InvestmentAccount ia ON tr.account_id = ia.account_id
JOIN Instrument i ON tr.instrument_id = i.instrument_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id;

-- Получение баланса счёта
-- Описание: Расчёт баланса счёта (выплаты минус налоги)
SELECT 
    COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0) AS account_balance
FROM InvestmentAccount ia
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
WHERE ia.account_id = :account_id;

-- Получение портфеля счёта
-- Описание: Получение списка инструментов с балансом для счёта
SELECT 
    i.instrument_id, 
    i.name, 
    i.category, 
    i.expected_payout_per_unit, 
    i.current_price, 
    i.expected_payout_date,
    COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) AS balance
FROM Instrument i
LEFT JOIN TransactionTable tr ON i.instrument_id = tr.instrument_id AND tr.account_id = :account_id
GROUP BY i.instrument_id, i.name, i.category, i.expected_payout_per_unit, i.current_price, i.expected_payout_date
HAVING balance > 0;

-- Отчёт: Инструменты счёта
-- Описание: Получение информации об инструментах счёта с общей стоимостью портфеля
WITH AccountInstruments AS (
    SELECT 
        c.full_name,
        i.name AS instrument_name,
        i.category,
        COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) AS balance,
        i.current_price,
        COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) * i.current_price AS total_value
    FROM InvestmentAccount ia
    JOIN Client c ON ia.client_id = c.client_id
    JOIN TransactionTable tr ON ia.account_id = tr.account_id
    JOIN Instrument i ON tr.instrument_id = i.instrument_id
    WHERE ia.account_id = :account_id
    GROUP BY i.instrument_id, c.full_name, i.name, i.category, i.current_price
    HAVING balance > 0
)
SELECT 
    full_name,
    instrument_name,
    category,
    balance,
    current_price,
    total_value,
    (SELECT SUM(total_value) FROM AccountInstruments) AS portfolio_value
FROM AccountInstruments;

-- Отчёт: Портфель
-- Описание: Получение отчёта о портфеле с процентами и уведомлениями о доле >50%
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
    SELECT account_id, COALESCE(SUM(total_value), 0) AS account_value
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
    COALESCE(CASE WHEN at.account_value > 0 THEN ROUND(p.total_value / at.account_value * 100, 2) ELSE 0 END, 0) AS percentage,
    CASE WHEN at.account_value > 0 AND p.total_value / at.account_value * 100 > 50 
         THEN 'Warning: Instrument share exceeds 50% in portfolio'
         ELSE '' 
    END AS notification
FROM Portfolio p
LEFT JOIN AccountTotal at ON p.account_id = at.account_id
WHERE p.balance > 0
ORDER BY p.account_id, p.total_value DESC;

-- Отчёт: Финансовое положение
-- Описание: Получение финансового положения (баланс, портфель, общее богатство)
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

-- Отчёт: Профиль клиента
-- Описание: Получение профиля клиента (информация, количество счетов, выплат, транзакций)
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

-- Уведомления
-- Описание: Получение уведомлений о предстоящих выплатах (за 7 дней) и доле инструмента >50%
WITH RawPortfolio AS (
    SELECT 
        ia.account_id,
        i.instrument_id,
        i.name,
        i.category,
        i.current_price,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance
    FROM InvestmentAccount ia
    JOIN TransactionTable tr ON ia.account_id = tr.account_id
    JOIN Instrument i ON tr.instrument_id = i.instrument_id
    GROUP BY ia.account_id, i.instrument_id, i.name, i.category, i.current_price
),
FilteredPortfolio AS (
    SELECT 
        account_id,
        instrument_id,
        name,
        category,
        current_price,
        balance,
        CAST(balance AS REAL) * current_price AS total_value
    FROM RawPortfolio
    WHERE balance > 0
),
AccountTotal AS (
    SELECT account_id, SUM(total_value) AS account_value
    FROM FilteredPortfolio
    GROUP BY account_id
)
SELECT 
    p.account_id,
    p.instrument_id,
    p.name,
    p.category,
    p.balance,
    p.total_value,
    at.account_value,
    ROUND(CASE WHEN at.account_value > 0 THEN p.total_value * 100.0 / at.account_value ELSE 0 END, 2) AS percentage,
    CASE 
        WHEN at.account_value > 0 AND p.total_value * 100.0 / at.account_value > 50 
        THEN 'Warning: Instrument share exceeds 50% in portfolio'
        ELSE '' 
    END AS notification
FROM FilteredPortfolio p
JOIN AccountTotal at ON p.account_id = at.account_id
ORDER BY p.account_id, p.total_value DESC;
