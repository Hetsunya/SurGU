-- Создание таблиц
-- Описание: Инициализация структуры базы данных с таблицами и ограничениями
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tax_status TEXT NOT NULL CHECK(tax_status IN ('Resident', 'NonResident')),
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    registration_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS InvestmentAccount (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    account_type TEXT NOT NULL CHECK(account_type IN ('Brokerage', 'IIS', 'Trust')),
    open_date DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Instrument (
    instrument_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Stock', 'Bond', 'ETF')),
    expected_payout_per_unit DECIMAL(10,2),
    current_price DECIMAL(10,2) NOT NULL,
    expected_payout_date DATE,
    UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS TransactionTable (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    instrument_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Buy', 'Sell')),
    quantity DECIMAL(10,2) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL,
    commission DECIMAL(10,2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    FOREIGN KEY (account_id) REFERENCES InvestmentAccount(account_id) ON DELETE CASCADE,
    FOREIGN KEY (instrument_id) REFERENCES Instrument(instrument_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Payout (
    payout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Profit', 'Dividends')),
    amount DECIMAL(10,2) NOT NULL,
    payout_date DATETIME NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES TransactionTable(transaction_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TaxObligation (
    tax_obligation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payout_id INTEGER NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    calculation_basis TEXT NOT NULL,
    FOREIGN KEY (payout_id) REFERENCES Payout(payout_id) ON DELETE CASCADE
);

-- CRUD для Client
-- Описание: Операции добавления, получения, обновления и удаления клиентов

-- Получение клиента по client_id
-- Использование: Укажите :client_id для конкретного человека
SELECT client_id, tax_status, full_name, email, phone, registration_date
FROM Client
WHERE client_id = :client_id;

-- Добавление клиента
-- Использование: Без изменений, подставьте параметры
INSERT INTO Client (tax_status, full_name, email, phone, registration_date)
VALUES (:tax_status, :full_name, :email, :phone, :registration_date);

-- Обновление клиента
-- Использование: Без изменений, подставьте :client_id и параметры
UPDATE Client
SET tax_status = :tax_status, 
    full_name = :full_name, 
    email = :email, 
    phone = :phone, 
    registration_date = :registration_date
WHERE client_id = :client_id;

-- Удаление клиента
-- Использование: Без изменений, подставьте :client_id
DELETE FROM Client WHERE client_id = :client_id;

-- CRUD для InvestmentAccount
-- Описание: Операции добавления, получения и удаления счетов

-- Получение счетов по client_id или account_id
-- Использование: Укажите :client_id или :account_id (или оба)
SELECT account_id, client_id, account_type, open_date
FROM InvestmentAccount
WHERE (:client_id IS NULL OR client_id = :client_id)
  AND (:account_id IS NULL OR account_id = :account_id);

-- Добавление счёта
-- Использование: Без изменений, подставьте параметры, включая :client_id
INSERT INTO InvestmentAccount (client_id, account_type, open_date)
VALUES (:client_id, :account_type, :open_date);

-- Удаление счёта
-- Использование: Без изменений, подставьте :account_id
DELETE FROM InvestmentAccount WHERE account_id = :account_id;

-- CRUD для Instrument
-- Описание: Операции добавления, получения, обновления и удаления инструментов

-- Получение всех инструментов
-- Использование: Без изменений, фильтрация по client_id или account_id не требуется
SELECT instrument_id, name, category, expected_payout_per_unit, current_price, expected_payout_date
FROM Instrument;

-- Обновление инструмента
-- Использование: Без изменений, подставьте :instrument_id и параметры
UPDATE Instrument
SET name = :name, 
    category = :category, 
    expected_payout_per_unit = :expected_payout_per_unit, 
    current_price = :current_price, 
    expected_payout_date = :expected_payout_date
WHERE instrument_id = :instrument_id;

-- Удаление инструмента
-- Использование: Без изменений, подставьте :instrument_id
DELETE FROM Instrument WHERE instrument_id = :instrument_id;

-- CRUD для TransactionTable
-- Описание: Операции добавления, получения и удаления транзакций

-- Получение транзакций по client_id или account_id
-- Использование: Укажите :client_id или :account_id (или оба)
SELECT t.transaction_id, t.account_id, t.instrument_id, t.type, t.quantity, t.price_per_unit, t.commission, t.transaction_date
FROM TransactionTable t
JOIN InvestmentAccount ia ON t.account_id = ia.account_id
WHERE (:client_id IS NULL OR ia.client_id = :client_id)
  AND (:account_id IS NULL OR t.account_id = :account_id);

-- Добавление транзакции
-- Использование: Без изменений, подставьте :account_id и параметры
INSERT INTO TransactionTable (account_id, instrument_id, type, quantity, price_per_unit, commission, transaction_date)
VALUES (:account_id, :instrument_id, :type, :quantity, :price_per_unit, :commission, :transaction_date)
RETURNING transaction_id;

-- Удаление транзакции
-- Использование: Без изменений, подставьте :transaction_id
DELETE FROM TransactionTable WHERE transaction_id = :transaction_id;

-- Получение tax_status клиента
-- Описание: Получение налогового статуса клиента по account_id
-- Использование: Без изменений, подставьте :account_id
SELECT c.tax_status
FROM Client c
JOIN InvestmentAccount ia ON c.client_id = ia.client_id
WHERE ia.account_id = :account_id;

-- Расчёт средней цены покупки
-- Описание: Расчёт средней цены покупки инструмента на счёте
-- Использование: Без изменений, подставьте :account_id и :instrument_id
SELECT COALESCE(SUM(quantity * price_per_unit) / SUM(quantity), 0) AS average_price
FROM TransactionTable
WHERE account_id = :account_id 
  AND instrument_id = :instrument_id 
  AND type = 'Buy';

-- Расчёт дивидендов
-- Описание: Создание выплат дивидендов и налоговых обязательств
-- Использование: Для client_id добавьте фильтр в WHERE (ia.client_id = :client_id), для account_id добавьте (ia.account_id = :account_id)
-- Шаг 1: Создание выплат
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
  AND (:client_id IS NULL OR ia.client_id = :client_id)
  AND (:account_id IS NULL OR ia.account_id = :account_id)
GROUP BY ia.account_id, i.instrument_id, i.name, i.expected_payout_per_unit, i.expected_payout_date, tr.transaction_id
HAVING SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) > 0
RETURNING payout_id, transaction_id, amount, payout_date;

-- Шаг 2: Создание налоговых обязательств
-- Использование: Без изменений, так как работает с новыми выплатами
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
-- Описание: Получение выплат с фильтрацией по client_id или account_id
-- Использование: Укажите :client_id или :account_id
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
JOIN Instrument i ON tr.instrument_id = i.instrument_id
WHERE (:client_id IS NULL OR ia.client_id = :client_id)
  AND (:account_id IS NULL OR ia.account_id = :account_id);

-- Получение выплат с налогами
-- Описание: Получение выплат с налогами для главного экрана
-- Использование: Укажите :client_id или :account_id
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
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
WHERE (:client_id IS NULL OR ia.client_id = :client_id)
  AND (:account_id IS NULL OR ia.account_id = :account_id);

-- Получение баланса счёта
-- Описание: Расчёт баланса счёта (выплаты минус налоги)
-- Использование: Без изменений, подставьте :account_id
SELECT 
    COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0) AS account_balance
FROM InvestmentAccount ia
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
WHERE ia.account_id = :account_id;

-- Получение портфеля счёта
-- Описание: Получение списка инструментов с балансом для счёта
-- Использование: Без изменений, подставьте :account_id
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
-- Описание: Получение информации об инструментах счёта
-- Использование: Без изменений, подставьте :account_id
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
-- Описание: Получение отчёта о портфеле с процентами и уведомлениями
-- Использование: Укажите :client_id или :account_id
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
    WHERE (:client_id IS NULL OR ia.client_id = :client_id)
      AND (:account_id IS NULL OR ia.account_id = :account_id)
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

-- Отчёт: Финансовое положение
-- Описание: Получение финансового положения
-- Использование: Укажите :client_id или :account_id
WITH Portfolio AS (
    SELECT 
        ia.account_id,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS portfolio_value
    FROM InvestmentAccount ia
    LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
    LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
    WHERE (:client_id IS NULL OR ia.client_id = :client_id)
      AND (:account_id IS NULL OR ia.account_id = :account_id)
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
WHERE (:client_id IS NULL OR ia.client_id = :client_id)
  AND (:account_id IS NULL OR ia.account_id = :account_id)
GROUP BY ia.account_id, c.full_name, pf.portfolio_value;

-- Отчёт: Профиль клиента
-- Описание: Получение профиля клиента
-- Использование: Укажите :client_id
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
WHERE c.client_id = :client_id
GROUP BY c.client_id, c.full_name, c.tax_status, c.email, c.phone, c.registration_date;

-- Уведомления
-- Описание: Получение уведомлений о выплатах и доле >50%
-- Использование: Укажите :client_id
WITH Portfolio AS (
    SELECT 
        ia.account_id,
        i.instrument_id,
        i.name,
        i.current_price,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance,
        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS total_value
    FROM InvestmentAccount ia
    JOIN TransactionTable tr ON ia.account_id = tr.account_id
    JOIN Instrument i ON tr.instrument_id = i.instrument_id
    WHERE (:client_id IS NULL OR ia.client_id = :client_id)
    GROUP BY ia.account_id, i.instrument_id, i.name, i.current_price
    HAVING balance > 0
),
AccountTotal AS (
    SELECT account_id, COALESCE(SUM(total_value), 0) AS account_value
    FROM Portfolio
    GROUP BY account_id
)
SELECT DISTINCT
    c.client_id,
    c.full_name,
    CASE 
        WHEN i.expected_payout_date IS NOT NULL AND i.expected_payout_date <= date('now', '+7 days') 
        THEN 'Ожидаемая выплата по ' || i.name || ' ' || i.expected_payout_date
        WHEN at.account_value > 0 AND p.total_value / at.account_value * 100 > 50 
        THEN 'Внимание: Доля инструмента ' || p.name || ' превышает 50% портфеля'
        ELSE ''
    END AS notification
FROM Client c
JOIN InvestmentAccount ia ON c.client_id = ia.client_id
LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
LEFT JOIN Portfolio p ON ia.account_id = p.account_id AND i.instrument_id = p.instrument_id
LEFT JOIN AccountTotal at ON ia.account_id = at.account_id
WHERE c.client_id = :client_id
  AND ((i.expected_payout_date IS NOT NULL AND i.expected_payout_date <= date('now', '+7 days'))
   OR (at.account_value > 0 AND p.total_value / at.account_value * 100 > 50))
   AND notification != '';