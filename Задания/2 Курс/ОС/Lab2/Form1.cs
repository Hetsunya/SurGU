using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Lab2
{
    public partial class Form1 : Form
    {
        int dx = 0, dy = 0;
        int count = 0;
        static Mutex m = new Mutex();

        public Form1()
        {
            InitializeComponent();
        }

        void mythread1()
        {
            //for (int i = 0; i < 10; i++)
            while(true)
            {
                m.WaitOne();
                // БЛОКИ TRY & FINALLY ЛОМАЮТ  
                try
                {
                    while (true)
                    {
                        button3.Location = new Point(button3.Location.X - dx, button3.Location.Y - dy);
                        count++;
                        button3.Text = Convert.ToString(count);
                        Thread.Sleep(700);
                    }
                }
                finally
                {
                    m.ReleaseMutex();
                }
            }
        }

        void mythread2()
        {
            Random rnd = new Random();
            m.WaitOne();

            try
            {
                while (true)
                {
                    dx = rnd.Next(-10, 10);
                    dy = rnd.Next(-10, 10);
                    Thread.Sleep(700);
                }
            }
            finally
            {
                m.ReleaseMutex();
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }

        private void button3_Click(object sender, EventArgs e)
        {
            CheckForIllegalCrossThreadCalls = false;

            Thread thread2 = new Thread(mythread2);
            Thread thread1 = new Thread(mythread1);
            thread2.Start();
            thread1.Start();
        }
    }
}
