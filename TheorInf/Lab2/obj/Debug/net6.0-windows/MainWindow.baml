   M S B A M L   `   `   `  ����  Lab2    ShannonFanoApp.MainWindow   5   	   W SPresentationCore, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=6.0.2.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=6.0.2.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$A  ;Алгоритм Шеннона-Фано / Хаффмана��5   	   $	��600��5   	   $	��500��6   .��5      � .+�5   
   �� $E��?Введите сообщение для кодирования��6   $��16(�5	      $
��Bold"�6"   $��Center=�5
      $	��Top=�61   $��
10,10,10,0q�5      �� 5   
   -   5         ��Name$ MessageTextBox��5      $��Stretch=�5      $	��Top=�5      $��
10,40,10,0q�5      $��30��5      �� 5   
    �� Orientation$ 
Horizontal=�6   $
��Left=�6.   $	��Top=�6I   $��	10,80,0,0q�6a   .+�5      	� -   5         	�Name$ ShannonFanoRadioButton��5      $��Шеннон-Фано��6:    d� 	IsChecked$
 TrueY�6P   $��	10,0,10,0q�6a   	� 5      -   5        $ HuffmanRadioButton��5      $��Хаффман��66   5      �� 5   
   -   5        $��Кодировать��5      $
��Left=�5      $	��Top=�6,   $	��100��5      $��30��6   $��
10,120,0,0q�5      5      �� 5"   
   -   5         ��Name$ ResultTextBlock��5"      $E��?Результаты будут отображены здесь��5#      $��14(�5$      $
��Left=�5%      $	��Top=�5&      $��
300,78,0,0q�5'      �� 5*   
   -   5        $ AverageLengthTextBlock��5*      $*��$Средняя длина кода: ��5+      $��14(�5,      $
��Left=�5-      $	��Top=�5.      $��
10,201,0,0q�5/      �� 52   
   -   5        $ VarianceTextBlock��52      $��Дисперсия: ��53      $��14(�54      $
��Left=�55      $	��Top=�56      $��
22,169,0,0q�57      58      59      