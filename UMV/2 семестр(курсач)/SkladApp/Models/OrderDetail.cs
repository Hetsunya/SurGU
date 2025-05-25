namespace SkladApp.Models
{
    public class OrderDetail
    {
        public int ID_Детали { get; set; }
        public int ID_Заказа { get; set; }
        public int ID_Товара { get; set; }
        public int Количество { get; set; }
        public decimal Цена_За_Единицу { get; set; }
    }
}