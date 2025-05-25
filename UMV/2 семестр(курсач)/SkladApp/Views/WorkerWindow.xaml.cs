using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Windows;
using System.Windows.Controls;
using SkladApp.Models;

namespace SkladApp.Views
{
    public partial class WorkerWindow : Window
    {
        private readonly User _currentUser;
        private readonly Dictionary<string, DataGrid> _dataGrids;

        public WorkerWindow(User currentUser)
        {
            InitializeComponent();
            _currentUser = currentUser;
            UserInfoTextBlock.Text = $"User: {_currentUser.ФИО} (Worker)";

            _dataGrids = new Dictionary<string, DataGrid>
            {
                { "Накладная", InvoicesDataGrid },
                { "Детали_Накладной", InvoiceDetailsDataGrid },
                { "Товар", ProductsDataGrid },
                { "Место_Хранения", StorageLocationsDataGrid }
            };

            LoadData("Накладная");
        }

        private void TabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (TabControl.SelectedItem is TabItem tabItem)
            {
                string tableName = tabItem.Header.ToString() switch
                {
                    "Invoices" => "Накладная",
                    "Invoice Details" => "Детали_Накладной",
                    "Products" => "Товар",
                    "Storage Locations" => "Место_Хранения",
                    _ => ""
                };
                LoadData(tableName);
            }
        }

        private void LoadData(string tableName)
        {
            try
            {
                using (var connection = new SQLiteConnection("Data Source=sklad.db;Version=3;"))
                {
                    connection.Open();
                    string query = $"SELECT * FROM {tableName}";
                    using (var command = new SQLiteCommand(query, connection))
                    {
                        using (var adapter = new SQLiteDataAdapter(command))
                        {
                            var table = new System.Data.DataTable();
                            adapter.Fill(table);
                            _dataGrids[tableName].ItemsSource = table.DefaultView;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }

        private void AddButton_Click(object sender, RoutedEventArgs e)
        {
            var selectedTab = TabControl.SelectedItem as TabItem;
            string tableName = selectedTab?.Header.ToString() switch
            {
                "Invoices" => "Накладная",
                "Invoice Details" => "Детали_Накладной",
                "Products" => "Товар",
                "Storage Locations" => "Место_Хранения",
                _ => ""
            };
            if (!string.IsNullOrEmpty(tableName))
            {
                new EditWindow(tableName).ShowDialog();
                LoadData(tableName);
            }
        }

        private void DataGrid_MouseDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (sender is DataGrid dataGrid && dataGrid.SelectedItem is System.Data.DataRowView rowView)
            {
                var selectedTab = TabControl.SelectedItem as TabItem;
                string tableName = selectedTab?.Header.ToString() switch
                {
                    "Invoices" => "Накладная",
                    "Invoice Details" => "Детали_Накладной",
                    "Products" => "Товар",
                    "Storage Locations" => "Место_Хранения",
                    _ => ""
                };

                if (!string.IsNullOrEmpty(tableName))
                {
                    object record = tableName switch
                    {
                        "Накладная" => new Invoice
                        {
                            ID_Накладной = Convert.ToInt32(rowView["ID_Накладной"]),
                            Номер_Документа = rowView["Номер_Документа"].ToString(),
                            Дата_Составления = rowView["Дата_Составления"].ToString(),
                            ID_Заказа = Convert.ToInt32(rowView["ID_Заказа"]),
                            ID_Пользователя = Convert.ToInt32(rowView["ID_Пользователя"]),
                            Статус_Накладной = rowView["Статус_Накладной"] is DBNull ? null : rowView["Статус_Накладной"].ToString()
                        },
                        "Детали_Накладной" => new InvoiceDetail
                        {
                            ID_Детали = Convert.ToInt32(rowView["ID_Детали"]),
                            ID_Накладной = Convert.ToInt32(rowView["ID_Накладной"]),
                            ID_Товара = Convert.ToInt32(rowView["ID_Товара"]),
                            Количество = Convert.ToInt32(rowView["Количество"])
                        },
                        "Товар" => new Product
                        {
                            ID_Товара = Convert.ToInt32(rowView["ID_Товара"]),
                            Артикул = rowView["Артикул"].ToString(),
                            Наименование = rowView["Наименование"].ToString(),
                            ID_Поставщика = Convert.ToInt32(rowView["ID_Поставщика"]),
                            ID_Места = Convert.ToInt32(rowView["ID_Места"]),
                            Цена_За_Единицу = Convert.ToDecimal(rowView["Цена_За_Единицу"]),
                            Дата_Поступления = rowView["Дата_Поступления"].ToString(),
                            Количество_На_Складе = Convert.ToInt32(rowView["Количество_На_Складе"]),
                            Масса_Единицы = Convert.ToDecimal(rowView["Масса_Единицы"])
                        },
                        "Место_Хранения" => new StorageLocation
                        {
                            ID_Места = Convert.ToInt32(rowView["ID_Места"]),
                            Зона = rowView["Зона"].ToString(),
                            Стеллаж = rowView["Стеллаж"].ToString(),
                            Ячейка = rowView["Ячейка"].ToString()
                        },
                        _ => null
                    };

                    new EditWindow(tableName, record).ShowDialog();
                    LoadData(tableName);
                }
            }
        }
    }
}