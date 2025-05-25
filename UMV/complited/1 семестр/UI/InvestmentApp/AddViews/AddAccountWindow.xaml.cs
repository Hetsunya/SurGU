using System;
using System.Windows;
using static InvestmentApp.DatabaseService;
using System.Windows.Controls;

namespace InvestmentApp
{
    public partial class AddAccountWindow : Window
    {
        private readonly DatabaseService dbService;
        public InvestmentAccount Account { get; private set; }

        public AddAccountWindow()
        {
            InitializeComponent();
            dbService = new DatabaseService();
            OpenDatePicker.SelectedDate = DateTime.Now;
            LoadClients();
        }

        private void LoadClients()
        {
            ClientComboBox.ItemsSource = dbService.GetClients();
        }

        private void Save_Click(object sender, RoutedEventArgs e)
        {
            if (ClientComboBox.SelectedItem == null)
            {
                MessageBox.Show("Выберите клиента.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (AccountTypeComboBox.SelectedItem == null)
            {
                MessageBox.Show("Выберите тип счёта.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!OpenDatePicker.SelectedDate.HasValue)
            {
                MessageBox.Show("Выберите дату открытия.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            Account = new InvestmentAccount
            {
                ClientId = ((Client)ClientComboBox.SelectedItem).ClientId,
                AccountType = (AccountTypeComboBox.SelectedItem as ComboBoxItem).Content.ToString(),
                OpenDate = OpenDatePicker.SelectedDate.Value.ToString("yyyy-MM-dd")
            };

            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}