using System.Data.SQLite;
using System.Windows;
using SkladApp.Models;
using SkladApp.Views;

namespace SkladApp.Views // Исправлено пространство имен
{
    public partial class LoginWindow : Window
    {
        public LoginWindow()
        {
            InitializeComponent(); // Вызываем InitializeComponent для связки с XAML
        }

        private void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                using (var connection = new SQLiteConnection("Data Source=sklad.db;Version=3;"))
                {
                    connection.Open();
                    string query = "SELECT * FROM Пользователь WHERE Логин = @Логин AND Пароль = @Пароль";
                    using (var command = new SQLiteCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("@Логин", LoginTextBox.Text);
                        command.Parameters.AddWithValue("@Пароль", PasswordBox.Password);
                        using (var reader = command.ExecuteReader())
                        {
                            if (reader.Read())
                            {
                                var user = new User
                                {
                                    ID_Пользователя = reader.GetInt32(0),
                                    ФИО = reader.GetString(1),
                                    Роль = reader.GetString(2),
                                    Логин = reader.GetString(3),
                                    Пароль = reader.GetString(4),
                                    Email = reader.IsDBNull(5) ? null : reader.GetString(5)
                                };

                                Window mainWindow = user.Роль switch
                                {
                                    "Администратор" => new AdminWindow(user),
                                    "Кладовщик" => new WorkerWindow(user),
                                    "Менеджер" => new ManagerWindow(user),
                                    _ => null
                                };

                                if (mainWindow != null)
                                {
                                    mainWindow.Show();
                                    Close();
                                }
                                else
                                {
                                    MessageBox.Show("Unknown role");
                                }
                            }
                            else
                            {
                                MessageBox.Show("Invalid login or password");
                            }
                        }
                    }
                }
            }
            catch (System.Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }
    }
}