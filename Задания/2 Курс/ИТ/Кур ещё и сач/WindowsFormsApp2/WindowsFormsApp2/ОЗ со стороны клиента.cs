using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.OleDb;
using System.Drawing;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                if (textBox1.Text == null ||
                    textBox2.Text == null ||
                    textBox3.Text == null ||
                    textBox4.Text == null)
                {
                    MessageBox.Show("Не все данные введены!");
                    return;
                }

                //string id = dataGridView1.Rows[index].Cells[0].Value.ToString();
                string type = textBox1.Text;
                string tel_number = textBox3.Text;
                string mail = textBox2.Text;
                string FIO = textBox1.Text;

                Random random = new Random();
                int id = random.Next(999);

                string connectionstring = "Provider = Microsoft.ACE.OLEDB.12.0;Data source=DB.accdb";
                OleDbConnection dbConnection = new OleDbConnection(connectionstring);


                dbConnection.Open();
                string query = "INSERT INTO Клиент VALUES (" + Convert.ToString(id) + ",'" + FIO + "', '" + mail + "', " + tel_number + " )";
                OleDbCommand dbCommand = new OleDbCommand(query, dbConnection);

                if (dbCommand.ExecuteNonQuery() != 1)
                    MessageBox.Show("Ошибка выполнения запроса");
                else
                    MessageBox.Show("Ваша заявка отправлена на рассмотрение!");

                dbConnection.Close();
            }
            catch
            {
                MessageBox.Show("Не все даныне веденны!");
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
