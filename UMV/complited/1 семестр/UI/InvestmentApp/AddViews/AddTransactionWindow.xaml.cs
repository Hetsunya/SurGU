using System;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace InvestmentApp
{
    public partial class AddTransactionWindow : Window
    {
        private readonly DatabaseService dbService;
        public DatabaseService.TransactionTable Transaction { get; private set; }
        private const decimal CommissionRate = 0.003m; // 0.3%

        public AddTransactionWindow()
        {
            InitializeComponent();
            dbService = new DatabaseService();
            AccountCombo.ItemsSource = dbService.GetInvestmentAccounts();
            TransactionDateText.Text = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
        }

        private void AccountCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            UpdateInstrumentCombo();
        }

        private void TypeCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            UpdateInstrumentCombo();
        }

        private void UpdateInstrumentCombo()
        {
            InstrumentBalanceText.Text = "Выберите инструмент и тип Продажа";
            if (AccountCombo.SelectedItem is DatabaseService.InvestmentAccount account && TypeCombo.SelectedItem is ComboBoxItem typeItem)
            {
                string type = typeItem.Content.ToString();
                if (type == "Продажа")
                {
                    // Только инструменты с положительным балансом на счёте
                    var portfolio = dbService.GetAccountPortfolio(account.AccountId);
                    InstrumentCombo.ItemsSource = portfolio.Where(i => i.Balance > 0).ToList();
                    // Отладочный вывод
                    string instrumentsList = string.Join(", ", portfolio.Select(i => $"{i.Name}: {i.Balance}"));
                    System.Diagnostics.Debug.WriteLine($"Счёт {account.AccountId} портфель: {instrumentsList}");
                }
                else
                {
                    // Все доступные инструменты
                    InstrumentCombo.ItemsSource = dbService.GetInstruments();
                }
            }
            else
            {
                InstrumentCombo.ItemsSource = null;
            }
            InstrumentCombo.SelectedIndex = -1;
            PricePerUnitText.Text = string.Empty;
            CommissionText.Text = string.Empty;
        }

        private void InstrumentCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (InstrumentCombo.SelectedItem is DatabaseService.Instrument instrument)
            {
                // Отображаем цену и обновляем комиссию для любого типа
                PricePerUnitText.Text = instrument.CurrentPrice.ToString();
                UpdateCommission();

                // Отображаем баланс только для Продажа
                if (TypeCombo.SelectedItem is ComboBoxItem typeItem &&
                    typeItem.Content.ToString() == "Продажа" &&
                    AccountCombo.SelectedItem is DatabaseService.InvestmentAccount account)
                {
                    var portfolio = dbService.GetAccountPortfolio(account.AccountId);
                    var balance = portfolio.FirstOrDefault(i => i.InstrumentId == instrument.InstrumentId)?.Balance ?? 0;
                    InstrumentBalanceText.Text = $"Доступно: {balance} {instrument.Name}";
                }
                else
                {
                    InstrumentBalanceText.Text = "Выберите инструмент и тип Продажа";
                }
            }
            else
            {
                InstrumentBalanceText.Text = "Выберите инструмент и тип Продажа";
                PricePerUnitText.Text = string.Empty;
                CommissionText.Text = string.Empty;
            }
        }

        private void QuantityText_TextChanged(object sender, TextChangedEventArgs e)
        {
            UpdateCommission();
        }

        private void UpdateCommission()
        {
            if (decimal.TryParse(QuantityText.Text, out decimal quantity) && quantity > 0 &&
                decimal.TryParse(PricePerUnitText.Text, out decimal price) && price > 0)
            {
                decimal dealAmount = quantity * price;
                decimal commission = dealAmount * CommissionRate;
                CommissionText.Text = commission.ToString("F2");
            }
            else
            {
                CommissionText.Text = string.Empty;
            }
        }

        private void Save_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // проверка на дублирование
                if (Transaction != null)
                {
                    System.Diagnostics.Debug.WriteLine("Транзакция уже создана — повторное нажатие?");
                    return;
                }

                if (AccountCombo.SelectedItem == null)
                    throw new Exception("Необходимо выбрать счёт.");
                if (InstrumentCombo.SelectedItem == null)
                    throw new Exception("Необходимо выбрать инструмент.");
                if (TypeCombo.SelectedItem == null)
                    throw new Exception("Необходимо выбрать тип транзакции.");
                if (string.IsNullOrWhiteSpace(QuantityText.Text) || !decimal.TryParse(QuantityText.Text, out decimal quantity) || quantity <= 0)
                    throw new Exception("Некорректное количество (должно быть положительным).");
                if (string.IsNullOrWhiteSpace(PricePerUnitText.Text) || !decimal.TryParse(PricePerUnitText.Text, out decimal price) || price <= 0)
                    throw new Exception("Некорректная цена (выберите инструмент).");
                if (string.IsNullOrWhiteSpace(CommissionText.Text) || !decimal.TryParse(CommissionText.Text, out decimal commission) || commission < 0)
                    throw new Exception("Некорректная комиссия.");
                if (string.IsNullOrWhiteSpace(TransactionDateText.Text) || !DateTime.TryParse(TransactionDateText.Text, out _))
                    throw new Exception("Некорректная дата транзакции (используйте формат yyyy-MM-dd HH:mm:ss).");

                var account = AccountCombo.SelectedItem as DatabaseService.InvestmentAccount;
                var instrument = InstrumentCombo.SelectedItem as DatabaseService.Instrument;
                string type = (TypeCombo.SelectedItem as ComboBoxItem).Content.ToString() == "Покупка" ? "Buy" : "Sell";

                // Проверка баланса инструмента при продаже
                if (type == "Sell")
                {
                    var portfolio = dbService.GetAccountPortfolio(account.AccountId);
                    var instrumentBalance = portfolio.FirstOrDefault(i => i.InstrumentId == instrument.InstrumentId)?.Balance ?? 0;
                    if (quantity > instrumentBalance)
                        throw new Exception($"Недостаточно инструмента на счёте. Доступно: {instrumentBalance}.");
                }

                // Создание транзакции
                Transaction = new DatabaseService.TransactionTable
                {
                    AccountId = account.AccountId,
                    InstrumentId = instrument.InstrumentId,
                    Type = type,
                    Quantity = quantity,
                    PricePerUnit = price,
                    Commission = commission,
                    TransactionDate = TransactionDateText.Text
                };

                int transactionId = dbService.AddTransaction(Transaction);

                // Обработка прибыли при продаже
                if (type == "Sell")
                {
                    // Получаем среднюю цену покупки
                    decimal avgPurchasePrice = dbService.GetAveragePurchasePrice(account.AccountId, instrument.InstrumentId);
                    if (avgPurchasePrice == 0)
                        throw new Exception("История покупок для этого инструмента отсутствует.");

                    // Рассчитываем прибыль
                    decimal profit = (price - avgPurchasePrice) * quantity;
                    if (profit > 0)
                    {
                        // Создаём выплату (Profit)
                        int payoutId = dbService.AddPayout(transactionId, "Profit", profit, TransactionDateText.Text);

                        // Получаем tax_status клиента
                        var taxStatus = dbService.GetClientTaxStatus(account.AccountId);

                        // Рассчитываем налог
                        decimal taxRate = taxStatus == "Resident" ? 0.13m : 0.30m;
                        decimal taxAmount = profit * taxRate;
                        string calculationBasis = $"НДФЛ {(taxRate * 100)}% на прибыль от продажи ({instrument.Name})";

                        // Создаём налоговое обязательство
                        dbService.AddTaxObligation(payoutId, taxAmount, DateTime.Parse(TransactionDateText.Text).AddDays(30).ToString("yyyy-MM-dd"), calculationBasis);
                    }
                }

                DialogResult = true;
                Close();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Ошибка при сохранении: {ex.Message}");
                MessageBox.Show($"Ошибка: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}