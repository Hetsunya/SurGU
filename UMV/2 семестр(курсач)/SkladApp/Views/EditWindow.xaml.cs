using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Linq;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;

namespace SkladApp.Views
{
    public partial class EditWindow : Window
    {
        private readonly object _record;
        private readonly string _tableName;
        private readonly Dictionary<string, TextBox> _textBoxes = new Dictionary<string, TextBox>();

        public EditWindow(string tableName, object record = null)
        {
            InitializeComponent();
            _tableName = tableName;
            _record = record;

            GenerateFields();
        }

        private void GenerateFields()
        {
            var properties = GetTableProperties(_tableName);
            foreach (var prop in properties)
            {
                var label = new Label { Content = $"{prop.Name}:" };
                FieldsPanel.Children.Add(label);

                var textBox = new TextBox { Margin = new Thickness(0, 0, 0, 10) };
                if (_record != null)
                {
                    var value = _record.GetType().GetProperty(prop.Name)?.GetValue(_record);
                    textBox.Text = value?.ToString();
                }
                FieldsPanel.Children.Add(textBox);
                _textBoxes[prop.Name] = textBox;
            }
        }

        private List<PropertyInfo> GetTableProperties(string tableName)
        {
            var type = tableName switch
            {
                "Пользователь" => typeof(Models.User),
                "Товар" => typeof(Models.Product),
                "Место_Хранения" => typeof(Models.StorageLocation),
                "Заказчик" => typeof(Models.Customer),
                "Заказ" => typeof(Models.Order),
                "Детали_Заказа" => typeof(Models.OrderDetail),
                "Накладная" => typeof(Models.Invoice),
                "Детали_Накладной" => typeof(Models.InvoiceDetail),
                "Поставщик" => typeof(Models.Supplier),
                _ => throw new ArgumentException("Unknown table")
            };
            return type.GetProperties().ToList();
        }

        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Определяем isUpdate в начале метода, чтобы она была доступна везде
                bool isUpdate = _record != null;

                using (var connection = new SQLiteConnection("Data Source=sklad.db;Version=3;"))
                {
                    connection.Open();
                    var properties = GetTableProperties(_tableName);

                    string query;
                    if (isUpdate)
                    {
                        var setClause = string.Join(", ", properties.Skip(1).Select(p => $"{p.Name} = @{p.Name}"));
                        query = $"UPDATE {_tableName} SET {setClause} WHERE {properties[0].Name} = @{properties[0].Name}";
                    }
                    else
                    {
                        var columns = string.Join(", ", properties.Select(p => p.Name));
                        var values = string.Join(", ", properties.Select(p => $"@{p.Name}"));
                        query = $"INSERT INTO {_tableName} ({columns}) VALUES ({values})";
                    }

                    using (var command = new SQLiteCommand(query, connection))
                    {
                        foreach (var prop in properties)
                        {
                            var value = _textBoxes[prop.Name].Text;
                            if (string.IsNullOrEmpty(value) && prop.PropertyType != typeof(int) && prop.PropertyType != typeof(decimal))
                            {
                                command.Parameters.AddWithValue($"@{prop.Name}", DBNull.Value);
                            }
                            else
                            {
                                command.Parameters.AddWithValue($"@{prop.Name}", value);
                            }
                        }
                        command.ExecuteNonQuery();
                    }
                }

                // Используем isUpdate для сообщения
                MessageBox.Show(isUpdate ? "Record updated" : "Record added");
                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }

        private void DeleteButton_Click(object sender, RoutedEventArgs e)
        {
            if (_record == null) return;

            try
            {
                using (var connection = new SQLiteConnection("Data Source=sklad.db;Version=3;"))
                {
                    connection.Open();
                    var primaryKey = GetTableProperties(_tableName)[0].Name;
                    var query = $"DELETE FROM {_tableName} WHERE {primaryKey} = @{primaryKey}";
                    using (var command = new SQLiteCommand(query, connection))
                    {
                        command.Parameters.AddWithValue($"@{primaryKey}", _textBoxes[primaryKey].Text);
                        command.ExecuteNonQuery();
                    }
                }
                MessageBox.Show("Record deleted");
                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }
    }
}