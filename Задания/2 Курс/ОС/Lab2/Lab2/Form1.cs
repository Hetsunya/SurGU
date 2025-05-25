using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Lab2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        void MyFunc(object sender, EventArgs e)
        {
            //string s = textBox1.Text.ToString();
            //int a = Convert.ToInt32(s);
            //a = a + 2;
            //MessageBox.Show(a.ToString());
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //CheckForIllegalCrossThreadCalls = false;
            //Thread t = new Thread(MyFunc);
            // t.Start();
            button1.Location = new Point(button1.Location.X, button1.Location.Y - 10);
        }
    }
}
