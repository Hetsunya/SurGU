using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lab7
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            dataGridView1.Columns.Add("Id", "Номер");
            dataGridView1.Columns.Add("Contetnt", "Значение");
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
        }

        private void label1_Click(object sender, EventArgs e)
        {
           
    }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            String textFile = "";
            String line;
            try
            {
                StreamReader sr = new StreamReader("D:\\lab7\\test.txt");
                line = sr.ReadLine();
                while (line != null)
                {
                    textFile += line;
                    line = sr.ReadLine();
                }
                sr.Close();
                Console.ReadLine();
            }
            catch
            {
                MessageBox.Show("Ошибка при попытке прочитать файл");
                return;
            }

            if (textFile.Length == 0)
            {
                MessageBox.Show("Пустой файл");
                return;
            }
            
            dataGridView1.Rows.Clear();
            
        
            int blockLength;
            try
            {
                blockLength = Int32.Parse(textCount.Text.ToLower().Trim());
            }
            catch
            {
                MessageBox.Show("В поле count нужно ввести число");
                return;
            }
            
            string block;
            string resultFind = "";
            string findValue = textSearch.Text.ToLower();
            int index = 0;

            for (int i = 1; i < textFile.Length; i += blockLength)
            {
                if (textFile.Length - i > blockLength)
                    block = textFile.Substring(i, blockLength);
                else
                    block = textFile.Substring(i, textFile.Length - i);

                index++;
                dataGridView1.Rows.Add((index).ToString(), block);


                if (block.Contains(findValue) || block.Contains(findValue.ToUpperInvariant()))
                {
                    resultFind += index.ToString() + " ";
                }
            }

            if (resultFind == "")
                textBox1.Text = "Не найдено";
            else
                textBox1.Text = resultFind;
        }

        private void textPathFile_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
