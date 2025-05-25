using System;
using System.Windows;
using System.Windows.Controls;
using static InvestmentApp.DatabaseService;

namespace InvestmentApp
{
    public partial class MainWindow : Window
    {
        private readonly DatabaseService dbService;

        public MainWindow()
        {
            InitializeComponent();
            dbService = new DatabaseService();
            LoadData();
        }

        private void LoadData()
        {
            ClientsGrid.ItemsSource = dbService.GetClients();
            AccountsGrid.ItemsSource = dbService.GetInvestmentAccounts();
            InstrumentsGrid.ItemsSource = dbService.GetInstruments();
            TransactionsGrid.ItemsSource = dbService.GetTransactions();
            PayoutsGrid.ItemsSource = dbService.GetPayoutsWithTaxes();
            NotificationsGrid.ItemsSource = dbService.GetNotifications();
        }

        private void AddClient_Click(object sender, RoutedEventArgs e)
        {
            var window = new AddClientWindow();
            if (window.ShowDialog() == true)
            {
                dbService.AddClient(window.Client);
                LoadData();
            }
        }

        private void EditClient_Click(object sender, RoutedEventArgs e)
        {
            if (ClientsGrid.SelectedItem is Client selectedClient)
            {
                var window = new EditClientWindow(selectedClient);
                if (window.ShowDialog() == true)
                {
                    dbService.UpdateClient(window.Client);
                    LoadData();
                }
            }
            else
            {
                MessageBox.Show("Выберите клиента для редактирования.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void DeleteClient_Click(object sender, RoutedEventArgs e)
        {
            if (ClientsGrid.SelectedItem is Client selectedClient)
            {
                if (MessageBox.Show($"Вы уверены, что хотите удалить клиента {selectedClient.FullName}?", "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
                {
                    try
                    {
                        dbService.DeleteClient(selectedClient.ClientId);
                        LoadData();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка при удалении клиента: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Выберите клиента для удаления.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void AddAccount_Click(object sender, RoutedEventArgs e)
        {
            var window = new AddAccountWindow();
            if (window.ShowDialog() == true)
            {
                dbService.AddInvestmentAccount(window.Account);
                LoadData();
            }
        }

        private void DeleteAccount_Click(object sender, RoutedEventArgs e)
        {
            if (AccountsGrid.SelectedItem is InvestmentAccount selectedAccount)
            {
                if (MessageBox.Show($"Вы уверены, что хотите удалить счёт {selectedAccount.AccountId}?", "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
                {
                    try
                    {
                        dbService.DeleteInvestmentAccount(selectedAccount.AccountId);
                        LoadData();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка при удалении счёта: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Выберите счёт для удаления.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void EditInstrument_Click(object sender, RoutedEventArgs e)
        {
            if (InstrumentsGrid.SelectedItem is Instrument selectedInstrument)
            {
                var window = new EditInstrumentWindow(selectedInstrument);
                if (window.ShowDialog() == true)
                {
                    dbService.UpdateInstrument(window.Instrument);
                    LoadData();
                }
            }
            else
            {
                MessageBox.Show("Выберите инструмент для редактирования.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void DeleteInstrument_Click(object sender, RoutedEventArgs e)
        {
            if (InstrumentsGrid.SelectedItem is Instrument selectedInstrument)
            {
                if (MessageBox.Show($"Вы уверены, что хотите удалить инструмент {selectedInstrument.Name}?", "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
                {
                    try
                    {
                        dbService.DeleteInstrument(selectedInstrument.InstrumentId);
                        LoadData();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка при удалении инструмента: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Выберите инструмент для удаления.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void AddTransaction_Click(object sender, RoutedEventArgs e)
        {
            var window = new AddTransactionWindow();
            if (window.ShowDialog() == true)
            {
                //dbService.AddTransaction(window.Transaction);
                LoadData();
            }
        }

        private void DeleteTransaction_Click(object sender, RoutedEventArgs e)
        {
            if (TransactionsGrid.SelectedItem is TransactionTable selectedTransaction)
            {
                if (MessageBox.Show($"Вы уверены, что хотите удалить транзакцию {selectedTransaction.TransactionId}?", "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
                {
                    try
                    {
                        dbService.DeleteTransaction(selectedTransaction.TransactionId);
                        LoadData();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Ошибка при удалении транзакции: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
            else
            {
                MessageBox.Show("Выберите транзакцию для удаления.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void CalculateDividends_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                int count = dbService.CalculateDividends();
                MessageBox.Show($"Рассчитано выплат: {count}", "Успех", MessageBoxButton.OK, MessageBoxImage.Information);
                LoadData();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при расчёте дивидендов: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void PortfolioReport_Click(object sender, RoutedEventArgs e)
        {
            ReportsGrid.ItemsSource = dbService.GetPortfolio();
        }

        private void FinancialPositionReport_Click(object sender, RoutedEventArgs e)
        {
            ReportsGrid.ItemsSource = dbService.GetFinancialPosition();
        }

        private void ClientProfileReport_Click(object sender, RoutedEventArgs e)
        {
            ReportsGrid.ItemsSource = dbService.GetClientProfile();
        }

        private void AccountInstrumentsReport_Click(object sender, RoutedEventArgs e)
        {
            if (!int.TryParse(AccountIdForReportTextBox.Text, out int accountId) || accountId <= 0)
            {
                MessageBox.Show("Введите корректный ID счёта для отчёта.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                var report = dbService.GetAccountInstrumentsReport(accountId);
                if (report.Count == 0)
                {
                    MessageBox.Show("Для указанного счёта нет данных.", "Информация", MessageBoxButton.OK, MessageBoxImage.Information);
                }
                ReportsGrid.ItemsSource = report;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при получении отчёта: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}