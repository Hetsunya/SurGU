namespace SkladApp.Models
{
    public class Customer
    {
        public int ID_Заказчика { get; set; }
        public string Тип_Заказчика { get; set; }
        public string ФИО { get; set; }
        public string Email { get; set; }
        public string Номер_Телефона { get; set; }
        public string Адрес_Доставки { get; set; }
        public string Серия_Номер_Паспорта { get; set; }
        public string ИНН { get; set; }
        public string Название { get; set; }
        public string КПП { get; set; }
    }
}