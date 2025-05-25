namespace SkladApp.Models
{
    public class Invoice
    {
        public int ID_Накладной { get; set; }
        public string Номер_Документа { get; set; }
        public string Дата_Составления { get; set; }
        public int ID_Заказа { get; set; }
        public int ID_Пользователя { get; set; }
        public string Статус_Накладной { get; set; }
    }
}