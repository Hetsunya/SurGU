namespace SkladApp.Models
{
    public class Product
    {
        public int ID_Товара { get; set; }
        public string Артикул { get; set; }
        public string Наименование { get; set; }
        public int ID_Поставщика { get; set; }
        public int ID_Места { get; set; }
        public decimal Цена_За_Единицу { get; set; }
        public string Дата_Поступления { get; set; }
        public int Количество_На_Складе { get; set; }
        public decimal Масса_Единицы { get; set; }
        public string Единица_Измерения { get; set; }
        public string Категория_Товара { get; set; }
    }
}