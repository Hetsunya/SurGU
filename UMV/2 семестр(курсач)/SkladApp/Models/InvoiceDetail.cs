namespace SkladApp.Models
{
    public class InvoiceDetail
    {
        public int ID_Детали { get; set; }
        public int ID_Накладной { get; set; }
        public int ID_Товара { get; set; }
        public int Количество { get; set; }
    }
}