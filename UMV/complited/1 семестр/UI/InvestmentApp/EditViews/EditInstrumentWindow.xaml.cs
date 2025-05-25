using System;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using static InvestmentApp.DatabaseService;

namespace InvestmentApp
{
    public partial class EditInstrumentWindow : Window
    {
        public Instrument Instrument { get; private set; }

        public EditInstrumentWindow(Instrument instrument)
        {
            InitializeComponent();
            Instrument = instrument;
            NameTextBox.Text = instrument.Name;
            CategoryComboBox.SelectedItem = CategoryComboBox.Items.Cast<ComboBoxItem>().FirstOrDefault(i => i.Content.ToString() == instrument.Category);
            ExpectedPayoutPerUnitTextBox.Text = instrument.ExpectedPayoutPerUnit?.ToString();
            CurrentPriceTextBox.Text = instrument.CurrentPrice.ToString();
            ExpectedPayoutDatePicker.SelectedDate = string.IsNullOrEmpty(instrument.ExpectedPayoutDate) ? null : DateTime.Parse(instrument.ExpectedPayoutDate);
        }

        private void Save_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(NameTextBox.Text))
            {
                MessageBox.Show("Введите название инструмента.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (CategoryComboBox.SelectedItem == null)
            {
                MessageBox.Show("Выберите категорию инструмента.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!decimal.TryParse(CurrentPriceTextBox.Text, out decimal currentPrice) || currentPrice <= 0)
            {
                MessageBox.Show("Введите корректную текущую цену.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            decimal? expectedPayoutPerUnit = null;
            if (!string.IsNullOrWhiteSpace(ExpectedPayoutPerUnitTextBox.Text) && (!decimal.TryParse(ExpectedPayoutPerUnitTextBox.Text, out decimal payout) || payout < 0))
            {
                MessageBox.Show("Введите корректную ожидаемую выплату за единицу.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            else if (!string.IsNullOrWhiteSpace(ExpectedPayoutPerUnitTextBox.Text))
            {
                expectedPayoutPerUnit = decimal.Parse(ExpectedPayoutPerUnitTextBox.Text);
            }

            Instrument.Name = NameTextBox.Text;
            Instrument.Category = (CategoryComboBox.SelectedItem as ComboBoxItem).Content.ToString();
            Instrument.ExpectedPayoutPerUnit = expectedPayoutPerUnit;
            Instrument.CurrentPrice = currentPrice;
            Instrument.ExpectedPayoutDate = ExpectedPayoutDatePicker.SelectedDate?.ToString("yyyy-MM-dd");

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