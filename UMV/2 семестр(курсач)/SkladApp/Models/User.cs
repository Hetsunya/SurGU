namespace SkladApp.Models
{
    public class User
    {
        public int ID_Пользователя { get; set; }
        public string ФИО { get; set; }
        public string Роль { get; set; }
        public string Логин { get; set; }
        public string Пароль { get; set; }
        public string Email { get; set; }
    }
}