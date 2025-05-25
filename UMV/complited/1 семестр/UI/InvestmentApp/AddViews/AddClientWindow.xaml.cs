using System;
using System.Windows;
using static InvestmentApp.DatabaseService;
using System.Windows.Controls;

namespace InvestmentApp
{
    public partial class AddClientWindow : Window
    {
        public Client Client { get; private set; }

        public AddClientWindow()
        {
            InitializeComponent();
            RegistrationDatePicker.SelectedDate = DateTime.Now;
        }

        private void Save_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(FullNameTextBox.Text))
            {
                MessageBox.Show("Введите ФИО.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (TaxStatusComboBox.SelectedItem == null)
            {
                MessageBox.Show("Выберите налоговый статус.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!RegistrationDatePicker.SelectedDate.HasValue)
            {
                MessageBox.Show("Выберите дату регистрации.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            Client = new Client
            {
                FullName = FullNameTextBox.Text,
                TaxStatus = (TaxStatusComboBox.SelectedItem as ComboBoxItem).Content.ToString(),
                Email = string.IsNullOrWhiteSpace(EmailTextBox.Text) ? null : EmailTextBox.Text,
                Phone = string.IsNullOrWhiteSpace(PhoneTextBox.Text) ? null : PhoneTextBox.Text,
                RegistrationDate = RegistrationDatePicker.SelectedDate.Value.ToString("yyyy-MM-dd")
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