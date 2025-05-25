using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Windows;
using System.Windows.Controls;
using SkladApp.Models;

namespace SkladApp.Views
{
    public partial class ManagerWindow : Window
    {
        private readonly User _currentUser;
        private readonly Dictionary<string, DataGrid> _dataGrids;

        public ManagerWindow(User currentUser)
        {
            InitializeComponent();
            _currentUser = currentUser;
            UserInfoTextBlock.Text = $"User: {_currentUser.ФИО} (Manager)";

            _dataGrids = new Dictionary<string, DataGrid>
            {
                { "Заказ", OrdersDataGrid },
                { "Детали_Заказа", OrderDetailsDataGrid },
                { "Заказчик", CustomersDataGrid },
                { "Поставщик", SuppliersDataGrid }
            };

            LoadData("Заказ");
        }

        private void TabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (TabControl.SelectedItem is TabItem tabItem)
            {
                string tableName = tabItem.Header.ToString() switch
                {
                    "Orders" => "Заказ",
                    "Order Details" => "Детали_Заказа",
                    "Customers" => "Заказчик",
                    "Suppliers" => "Поставщик",
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
                "Orders" => "Заказ",
                "Order Details" => "Детали_Заказа",
                "Customers" => "Заказчик",
                "Suppliers" => "Поставщик",
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
                    "Orders" => "Заказ",
                    "Order Details" => "Детали_Заказа",
                    "Customers" => "Заказчик",
                    "Suppliers" => "Поставщик",
                    _ => ""
                };

                if (!string.IsNullOrEmpty(tableName))
                {
                    object record = tableName switch
                    {
                        "Заказ" => new Order
                        {
                            ID_Заказа = Convert.ToInt32(rowView["ID_Заказа"]),
                            Номер_Заказа = rowView["Номер_Заказа"].ToString(),
                            Дата_Оформления = rowView["Дата_Оформления"].ToString(),
                            ID_Заказчика = Convert.ToInt32(rowView["ID_Заказчика"]),
                            ID_Пользователя = Convert.ToInt32(rowView["ID_Пользователя"]),
                            Статус_Заказа = rowView["Статус_Заказа"] is DBNull ? null : rowView["Статус_Заказа"].ToString(),
                            Дата_Доставки = rowView["Дата_Доставки"] is DBNull ? null : rowView["Дата_Доставки"].ToString()
                        },
                        "Детали_Заказа" => new OrderDetail
                        {
                            ID_Детали = Convert.ToInt32(rowView["ID_Детали"]),
                            ID_Заказа = Convert.ToInt32(rowView["ID_Заказа"]),
                            ID_Товара = Convert.ToInt32(rowView["ID_Товара"]),
                            Количество = Convert.ToInt32(rowView["Количество"]),
                            Цена_За_Единицу = Convert.ToDecimal(rowView["Цена_За_Единицу"])
                        },
                        "Заказчик" => new Customer
                        {
                            ID_Заказчика = Convert.ToInt32(rowView["ID_Заказчика"]),
                            Тип_Заказчика = rowView["Тип_Заказчика"].ToString(),
                            ФИО = rowView["ФИО"].ToString(),
                            Email = rowView["Email"] is DBNull ? null : rowView["Email"].ToString(),
                            Номер_Телефона = rowView["Номер_Телефона"] is DBNull ? null : rowView["Номер_Телефона"].ToString(),
                            Адрес_Доставки = rowView["Адрес_Доставки"].ToString(),
                            Серия_Номер_Паспорта = rowView["Серия_Номер_Паспорта"] is DBNull ? null : rowView["Серия_Номер_Паспорта"].ToString(),
                            ИНН = rowView["ИНН"] is DBNull ? null : rowView["ИНН"].ToString(),
                            Название = rowView["Название"] is DBNull ? null : rowView["Название"].ToString(),
                            КПП = rowView["КПП"] is DBNull ? null : rowView["КПП"].ToString()
                        },
                        "Поставщик" => new Supplier
                        {
                            ID_Поставщика = Convert.ToInt32(rowView["ID_Поставщика"]),
                            ИНН = rowView["ИНН"].ToString(),
                            Название = rowView["Название"].ToString(),
                            Адрес = rowView["Адрес"].ToString(),
                            Контактное_Лицо = rowView["Контактное_Лицо"] is DBNull ? null : rowView["Контактное_Лицо"].ToString(),
                            Банковские_Реквизиты = rowView["Банковские_Реквизиты"] is DBNull ? null : rowView["Банковские_Реквизиты"].ToString()
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