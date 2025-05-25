using System;
using System.Collections.Generic;
using System.Data.SQLite;

namespace InvestmentApp
{
    public class DatabaseService
    {
        private readonly string connectionString = "Data Source=investments.db;Version=3;";

        public DatabaseService()
        {
            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
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
                );";
            command.ExecuteNonQuery();
        }

        // Получение tax_status клиента
        public string GetClientTaxStatus(int accountId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT c.tax_status
                FROM Client c
                JOIN InvestmentAccount ia ON c.client_id = ia.client_id
                WHERE ia.account_id = @account_id";
            command.Parameters.AddWithValue("@account_id", accountId);
            var result = command.ExecuteScalar();
            return result?.ToString() ?? "Resident";
        }

        // Расчёт средней цены покупки
        public decimal GetAveragePurchasePrice(int accountId, int instrumentId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT 
                    COALING(SUM(quantity * price_per_unit) / SUM(quantity), 0)
                FROM TransactionTable
                WHERE account_id = @account_id 
                  AND instrument_id = @instrument_id 
                  AND type = 'Buy'";
            command.Parameters.AddWithValue("@account_id", accountId);
            command.Parameters.AddWithValue("@instrument_id", instrumentId);
            var result = command.ExecuteScalar();
            return result == DBNull.Value ? 0m : Convert.ToDecimal(result);
        }

        // Добавление выплаты
        public int AddPayout(int transactionId, string type, decimal amount, string payoutDate)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                INSERT INTO Payout (transaction_id, type, amount, payout_date)
                VALUES (@transaction_id, @type, @amount, @payout_date);
                SELECT last_insert_rowid();";
            command.Parameters.AddWithValue("@transaction_id", transactionId);
            command.Parameters.AddWithValue("@type", type);
            command.Parameters.AddWithValue("@amount", amount);
            command.Parameters.AddWithValue("@payout_date", payoutDate);
            return Convert.ToInt32(command.ExecuteScalar());
        }

        // Добавление налогового обязательства
        public void AddTaxObligation(int payoutId, decimal amount, string dueDate, string calculationBasis)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                INSERT INTO TaxObligation (payout_id, amount, due_date, calculation_basis)
                VALUES (@payout_id, @amount, @due_date, @calculation_basis)";
            command.Parameters.AddWithValue("@payout_id", payoutId);
            command.Parameters.AddWithValue("@amount", amount);
            command.Parameters.AddWithValue("@due_date", dueDate);
            command.Parameters.AddWithValue("@calculation_basis", calculationBasis);
            command.ExecuteNonQuery();
        }

        // Расчёт дивидендов
        public int CalculateDividends()
        {
            int payoutCount = 0;
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();

            // Находим инструменты с ожидаемой выплатой до текущей даты
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT instrument_id, name, expected_payout_per_unit, expected_payout_date
                FROM Instrument
                WHERE expected_payout_per_unit IS NOT NULL 
                  AND expected_payout_per_unit > 0
                  AND expected_payout_date IS NOT NULL 
                  AND expected_payout_date <= @current_date";
            command.Parameters.AddWithValue("@current_date", DateTime.Now.ToString("yyyy-MM-dd"));
            var instruments = new List<(int InstrumentId, string Name, decimal PayoutPerUnit, string PayoutDate)>();
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    instruments.Add((
                        reader.GetInt32(0),
                        reader.GetString(1),
                        reader.GetDecimal(2),
                        reader.GetString(3)
                    ));
                    System.Diagnostics.Debug.WriteLine($"Найден инструмент: {reader.GetString(1)}, Выплата: {reader.GetDecimal(2)}, Дата: {reader.GetString(3)}");
                }
            }

            foreach (var instrument in instruments)
            {
                // Находим счета с положительным балансом и последнюю транзакцию покупки, исключая уже выплаченные дивиденды
                command = conn.CreateCommand();
                command.CommandText = @"
                    SELECT 
                        ia.account_id, 
                        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance,
                        MAX(CASE WHEN tr.type = 'Buy' THEN tr.transaction_id ELSE NULL END) AS transaction_id
                    FROM InvestmentAccount ia
                    JOIN TransactionTable tr ON ia.account_id = tr.account_id
                    LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id 
                        AND p.type = 'Dividends' 
                        AND p.payout_date = @payout_date
                    WHERE tr.instrument_id = @instrument_id
                        AND p.payout_id IS NULL
                    GROUP BY ia.account_id
                    HAVING balance > 0";
                command.Parameters.AddWithValue("@instrument_id", instrument.InstrumentId);
                command.Parameters.AddWithValue("@payout_date", instrument.PayoutDate);
                var accounts = new List<(int AccountId, decimal Balance, int? TransactionId)>();
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        accounts.Add((
                            reader.GetInt32(0),
                            reader.GetDecimal(1),
                            reader.IsDBNull(2) ? null : reader.GetInt32(2)
                        ));
                        System.Diagnostics.Debug.WriteLine($"Счёт {reader.GetInt32(0)} баланс для {instrument.Name}: {reader.GetDecimal(1)}, Транзакция: {(reader.IsDBNull(2) ? "Отсутствует" : reader.GetInt32(2).ToString())}");
                    }
                }

                foreach (var account in accounts)
                {
                    if (!account.TransactionId.HasValue)
                    {
                        System.Diagnostics.Debug.WriteLine($"Нет действительной транзакции покупки для счёта {account.AccountId}, инструмент {instrument.Name}");
                        continue;
                    }

                    // Проверяем, не существует ли уже выплата
                    command = conn.CreateCommand();
                    command.CommandText = @"
                        SELECT COUNT(*)
                        FROM Payout p
                        JOIN TransactionTable tr ON p.transaction_id = tr.transaction_id
                        WHERE tr.account_id = @account_id
                          AND tr.instrument_id = @instrument_id
                          AND p.type = 'Dividends'
                          AND p.payout_date = @payout_date";
                    command.Parameters.AddWithValue("@account_id", account.AccountId);
                    command.Parameters.AddWithValue("@instrument_id", instrument.InstrumentId);
                    command.Parameters.AddWithValue("@payout_date", instrument.PayoutDate);
                    var exists = Convert.ToInt32(command.ExecuteScalar()) > 0;
                    if (exists)
                    {
                        System.Diagnostics.Debug.WriteLine($"Выплата уже существует для счёта {account.AccountId}, инструмент {instrument.Name}, дата {instrument.PayoutDate}");
                        continue;
                    }

                    // Рассчитываем сумму выплаты
                    decimal amount = account.Balance * instrument.PayoutPerUnit;
                    System.Diagnostics.Debug.WriteLine($"Создание выплаты для счёта {account.AccountId}, инструмент {instrument.Name}, сумма: {amount}");

                    // Добавляем Payout
                    int payoutId = AddPayout(account.TransactionId.Value, "Dividends", amount, instrument.PayoutDate);
                    System.Diagnostics.Debug.WriteLine($"Выплата создана: payout_id={payoutId}, сумма={amount}");

                    // Находим tax_status клиента
                    string taxStatus = GetClientTaxStatus(account.AccountId);
                    System.Diagnostics.Debug.WriteLine($"Налоговый статус для счёта {account.AccountId}: {(taxStatus == "Resident" ? "Резидент" : "Нерезидент")}");

                    // Рассчитываем налог
                    decimal taxRate = taxStatus == "Resident" ? 0.13m : 0.30m;
                    decimal taxAmount = amount * taxRate;
                    string calculationBasis = $"НДФЛ {(taxRate * 100)}% на дивиденды ({instrument.Name})";
                    string dueDate = DateTime.Parse(instrument.PayoutDate).AddDays(30).ToString("yyyy-MM-dd");

                    // Добавляем TaxObligation
                    AddTaxObligation(payoutId, taxAmount, dueDate, calculationBasis);
                    System.Diagnostics.Debug.WriteLine($"Налоговое обязательство создано для выплаты {payoutId}, сумма: {taxAmount}, срок: {dueDate}");

                    payoutCount++;
                }
            }
            System.Diagnostics.Debug.WriteLine($"Всего создано выплат: {payoutCount}");
            return payoutCount;
        }

        // Получение списка выплат
        public List<PayoutReport> GetPayouts()
        {
            var payouts = new List<PayoutReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT p.payout_id, p.transaction_id, ia.account_id, i.name, p.type, p.amount, p.payout_date
                FROM Payout p
                JOIN TransactionTable tr ON p.transaction_id = tr.transaction_id
                JOIN InvestmentAccount ia ON tr.account_id = ia.account_id
                JOIN Instrument i ON tr.instrument_id = i.instrument_id";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                payouts.Add(new PayoutReport
                {
                    PayoutId = reader.GetInt32(0),
                    TransactionId = reader.GetInt32(1),
                    AccountId = reader.GetInt32(2),
                    InstrumentName = reader.GetString(3),
                    Type = reader.GetString(4) == "Dividends" ? "Дивиденды" : "Прибыль",
                    Amount = reader.GetDecimal(5),
                    PayoutDate = reader.GetString(6)
                });
            }
            return payouts;
        }

        // Получение списка выплат с налогами для главного экрана
        public List<PayoutWithTaxReport> GetPayoutsWithTaxes()
        {
            var reports = new List<PayoutWithTaxReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT 
                    p.payout_id,
                    p.transaction_id,
                    ia.account_id,
                    i.name,
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
                LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                reports.Add(new PayoutWithTaxReport
                {
                    PayoutId = reader.GetInt32(0),
                    TransactionId = reader.GetInt32(1),
                    AccountId = reader.GetInt32(2),
                    InstrumentName = reader.GetString(3),
                    Type = reader.GetString(4) == "Dividends" ? "Дивиденды" : "Прибыль",
                    Amount = reader.GetDecimal(5),
                    PayoutDate = reader.GetString(6),
                    TaxAmount = reader.GetDecimal(7),
                    TaxDueDate = reader.GetString(8),
                    TaxCalculationBasis = reader.GetString(9)
                });
            }
            return reports;
        }

        // Получение баланса счёта
        public decimal GetAccountBalance(int accountId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT COALESCE(SUM(p.amount), 0) - COALESCE(SUM(t.amount), 0)
                FROM InvestmentAccount ia
                LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
                LEFT JOIN Payout p ON tr.transaction_id = p.transaction_id
                LEFT JOIN TaxObligation t ON p.payout_id = t.payout_id
                WHERE ia.account_id = @account_id";
            command.Parameters.AddWithValue("@account_id", accountId);
            return Convert.ToDecimal(command.ExecuteScalar());
        }

        // Получение портфеля счёта
        public List<Instrument> GetAccountPortfolio(int accountId)
        {
            var instruments = new List<Instrument>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT 
                    i.instrument_id, 
                    i.name, 
                    i.category, 
                    i.expected_payout_per_unit, 
                    i.current_price, 
                    i.expected_payout_date,
                    COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) AS balance
                FROM Instrument i
                LEFT JOIN TransactionTable tr ON i.instrument_id = tr.instrument_id AND tr.account_id = @account_id
                GROUP BY i.instrument_id, i.name, i.category, i.expected_payout_per_unit, i.current_price, i.expected_payout_date
                HAVING balance > 0";
            command.Parameters.AddWithValue("@account_id", accountId);
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                instruments.Add(new Instrument
                {
                    InstrumentId = reader.GetInt32(0),
                    Name = reader.GetString(1),
                    Category = reader.GetString(2) switch
                    {
                        "Stock" => "Акция",
                        "Bond" => "Облигация",
                        "ETF" => "ETF",
                        _ => reader.GetString(2)
                    },
                    ExpectedPayoutPerUnit = reader.IsDBNull(3) ? null : reader.GetDecimal(3),
                    CurrentPrice = reader.GetDecimal(4),
                    ExpectedPayoutDate = reader.IsDBNull(5) ? null : reader.GetString(5),
                    Balance = reader.GetDecimal(6)
                });
            }
            return instruments;
        }

        // Отчёт: Инструменты счёта
        public List<AccountInstrumentsReport> GetAccountInstrumentsReport(int accountId)
        {
            var reports = new List<AccountInstrumentsReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT 
                    c.full_name,
                    i.name,
                    i.category,
                    COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) AS balance,
                    i.current_price,
                    COALESCE(SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END), 0) * i.current_price AS total_value
                FROM InvestmentAccount ia
                JOIN Client c ON ia.client_id = c.client_id
                JOIN TransactionTable tr ON ia.account_id = tr.account_id
                JOIN Instrument i ON tr.instrument_id = i.instrument_id
                WHERE ia.account_id = @account_id
                GROUP BY i.instrument_id, c.full_name, i.name, i.category, i.current_price
                HAVING balance > 0";
            command.Parameters.AddWithValue("@account_id", accountId);
            decimal portfolioValue = 0;
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    var report = new AccountInstrumentsReport
                    {
                        ФИОКлиента = reader.GetString(0),
                        НазваниеИнструмента = reader.GetString(1),
                        Категория = reader.GetString(2) switch
                        {
                            "Stock" => "Акция",
                            "Bond" => "Облигация",
                            "ETF" => "ETF",
                            _ => reader.GetString(2)
                        },
                        Количество = reader.GetDecimal(3),
                        ТекущаяЦена = reader.GetDecimal(4),
                        ОбщаяСтоимость = reader.GetDecimal(5)
                    };
                    portfolioValue += report.ОбщаяСтоимость;
                    reports.Add(report);
                }
            }
            foreach (var report in reports)
            {
                report.СтоимостьПортфеля = portfolioValue;
            }
            return reports;
        }

        // CRUD для Client
        public List<Client> GetClients()
        {
            var clients = new List<Client>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "SELECT * FROM Client";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                clients.Add(new Client
                {
                    ClientId = reader.GetInt32(0),
                    TaxStatus = reader.GetString(1) == "Resident" ? "Резидент" : "Нерезидент",
                    FullName = reader.GetString(2),
                    Email = reader.IsDBNull(3) ? null : reader.GetString(3),
                    Phone = reader.IsDBNull(4) ? null : reader.GetString(4),
                    RegistrationDate = reader.GetString(5)
                });
            }
            return clients;
        }

        public void AddClient(Client client)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                INSERT INTO Client (tax_status, full_name, email, phone, registration_date)
                VALUES (@tax_status, @full_name, @email, @phone, @registration_date)";
            command.Parameters.AddWithValue("@tax_status", client.TaxStatus == "Резидент" ? "Resident" : "NonResident");
            command.Parameters.AddWithValue("@full_name", client.FullName);
            command.Parameters.AddWithValue("@email", (object)client.Email ?? DBNull.Value);
            command.Parameters.AddWithValue("@phone", (object)client.Phone ?? DBNull.Value);
            command.Parameters.AddWithValue("@registration_date", client.RegistrationDate);
            command.ExecuteNonQuery();
        }

        public void UpdateClient(Client client)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                UPDATE Client
                SET tax_status = @tax_status, full_name = @full_name, email = @email, phone = @phone, registration_date = @registration_date
                WHERE client_id = @client_id";
            command.Parameters.AddWithValue("@client_id", client.ClientId);
            command.Parameters.AddWithValue("@tax_status", client.TaxStatus == "Резидент" ? "Resident" : "NonResident");
            command.Parameters.AddWithValue("@full_name", client.FullName);
            command.Parameters.AddWithValue("@email", (object)client.Email ?? DBNull.Value);
            command.Parameters.AddWithValue("@phone", (object)client.Phone ?? DBNull.Value);
            command.Parameters.AddWithValue("@registration_date", client.RegistrationDate);
            command.ExecuteNonQuery();
        }

        public void DeleteClient(int clientId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "DELETE FROM Client WHERE client_id = @client_id";
            command.Parameters.AddWithValue("@client_id", clientId);
            command.ExecuteNonQuery();
        }

        // CRUD для InvestmentAccount
        public List<InvestmentAccount> GetInvestmentAccounts()
        {
            var accounts = new List<InvestmentAccount>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT ia.account_id, c.full_name, ia.account_type, ia.open_date, ia.client_id
                FROM InvestmentAccount ia
                JOIN Client c ON ia.client_id = c.client_id";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                var account = new InvestmentAccount
                {
                    ClientName = reader.GetString(1),
                    AccountType = reader.GetString(2) switch
                    {
                        "Brokerage" => "Брокерский",
                        "IIS" => "ИИС",
                        "Trust" => "Доверительный",
                        _ => reader.GetString(2)
                    },
                    OpenDate = reader.GetString(3),
                    ClientId = reader.GetInt32(4) 
                };
                accounts.Add(account);
                System.Diagnostics.Debug.WriteLine($"Счёт {account.AccountId}, Тип: {account.AccountType}, ФИО клиента: {account.ClientName}");
            }
            System.Diagnostics.Debug.WriteLine($"Всего счетов возвращено: {accounts.Count}");
            return accounts;
        }

        public void AddInvestmentAccount(InvestmentAccount account)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                INSERT INTO InvestmentAccount (client_id, account_type, open_date)
                VALUES (@client_id, @account_type, @open_date)";
            command.Parameters.AddWithValue("@client_id", account.ClientId);
            command.Parameters.AddWithValue("@account_type", account.AccountType switch
            {
                "Брокерский" => "Brokerage",
                "ИИС" => "IIS",
                "Доверительный" => "Trust",
                _ => account.AccountType
            });
            command.Parameters.AddWithValue("@open_date", account.OpenDate);
            command.ExecuteNonQuery();
        }

        public void DeleteInvestmentAccount(int accountId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "DELETE FROM InvestmentAccount WHERE account_id = @account_id";
            command.Parameters.AddWithValue("@account_id", accountId);
            command.ExecuteNonQuery();
        }

        // CRUD для Instrument
        public List<Instrument> GetInstruments()
        {
            var instruments = new List<Instrument>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "SELECT * FROM Instrument";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                instruments.Add(new Instrument
                {
                    InstrumentId = reader.GetInt32(0),
                    Name = reader.GetString(1),
                    Category = reader.GetString(2) switch
                    {
                        "Stock" => "Акция",
                        "Bond" => "Облигация",
                        "ETF" => "ETF",
                        _ => reader.GetString(2)
                    },
                    ExpectedPayoutPerUnit = reader.IsDBNull(3) ? null : reader.GetDecimal(3),
                    CurrentPrice = reader.GetDecimal(4),
                    ExpectedPayoutDate = reader.IsDBNull(5) ? null : reader.GetString(5)
                });
            }
            return instruments;
        }

        public void UpdateInstrument(Instrument instrument)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                UPDATE Instrument
                SET name = @name, category = @category, expected_payout_per_unit = @expected_payout_per_unit,
                    current_price = @current_price, expected_payout_date = @expected_payout_date
                WHERE instrument_id = @instrument_id";
            command.Parameters.AddWithValue("@instrument_id", instrument.InstrumentId);
            command.Parameters.AddWithValue("@name", instrument.Name);
            command.Parameters.AddWithValue("@category", instrument.Category switch
            {
                "Акция" => "Stock",
                "Облигация" => "Bond",
                "ETF" => "ETF",
                _ => instrument.Category
            });
            command.Parameters.AddWithValue("@expected_payout_per_unit", (object)instrument.ExpectedPayoutPerUnit ?? DBNull.Value);
            command.Parameters.AddWithValue("@current_price", instrument.CurrentPrice);
            command.Parameters.AddWithValue("@expected_payout_date", (object)instrument.ExpectedPayoutDate ?? DBNull.Value);
            command.ExecuteNonQuery();
        }

        public void DeleteInstrument(int instrumentId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "DELETE FROM Instrument WHERE instrument_id = @instrument_id";
            command.Parameters.AddWithValue("@instrument_id", instrumentId);
            command.ExecuteNonQuery();
        }

        // CRUD для TransactionTable
        public List<TransactionTable> GetTransactions()
        {
            var transactions = new List<TransactionTable>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                SELECT 
                    tr.transaction_id,
                    tr.account_id,
                    tr.instrument_id,
                    tr.type,
                    tr.quantity,
                    tr.price_per_unit,
                    tr.commission,
                    tr.transaction_date,
                    i.name AS instrument_name
                FROM TransactionTable tr
                JOIN Instrument i ON tr.instrument_id = i.instrument_id";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                transactions.Add(new TransactionTable
                {
                    TransactionId = reader.GetInt32(0),
                    AccountId = reader.GetInt32(1),
                    InstrumentId = reader.GetInt32(2),
                    Type = reader.GetString(3) == "Buy" ? "Покупка" : "Продажа",
                    Quantity = reader.GetDecimal(4),
                    PricePerUnit = reader.GetDecimal(5),
                    Commission = reader.GetDecimal(6),
                    TransactionDate = reader.GetString(7),
                    InstrumentName = reader.GetString(8)
                });
            }
            return transactions;
        }

        public int AddTransaction(TransactionTable transaction)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                INSERT INTO TransactionTable (account_id, instrument_id, type, quantity, price_per_unit, commission, transaction_date)
                VALUES (@account_id, @instrument_id, @type, @quantity, @price_per_unit, @commission, @transaction_date);
                SELECT last_insert_rowid();";
            command.Parameters.AddWithValue("@account_id", transaction.AccountId);
            command.Parameters.AddWithValue("@instrument_id", transaction.InstrumentId);
            command.Parameters.AddWithValue("@type", transaction.Type);
            command.Parameters.AddWithValue("@quantity", transaction.Quantity);
            command.Parameters.AddWithValue("@price_per_unit", transaction.PricePerUnit);
            command.Parameters.AddWithValue("@commission", transaction.Commission);
            command.Parameters.AddWithValue("@transaction_date", transaction.TransactionDate);
            return Convert.ToInt32(command.ExecuteScalar());
        }

        public void DeleteTransaction(int transactionId)
        {
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = "DELETE FROM TransactionTable WHERE transaction_id = @transaction_id";
            command.Parameters.AddWithValue("@transaction_id", transactionId);
            command.ExecuteNonQuery();
        }

        // Отчёты
        public List<PortfolioReport> GetPortfolio()
        {
            var reports = new List<PortfolioReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
            WITH Portfolio AS (
                SELECT 
                    ia.account_id,
                    ia.account_type,
                    i.instrument_id,
                    i.name,
                    i.category,
                    i.current_price,
                    i.expected_payout_date,
                    SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) AS balance,
                    SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS total_value
                FROM InvestmentAccount ia
                JOIN TransactionTable tr ON ia.account_id = tr.account_id
                JOIN Instrument i ON tr.instrument_id = i.instrument_id
                GROUP BY ia.account_id, ia.account_type, i.instrument_id, i.name, i.category, i.current_price, i.expected_payout_date
                HAVING balance > 0
            ),
            AccountTotal AS (
                SELECT account_id, COALESCE(SUM(total_value), 0) AS account_value
                FROM Portfolio
                GROUP BY account_id
            )
            SELECT 
                p.account_id,
                p.account_type,
                p.instrument_id,
                p.name,
                p.category,
                p.balance,
                p.total_value,
                COALESCE(CASE WHEN at.account_value > 0 THEN ROUND(1.0 * p.total_value / CAST(at.account_value AS DECIMAL(10,2)) * 100, 2) ELSE 0 END, 0) AS percentage,
                CASE 
                    WHEN p.expected_payout_date IS NOT NULL AND p.expected_payout_date <= date('now', '+7 days') 
                        THEN 'Ожидаемая выплата по ' || p.name || ' на ' || p.expected_payout_date
                    WHEN at.account_value > 0 AND p.total_value / at.account_value * 100 > 50 
                        THEN 'Внимание: Доля инструмента ' || p.name || ' превышает 50% портфеля'
                    ELSE 'Нет уведомлений' 
                END AS notification
            FROM Portfolio p
            LEFT JOIN AccountTotal at ON p.account_id = at.account_id
            WHERE p.balance > 0
            ORDER BY p.account_id, p.total_value DESC;";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                var report = new PortfolioReport
                {
                    КодСчета = reader.GetInt32(0),
                    ТипСчёта = reader.GetString(1) switch
                    {
                        "Brokerage" => "Брокерский",
                        "IIS" => "ИИС",
                        "Trust" => "Доверительный",
                        _ => reader.GetString(1)
                    },
                    НазваниеИнструмента = reader.GetString(3),
                    Категория = reader.GetString(4) switch
                    {
                        "Stock" => "Акция",
                        "Bond" => "Облигация",
                        "ETF" => "ETF",
                        _ => reader.GetString(4)
                    },
                    Количество = reader.GetDecimal(5),
                    ОбщаяСтоимость = reader.GetDecimal(6),
                    ДоляВПортфеле = reader.GetDecimal(7),
                    Уведомление = reader.GetString(8)
                };
                reports.Add(report);
                System.Diagnostics.Debug.WriteLine($"Портфель: Счёт {report.ТипСчёта}, Инструмент {report.НазваниеИнструмента}, Баланс: {report.Количество}, Общая стоимость: {report.ОбщаяСтоимость}, Доля: {report.ДоляВПортфеле}%, Уведомление: {report.Уведомление}");
            }
            return reports;
        }

        public List<FinancialPositionReport> GetFinancialPosition()
        {
            var reports = new List<FinancialPositionReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
                WITH Portfolio AS (
                    SELECT 
                        ia.account_id,
                        ia.account_type,
                        SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) * i.current_price AS portfolio_value
                    FROM InvestmentAccount ia
                    LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
                    LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
                    GROUP BY ia.account_id, ia.account_type
                    HAVING SUM(CASE WHEN tr.type = 'Buy' THEN tr.quantity ELSE -tr.quantity END) > 0
                )
                SELECT 
                    ia.account_id,
                    ia.account_type,
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
                GROUP BY ia.account_id, ia.account_type, c.full_name, pf.portfolio_value";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                reports.Add(new FinancialPositionReport
                {
                    ТипСчёта = reader.GetString(1) switch
                    {
                        "Brokerage" => "Брокерский",
                        "IIS" => "ИИС",
                        "Trust" => "Доверительный",
                        _ => reader.GetString(1)
                    },
                    ФИОКлиента = reader.GetString(2),
                    БалансСчёта = reader.GetDecimal(3),
                    СтоимостьПортфеля = reader.GetDecimal(4),
                    ОбщееБогатство = reader.GetDecimal(5)
                });
            }
            return reports;
        }

        public List<ClientProfileReport> GetClientProfile()
        {
            var reports = new List<ClientProfileReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
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
                GROUP BY c.client_id, c.full_name, c.tax_status, c.email, c.phone, c.registration_date";
            using var reader = command.ExecuteReader();
            while (reader.Read())
            {
                reports.Add(new ClientProfileReport
                {
                    ФИОКлиента = reader.GetString(1),
                    НалоговыйСтатус = reader.GetString(2) == "Resident" ? "Резидент" : "Нерезидент",
                    ЭлектроннаяПочта = reader.IsDBNull(3) ? null : reader.GetString(3),
                    Телефон = reader.IsDBNull(4) ? null : reader.GetString(4),
                    ДатаРегистрации = reader.GetString(5),
                    КоличествоСчетов = reader.GetInt32(6),
                    ОбщаяСуммаВыплат = reader.GetDecimal(7),
                    КоличествоТранзакций = reader.GetInt32(8)
                });
            }
            return reports;
        }

        public List<NotificationReport> GetNotifications()
        {
            var reports = new List<NotificationReport>();
            using var conn = new SQLiteConnection(connectionString);
            conn.Open();
            var command = conn.CreateCommand();
            command.CommandText = @"
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
                        THEN 'Ожидаемая выплата по ' || i.name || ' на ' || i.expected_payout_date
                        WHEN at.account_value > 0 AND p.total_value / at.account_value * 100 > 50 
                        THEN 'Внимание: Доля инструмента ' || p.name || ' превышает 50% портфеля'
                        ELSE 'Нет уведомлений'
                    END AS notification
                FROM Client c
                JOIN InvestmentAccount ia ON c.client_id = ia.client_id
                LEFT JOIN TransactionTable tr ON ia.account_id = tr.account_id
                LEFT JOIN Instrument i ON tr.instrument_id = i.instrument_id
                LEFT JOIN Portfolio p ON ia.account_id = p.account_id AND i.instrument_id = p.instrument_id
                LEFT JOIN AccountTotal at ON ia.account_id = at.account_id
                WHERE (i.expected_payout_date IS NOT NULL AND i.expected_payout_date <= date('now', '+7 days'))
                   OR (at.account_value > 0 AND p.total_value / at.account_value * 100 > 50)
                   OR 1=1";
            using var reader = command.ExecuteReader();
            int count = 0;
            while (reader.Read())
            {
                var report = new NotificationReport
                {
                    КодКлиента = reader.GetInt32(0),
                    ФИОКлиента = reader.GetString(1) ?? "Неизвестный клиент",
                    Уведомление = reader.GetString(2)
                };
                reports.Add(report);
                count++;
                System.Diagnostics.Debug.WriteLine($"Уведомление #{count}: КлиентID={report.КодКлиента}, ФИО={report.ФИОКлиента}, Текст={report.Уведомление}");
            }
            System.Diagnostics.Debug.WriteLine($"Всего уведомлений возвращено: {count}");
            return reports;
        }

        // Модели данных
        public class Client
        {
            public int ClientId { get; set; }
            public string TaxStatus { get; set; } // Налоговый статус
            public string FullName { get; set; } // ФИО
            public string Email { get; set; } // Электронная почта
            public string Phone { get; set; } // Телефон
            public string RegistrationDate { get; set; } // Дата регистрации
        }

        public class InvestmentAccount
        {
            public int AccountId { get; set; }

            public string ClientName { get; set; } // ФИО клиента
            public int ClientId { get; set; }
            public string AccountType { get; set; } // Тип счёта
            public string OpenDate { get; set; } // Дата открытия
        }

        public class Instrument
        {
            public int InstrumentId { get; set; }
            public string Name { get; set; } // Название
            public string Category { get; set; } // Категория
            public decimal? ExpectedPayoutPerUnit { get; set; } // Ожидаемая выплата за единицу
            public decimal CurrentPrice { get; set; } // Текущая цена
            public string ExpectedPayoutDate { get; set; } // Ожидаемая дата выплаты
            public decimal Balance { get; set; } // Баланс
        }

        public class TransactionTable
        {
            public int TransactionId { get; set; }
            public int AccountId { get; set; }
            public int InstrumentId { get; set; }
            public string Type { get; set; } // Тип (Покупка/Продажа)
            public decimal Quantity { get; set; } // Количество
            public decimal PricePerUnit { get; set; } // Цена за единицу
            public decimal Commission { get; set; } // Комиссия
            public string TransactionDate { get; set; } // Дата транзакции
            public string InstrumentName { get; set; } // Название инструмента
        }

        public class PayoutReport
        {
            public int PayoutId { get; set; }
            public int TransactionId { get; set; }
            public int AccountId { get; set; }
            public string InstrumentName { get; set; } // Название инструмента
            public string Type { get; set; } // Тип выплаты
            public decimal Amount { get; set; } // Сумма
            public string PayoutDate { get; set; } // Дата выплаты
        }

        public class PayoutWithTaxReport
        {
            public int PayoutId { get; set; }
            public int TransactionId { get; set; }
            public int AccountId { get; set; }
            public string InstrumentName { get; set; } // Название инструмента
            public string Type { get; set; } // Тип выплаты
            public decimal Amount { get; set; } // Сумма выплаты
            public string PayoutDate { get; set; } // Дата выплаты
            public decimal TaxAmount { get; set; } // Сумма налога
            public string TaxDueDate { get; set; } // Срок уплаты налога
            public string TaxCalculationBasis { get; set; } // Основание расчёта налога
        }

        public class PortfolioReport
        {
            public int КодСчета { get; set; }
            public string ТипСчёта { get; set; } // Тип счёта
            public string НазваниеИнструмента { get; set; } // Название инструмента
            public string Категория { get; set; } // Категория
            public decimal Количество { get; set; } // Количество
            public decimal ОбщаяСтоимость { get; set; } // Общая стоимость
            public decimal ДоляВПортфеле { get; set; } // Доля в портфеле
            public string Уведомление { get; set; } // Уведомление
        }

        public class FinancialPositionReport
        {
            public string ТипСчёта { get; set; } // Тип счёта
            public string ФИОКлиента { get; set; } // ФИО клиента
            public decimal БалансСчёта { get; set; } // Баланс счёта
            public decimal СтоимостьПортфеля { get; set; } // Стоимость портфеля
            public decimal ОбщееБогатство { get; set; } // Общее богатство
        }

        public class ClientProfileReport
        {
            public string ФИОКлиента { get; set; } // ФИО клиента
            public string НалоговыйСтатус { get; set; } // Налоговый статус
            public string ЭлектроннаяПочта { get; set; } // Электронная почта
            public string Телефон { get; set; } // Телефон
            public string ДатаРегистрации { get; set; } // Дата регистрации
            public int КоличествоСчетов { get; set; } // Количество счетов
            public decimal ОбщаяСуммаВыплат { get; set; } // Общая сумма выплат
            public int КоличествоТранзакций { get; set; } // Количество транзакций
        }

        public class NotificationReport
        {
            public int КодКлиента { get; set; }
            public string ФИОКлиента { get; set; } // ФИО клиента
            public string Уведомление { get; set; } // Уведомление
        }

        public class AccountInstrumentsReport
        {
            public string ФИОКлиента { get; set; } // ФИО клиента
            public string НазваниеИнструмента { get; set; } // Название инструмента
            public string Категория { get; set; } // Категория
            public decimal Количество { get; set; } // Количество
            public decimal ТекущаяЦена { get; set; } // Текущая цена
            public decimal ОбщаяСтоимость { get; set; } // Общая стоимость
            public decimal СтоимостьПортфеля { get; set; } // Стоимость портфеля
        }
    }
}