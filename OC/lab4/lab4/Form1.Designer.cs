namespace lab4
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.BackButton = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.PathLabel = new System.Windows.Forms.Label();
            this.FilePathTextBox = new System.Windows.Forms.TextBox();
            this.listView1 = new System.Windows.Forms.ListView();
            this.IconList = new System.Windows.Forms.ImageList(this.components);
            this.FileNameLabel = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.FileTypeLabel = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.FileFindTextBox = new System.Windows.Forms.TextBox();
            this.FileFindButton = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.FileCreationTimeLabel = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.FilesInDirLabel = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.FileSizeLabel = new System.Windows.Forms.Label();
            this.Label7 = new System.Windows.Forms.Label();
            this.SubDirLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // BackButton
            // 
            this.BackButton.Location = new System.Drawing.Point(12, 6);
            this.BackButton.Name = "BackButton";
            this.BackButton.Size = new System.Drawing.Size(38, 23);
            this.BackButton.TabIndex = 0;
            this.BackButton.Text = "<<";
            this.BackButton.UseVisualStyleBackColor = true;
            this.BackButton.Click += new System.EventHandler(this.button1_Click);
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(756, 6);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(68, 24);
            this.button3.TabIndex = 2;
            this.button3.Text = "Открыть";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // PathLabel
            // 
            this.PathLabel.AutoSize = true;
            this.PathLabel.Location = new System.Drawing.Point(56, 10);
            this.PathLabel.Name = "PathLabel";
            this.PathLabel.Size = new System.Drawing.Size(36, 15);
            this.PathLabel.TabIndex = 3;
            this.PathLabel.Text = "Путь:";
            this.PathLabel.Click += new System.EventHandler(this.label1_Click);
            // 
            // FilePathTextBox
            // 
            this.FilePathTextBox.Location = new System.Drawing.Point(98, 7);
            this.FilePathTextBox.Name = "FilePathTextBox";
            this.FilePathTextBox.Size = new System.Drawing.Size(177, 23);
            this.FilePathTextBox.TabIndex = 4;
            this.FilePathTextBox.TextChanged += new System.EventHandler(this.FilePathTextBox_TextChanged);
            // 
            // listView1
            // 
            this.listView1.LargeImageList = this.IconList;
            this.listView1.Location = new System.Drawing.Point(212, 35);
            this.listView1.Name = "listView1";
            this.listView1.Size = new System.Drawing.Size(687, 463);
            this.listView1.SmallImageList = this.IconList;
            this.listView1.TabIndex = 5;
            this.listView1.UseCompatibleStateImageBehavior = false;
            this.listView1.ItemSelectionChanged += new System.Windows.Forms.ListViewItemSelectionChangedEventHandler(this.listView1_ItemSelectionChanged);
            this.listView1.SelectedIndexChanged += new System.EventHandler(this.listView1_SelectedIndexChanged);
            this.listView1.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.listView1_MouseDoubleClick);
            // 
            // IconList
            // 
            this.IconList.ColorDepth = System.Windows.Forms.ColorDepth.Depth32Bit;
            this.IconList.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("IconList.ImageStream")));
            this.IconList.TransparentColor = System.Drawing.Color.Transparent;
            this.IconList.Images.SetKeyName(0, "doc.png");
            this.IconList.Images.SetKeyName(1, "folder.png");
            this.IconList.Images.SetKeyName(2, "icons8-exe-80.png");
            this.IconList.Images.SetKeyName(3, "icons8-folder-80.png");
            this.IconList.Images.SetKeyName(4, "icons8-mp3-80.png");
            this.IconList.Images.SetKeyName(5, "icons8-pdf-48.png");
            this.IconList.Images.SetKeyName(6, "icons8-rar-80.png");
            this.IconList.Images.SetKeyName(7, "icons8-video-file-48.png");
            this.IconList.Images.SetKeyName(8, "icons8-wav-80.png");
            this.IconList.Images.SetKeyName(9, "icons8-zip-80.png");
            this.IconList.Images.SetKeyName(10, "pdf.png");
            this.IconList.Images.SetKeyName(11, "xls.png");
            this.IconList.Images.SetKeyName(12, "paper.png");
            this.IconList.Images.SetKeyName(13, "png.png");
            // 
            // FileNameLabel
            // 
            this.FileNameLabel.AutoSize = true;
            this.FileNameLabel.Location = new System.Drawing.Point(84, 75);
            this.FileNameLabel.Name = "FileNameLabel";
            this.FileNameLabel.Size = new System.Drawing.Size(16, 15);
            this.FileNameLabel.TabIndex = 6;
            this.FileNameLabel.Text = "...";
            this.FileNameLabel.Click += new System.EventHandler(this.label2_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 75);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(72, 15);
            this.label3.TabIndex = 7;
            this.label3.Text = "Имя файла:";
            this.label3.Click += new System.EventHandler(this.label3_Click);
            // 
            // FileTypeLabel
            // 
            this.FileTypeLabel.AutoSize = true;
            this.FileTypeLabel.Location = new System.Drawing.Point(80, 90);
            this.FileTypeLabel.Name = "FileTypeLabel";
            this.FileTypeLabel.Size = new System.Drawing.Size(16, 15);
            this.FileTypeLabel.TabIndex = 8;
            this.FileTypeLabel.Text = "...";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 90);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(68, 15);
            this.label5.TabIndex = 9;
            this.label5.Text = "Тип файла:";
            this.label5.Click += new System.EventHandler(this.label5_Click);
            // 
            // FileFindTextBox
            // 
            this.FileFindTextBox.Location = new System.Drawing.Point(538, 7);
            this.FileFindTextBox.Name = "FileFindTextBox";
            this.FileFindTextBox.Size = new System.Drawing.Size(181, 23);
            this.FileFindTextBox.TabIndex = 11;
            this.FileFindTextBox.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // FileFindButton
            // 
            this.FileFindButton.Location = new System.Drawing.Point(468, 7);
            this.FileFindButton.Name = "FileFindButton";
            this.FileFindButton.Size = new System.Drawing.Size(64, 22);
            this.FileFindButton.TabIndex = 12;
            this.FileFindButton.Text = "Найти:";
            this.FileFindButton.UseVisualStyleBackColor = true;
            this.FileFindButton.Click += new System.EventHandler(this.FileFindButton_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 105);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(88, 15);
            this.label1.TabIndex = 13;
            this.label1.Text = "Дата создания:";
            this.label1.Click += new System.EventHandler(this.label1_Click_2);
            // 
            // FileCreationTimeLabel
            // 
            this.FileCreationTimeLabel.AutoSize = true;
            this.FileCreationTimeLabel.Location = new System.Drawing.Point(102, 105);
            this.FileCreationTimeLabel.Name = "FileCreationTimeLabel";
            this.FileCreationTimeLabel.Size = new System.Drawing.Size(16, 15);
            this.FileCreationTimeLabel.TabIndex = 14;
            this.FileCreationTimeLabel.Text = "...";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 46);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(58, 15);
            this.label2.TabIndex = 15;
            this.label2.Text = "Свойства";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 447);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(96, 15);
            this.label4.TabIndex = 16;
            this.label4.Text = "Файлов в папке:";
            // 
            // FilesInDirLabel
            // 
            this.FilesInDirLabel.AutoSize = true;
            this.FilesInDirLabel.Location = new System.Drawing.Point(114, 447);
            this.FilesInDirLabel.Name = "FilesInDirLabel";
            this.FilesInDirLabel.Size = new System.Drawing.Size(16, 15);
            this.FilesInDirLabel.TabIndex = 17;
            this.FilesInDirLabel.Text = "...";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(12, 120);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(47, 15);
            this.label6.TabIndex = 18;
            this.label6.Text = "Размер";
            this.label6.Click += new System.EventHandler(this.label6_Click);
            // 
            // FileSizeLabel
            // 
            this.FileSizeLabel.AutoSize = true;
            this.FileSizeLabel.Location = new System.Drawing.Point(56, 120);
            this.FileSizeLabel.Name = "FileSizeLabel";
            this.FileSizeLabel.Size = new System.Drawing.Size(16, 15);
            this.FileSizeLabel.TabIndex = 19;
            this.FileSizeLabel.Text = "...";
            // 
            // Label7
            // 
            this.Label7.AutoSize = true;
            this.Label7.Location = new System.Drawing.Point(12, 470);
            this.Label7.Name = "Label7";
            this.Label7.Size = new System.Drawing.Size(87, 15);
            this.Label7.TabIndex = 13;
            this.Label7.Text = "Подкаталогов:";
            this.Label7.Click += new System.EventHandler(this.label1_Click_2);
            // 
            // SubDirLabel
            // 
            this.SubDirLabel.AutoSize = true;
            this.SubDirLabel.Location = new System.Drawing.Point(98, 470);
            this.SubDirLabel.Name = "SubDirLabel";
            this.SubDirLabel.Size = new System.Drawing.Size(16, 15);
            this.SubDirLabel.TabIndex = 17;
            this.SubDirLabel.Text = "...";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(903, 502);
            this.Controls.Add(this.FileSizeLabel);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.SubDirLabel);
            this.Controls.Add(this.FilesInDirLabel);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.FileCreationTimeLabel);
            this.Controls.Add(this.Label7);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.FileFindButton);
            this.Controls.Add(this.FileFindTextBox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.FileTypeLabel);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.FileNameLabel);
            this.Controls.Add(this.listView1);
            this.Controls.Add(this.FilePathTextBox);
            this.Controls.Add(this.PathLabel);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.BackButton);
            this.Name = "Form1";
            this.Text = "<<";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private Button BackButton;
        private Button button3;
        private Label PathLabel;
        private TextBox FilePathTextBox;
        private ListView listView1;
        private Label FileNameLabel;
        private Label label3;
        private Label FileTypeLabel;
        private Label label5;
        private ImageList IconList;
        private TextBox FileFindTextBox;
        private Button FileFindButton;
        private Label label1;
        private Label FileCreationTimeLabel;
        private Label label2;
        private Label label4;
        private Label FilesInDirLabel;
        private Label label6;
        private Label FileSizeLabel;
        private Label Label7;
        private Label SubDirLabel;
    }
}