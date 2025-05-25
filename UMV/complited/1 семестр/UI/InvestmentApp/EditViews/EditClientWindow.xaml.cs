using System;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using static InvestmentApp.DatabaseService;

namespace InvestmentApp
{
    public partial class EditClientWindow : Window
    {
        public Client Client { get; private set; }

        public EditClientWindow(Client client)
        {
            InitializeComponent();
            Client = client;
            FullNameTextBox.Text = client.FullName;
            TaxStatusComboBox.SelectedItem = TaxStatusComboBox.Items.Cast<ComboBoxItem>().FirstOrDefault(i => i.Content.ToString() == client.TaxStatus);
            EmailTextBox.Text = client.Email;
            PhoneTextBox.Text = client.Phone;
            RegistrationDatePicker.SelectedDate = DateTime.Parse(client.RegistrationDate);
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

            Client.FullName = FullNameTextBox.Text;
            Client.TaxStatus = (TaxStatusComboBox.SelectedItem as ComboBoxItem).Content.ToString();
            Client.Email = string.IsNullOrWhiteSpace(EmailTextBox.Text) ? null : EmailTextBox.Text;
            Client.Phone = string.IsNullOrWhiteSpace(PhoneTextBox.Text) ? null : PhoneTextBox.Text;
            Client.RegistrationDate = RegistrationDatePicker.SelectedDate.Value.ToString("yyyy-MM-dd");

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