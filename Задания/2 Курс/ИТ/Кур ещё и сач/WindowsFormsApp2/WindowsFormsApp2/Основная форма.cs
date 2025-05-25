using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.OleDb;
using System.Drawing;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    //testdlyaprogi@mail.ru
    //QWERTY12345YTREW
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView2.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;

            dataGridView1.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells;
            dataGridView2.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells;
        }

        private void LoadButton_Click(object sender, EventArgs e)
        {
            this.dataGridView1.Rows.Clear();

            string connectionstring = "Provider = Microsoft.ACE.OLEDB.12.0;Data source=DB.accdb";
            OleDbConnection dbConnection = new OleDbConnection(connectionstring);

            dbConnection.Open();
            string query = "SELECT * FROM Груз";
            OleDbCommand dbCommand = new OleDbCommand(query, dbConnection);
            OleDbDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows == false)
            {
                MessageBox.Show("Данные ненайдены!", "Ошибка");
            }
            else
            {
                while (dbReader.Read())
                {
                    dataGridView1.Rows.Add(dbReader["id"], dbReader["Классификация груза"], dbReader["Цена"], dbReader["id Водителя"], dbReader["id Транспорта"], dbReader["id клиента"]);
                }
            }

            dbReader.Close();
            dbConnection.Close();
        }

        private void AddButton_Click(object sender, EventArgs e)
        {
            if(dataGridView1.SelectedRows.Count != 1)
            {
                MessageBox.Show("Выберите одну строку!");
                return;
            }

            int index = dataGridView1.SelectedRows[0].Index;

            if (dataGridView1.Rows[index].Cells[0].Value == null ||
                dataGridView1.Rows[index].Cells[1].Value == null ||
                dataGridView1.Rows[index].Cells[2].Value == null ||
                dataGridView1.Rows[index].Cells[3].Value == null ||
                dataGridView1.Rows[index].Cells[4].Value == null)
            {
                MessageBox.Show("Не все данные введены!");
                return;
            }

            string id = dataGridView1.Rows[index].Cells[0].Value.ToString();
            string type = dataGridView1.Rows[index].Cells[1].Value.ToString();
            string cost = dataGridView1.Rows[index].Cells[2].Value.ToString();
            string id_driver = dataGridView1.Rows[index].Cells[3].Value.ToString();
            string id_transport = dataGridView1.Rows[index].Cells[4].Value.ToString();
            string id_client = dataGridView1.Rows[index].Cells[5].Value.ToString();

            string connectionstring = "Provider = Microsoft.ACE.OLEDB.12.0;Data source=DB.accdb";
            OleDbConnection dbConnection = new OleDbConnection(connectionstring);

            dbConnection.Open();
            string query = "INSERT INTO Груз VALUES (" + id + ", ' " + type + " ', " + cost + ", " + id_driver + ", " + id_transport + ", " + id_client + ")";
            OleDbCommand dbCommand = new OleDbCommand(query, dbConnection);

            if (dbCommand.ExecuteNonQuery() != 1)
                MessageBox.Show("Ошибка выполнения запроса");
            else
                MessageBox.Show("Даныне добавлены");

            dbConnection.Close();

        }

        private void ExitButton_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void DeleteButton_Click(object sender, EventArgs e)
        {
            if (dataGridView1.SelectedRows.Count != 1)
            {
                MessageBox.Show("Выберите одну строку!");
                return;
            }

            int index = dataGridView1.SelectedRows[0].Index;

            if (dataGridView1.Rows[index].Cells[0].Value == null)
            {
                MessageBox.Show("Не все данные введены!");
                return;
            }

            string id = dataGridView1.Rows[index].Cells[0].Value.ToString();

            string connectionstring = "Provider = Microsoft.ACE.OLEDB.12.0;Data source=DB.accdb";
            OleDbConnection dbConnection = new OleDbConnection(connectionstring);

            dbConnection.Open();
            string query = "DELETE FROM Груз WHERE id = " + id;
            OleDbCommand dbCommand = new OleDbCommand(query, dbConnection);

            if (dbCommand.ExecuteNonQuery() != 1)
                MessageBox.Show("Ошибка выполнения запроса");
            else
            {
                MessageBox.Show("Даныне удалены!");
                dataGridView1.Rows.RemoveAt(index);
            }

            dbConnection.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form2 form2 = new Form2();
            Form1 form1 = new Form1();
            form1.Hide();
            form2.Show();
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            try
            {
                SmtpClient mySmtpClient = new SmtpClient("smtp.mail.ru");
                mySmtpClient.UseDefaultCredentials = true;
                mySmtpClient.EnableSsl = true;
                //UF9eQrvcuQkYmLsZZkpc - ПАРОЛЬ ДЛЯ ВНЕШНИХ ПРИЛОЖЕНИЙ 
                System.Net.NetworkCredential basicAuthenticationInfo = new
                    System.Net.NetworkCredential("vitalick113@mail.ru", "UF9eQrvcuQkYmLsZZkpc");
                mySmtpClient.Credentials = basicAuthenticationInfo;

                MailAddress from = new MailAddress("vitalick113@mail.ru", "Компания");
                MailAddress to = new MailAddress("testdlyaprogi@mail.ru", "Ваш груз доставлен!");
                MailMessage myMail = new System.Net.Mail.MailMessage(from, to);

                // add ReplyTo
                MailAddress replyTo = new MailAddress("for_vpn101@mail.ru");
                myMail.ReplyToList.Add(replyTo);

                myMail.Subject = "Test message";
                myMail.SubjectEncoding = System.Text.Encoding.UTF8;

                // set body-message and encoding
                myMail.Body = "<b>Груз доставлен!</b>";
                myMail.BodyEncoding = System.Text.Encoding.UTF8;
                // text or html
                myMail.IsBodyHtml = true;

                mySmtpClient.Send(myMail);
                MessageBox.Show("Уведомление отправлено!");
            }
            catch
            {
                MessageBox.Show("Ошибка при отправке уведомления!");
            }
        }

        private void button1_Click_2(object sender, EventArgs e)
        {

        }

        private void button1_Click_3(object sender, EventArgs e)
        {
            /*try
            {
                SmtpClient mySmtpClient = new SmtpClient("smtp.mail.ru");
                mySmtpClient.UseDefaultCredentials = true;
                mySmtpClient.EnableSsl = true;
                //UF9eQrvcuQkYmLsZZkpc - ПАРОЛЬ ДЛЯ ВНЕШНИХ ПРИЛОЖЕНИЙ 
                System.Net.NetworkCredential basicAuthenticationInfo = new
                    System.Net.NetworkCredential("vitalick113@mail.ru", "UF9eQrvcuQkYmLsZZkpc");
                mySmtpClient.Credentials = basicAuthenticationInfo;

                MailAddress from = new MailAddress("vitalick113@mail.ru", "Компания");
                MailAddress to = new MailAddress("testdlyaprogi@mail.ru", "Ваш заказ принят!");
                MailMessage myMail = new System.Net.Mail.MailMessage(from, to);

                // add ReplyTo
                MailAddress replyTo = new MailAddress("for_vpn101@mail.ru");
                myMail.ReplyToList.Add(replyTo);

                myMail.Subject = "Test message";
                myMail.SubjectEncoding = System.Text.Encoding.UTF8;

                // set body-message and encoding
                myMail.Body = "<b>Ваше заявление было рассмотрено и одобренно!</b>";
                myMail.BodyEncoding = System.Text.Encoding.UTF8;
                // text or html
                myMail.IsBodyHtml = true;

                mySmtpClient.Send(myMail);
                MessageBox.Show("Уведомление отправлено!");
            }
            catch
            {
                MessageBox.Show("Ошибка при отправке уведомления!");
            }*/
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.dataGridView2.Rows.Clear();
            string connectionstring = "Provider = Microsoft.ACE.OLEDB.12.0;Data source=DB.accdb";
            OleDbConnection dbConnection = new OleDbConnection(connectionstring);

            dbConnection.Open();
            string query = "SELECT * FROM Клиент";
            OleDbCommand dbCommand = new OleDbCommand(query, dbConnection);
            OleDbDataReader dbReader = dbCommand.ExecuteReader();

            if (dbReader.HasRows == false)
            {
                MessageBox.Show("Данные ненайдены!", "Ошибка");
            }
            else
            {
                while (dbReader.Read())
                {
                    dataGridView2.Rows.Add(dbReader["id"], dbReader["ФИО"], dbReader["mail"], dbReader["Номер телефона"]);
                }
            }

            dbReader.Close();
            dbConnection.Close();
        }

        private void UpdateButton_Click(object sender, EventArgs e)
        {
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
