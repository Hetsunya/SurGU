using Microsoft.VisualBasic.FileIO;
using System.Diagnostics;
using System.DirectoryServices;
using System.IO;

namespace lab4
{
    public partial class Form1 : Form
    {
        private string filePath = "C:";
        private bool isFile = false;
        private string currentlySelectedItemName = "";
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            FilePathTextBox.Text = filePath;
            LoadFilesAndDirectories();
        }

        public void LoadFilesAndDirectories()
        {
            DirectoryInfo fileList;
            string tempFilePath = "";
            FileAttributes fileAttr;
            try
            {
                if (isFile)
                {
                    fileList = new DirectoryInfo(filePath);
                    FileInfo[] files = fileList.GetFiles(); // GETS ALL THE FILES 
                    DirectoryInfo[] dirs = fileList.GetDirectories(); //GET ALL THE DIRS
                    tempFilePath = filePath + "/" + currentlySelectedItemName;

                    //—¬Œ…—“¬¿ ‘¿…ÀŒ¬
                    FileInfo fileDtetails = new FileInfo(tempFilePath);
                    FileNameLabel.Text = fileDtetails.Name;
                    FileTypeLabel.Text = fileDtetails.Extension;
                    FileSizeLabel.Text = Convert.ToString(fileDtetails.Length);
                    FileCreationTimeLabel.Text = Convert.ToString(fileDtetails.CreationTime);
                    fileAttr = System.IO.File.GetAttributes(tempFilePath);
                }
                else
                {
                    //—¬Œ…—“¬¿ œ¿œŒ 
                    FileCreationTimeLabel.Text = Convert.ToString(Directory.GetCreationTime(filePath));
                    FilesInDirLabel.Text = Convert.ToString(Directory.GetFiles(filePath).Count());
                    fileAttr = System.IO.File.GetAttributes(filePath);
                }

                if ((fileAttr & FileAttributes.Directory) == FileAttributes.Directory)
                {
                    fileList = new DirectoryInfo(filePath);
                    FileInfo[] files = fileList.GetFiles(); // GETS ALL THE FILES 
                    DirectoryInfo[] dirs = fileList.GetDirectories(); //GET ALL THE DIRS
                    //string fileExtension = "";
                    SubDirLabel.Text = Convert.ToString(dirs.Length);

                    listView1.Items.Clear();

                    //¬€¬Œƒ ‘¿…ÀŒ¬
                    for (int i = 0; i < files.Length; i++)
                    {
                        //fileExtension = files[i].Extension.ToUpper();
                        listView1.Items.Add(f[i].Name, 1);
                    }
                    //¬€¬Œƒ œ¿œŒ 
                    for (int i = 0; i < dirs.Length; i++)
                    {
                        listView1.Items.Add(dirs[i].Name, 1);
                    }
                }
                else
                {
                    FileNameLabel.Text = this.currentlySelectedItemName;
                }
            }
            catch(Exception e)
            {

            }
        }
        public void LoadButtonAction()
        {
            RemoveBackSlash();
            filePath = FilePathTextBox.Text;
            LoadFilesAndDirectories();
            isFile = false;
        }

        public void GoBack()
        {
            try
            {
                RemoveBackSlash();
                string path = FilePathTextBox.Text;
                path = path.Substring(0, path.LastIndexOf("/"));
                this.isFile = false;
                FilePathTextBox.Text = path;
                RemoveBackSlash();
            }
            catch(Exception e)
            {

            }
        }
        public void RemoveBackSlash()
        {
            string path = FilePathTextBox.Text;
            if (path.LastIndexOf("/") == path.Length - 1)
            {
                FilePathTextBox.Text = path.Substring(0, path.Length - 1);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            GoBack();
            LoadButtonAction();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void listView1_ItemSelectionChanged(object sender, ListViewItemSelectionChangedEventArgs e)
        {
            currentlySelectedItemName = e.Item.Text;

            FileAttributes fileAttr = System.IO.File.GetAttributes(filePath + "/" + currentlySelectedItemName);

            if((fileAttr & FileAttributes.Directory) == FileAttributes.Directory)
            {
                isFile = false;
                FilePathTextBox.Text = filePath + "/" + currentlySelectedItemName;
            }
            else
            {
                isFile = true;
            }
             
        }

        private void button3_Click(object sender, EventArgs e)
        {
            LoadButtonAction();
        }

        private void listView1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            LoadButtonAction();
        }

        private void label1_Click_1(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void FileFindButton_Click(object sender, EventArgs e)
        {
            string tempFilePath = "";
            FileAttributes fileAttr;
            try
            {
                if (isFile)
                {
                    //tempFilePath = filePath + "/" + currentlySelectedItemName;
                    fileAttr = System.IO.File.GetAttributes(tempFilePath);
                }
                else
                {
                    fileAttr = System.IO.File.GetAttributes(filePath);
                }

                if ((fileAttr & FileAttributes.Directory) == FileAttributes.Directory)
                {
                    listView1.Items.Clear();

                    //System.IO.SearchOption.TopDirectoryOnly ›“Œ ÃŒ∆≈“ »ƒ“» 3 ¿–√”Ã≈Õ“ŒÃ ¬ GETFILES
                    string[] filess = System.IO.Directory.GetFiles(filePath, "*" + FileFindTextBox.Text + "*");
                    string[] dirss = System.IO.Directory.GetDirectories(filePath, "*" + FileFindTextBox.Text + "*");

                    for (int i = 0; i < filess.Length; i++)
                     {
                        listView1.Items.Add(filess[i], 12);
                    }
                     for (int i = 0; i < dirss.Length; i++)
                     {
                         listView1.Items.Add(dirss[i], 1);
                     }
                }
                else
                {
                    FileNameLabel.Text = this.currentlySelectedItemName;
                }
            }
            catch
            {

            }

        }

        private void label1_Click_2(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void FilePathTextBox_TextChanged(object sender, EventArgs e)
        {

        }
    }
}