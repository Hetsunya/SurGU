PRAGMA foreign_keys = ON;

-- Удаление таблиц в правильном порядке (с учётом зависимостей)
DROP TABLE IF EXISTS TaxObligation;
DROP TABLE IF EXISTS Payout;
DROP TABLE IF EXISTS TransactionTable;
DROP TABLE IF EXISTS Instrument;
DROP TABLE IF EXISTS InvestmentAccount;
DROP TABLE IF EXISTS Client;

-- Client (Клиент)
CREATE TABLE Client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tax_status TEXT NOT NULL CHECK(tax_status IN ('Resident', 'NonResident')),
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    registration_date DATE NOT NULL
);

-- InvestmentAccount (Инвестиционный счёт)
CREATE TABLE InvestmentAccount (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    account_type TEXT NOT NULL CHECK(account_type IN ('Brokerage', 'IIS', 'Trust')),
    open_date DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

-- Instrument (Финансовый инструмент)
CREATE TABLE Instrument (
    instrument_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Stock', 'Bond', 'ETF')),
    expected_payout_per_unit DECIMAL(10,2),
    current_price DECIMAL(10,2) NOT NULL,
    expected_payout_date DATE,
    UNIQUE(name)
);

-- TransactionTable (Транзакция)
CREATE TABLE TransactionTable (
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

-- Payout (Выплата)
CREATE TABLE Payout (
    payout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Profit', 'Dividends')),
    amount DECIMAL(10,2) NOT NULL,
    payout_date DATETIME NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES TransactionTable(transaction_id) ON DELETE CASCADE
);

-- TaxObligation (Налоговое обязательство)
CREATE TABLE TaxObligation (
    tax_obligation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payout_id INTEGER NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    calculation_basis TEXT NOT NULL,
    FOREIGN KEY (payout_id) REFERENCES Payout(payout_id) ON DELETE CASCADE
);
