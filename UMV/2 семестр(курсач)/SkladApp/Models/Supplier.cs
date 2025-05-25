namespace SkladApp.Models
{
    public class Supplier
    {
        public int ID_Поставщика { get; set; }
        public string ИНН { get; set; }
        public string Название { get; set; }
        public string Адрес { get; set; }
        public string Контактное_Лицо { get; set; }
        public string Банковские_Реквизиты { get; set; }
    }
}