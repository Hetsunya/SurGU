namespace SkladApp.Models
{
    public class Order
    {
        public int ID_Заказа { get; set; }
        public string Номер_Заказа { get; set; }
        public string Дата_Оформления { get; set; }
        public int ID_Заказчика { get; set; }
        public int ID_Пользователя { get; set; }
        public string Статус_Заказа { get; set; }
        public string Дата_Доставки { get; set; }
    }
}