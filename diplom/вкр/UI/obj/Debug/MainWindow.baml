   M S B A M L   `   `   `  ����=  9UI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=nullclr-namespace:UIUI  5   	       UI.MainWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   "localclr-namespace:UI     5   	     � Title$[  UМультимодальная система распознавания эмоций��5   	   $	��600��6>   $
��1000��6K   .��5	      �  � ColumnDefinitions 5   
   �� 5      $	��200 �6   �� 5      $��* �6   �� 5      $	��300 �6    � RowDefinitions 5   
   �� 5      $
��Auto �6   �� 5      $��* �6   �� 5      $
��Auto �6   .+�5   
   �� $��0��6   $��3��6$   $)��#Анализ эмоций для HR��68   $��20(�6T   $
��Bold"�6b   $��10q�5      $��Center=�6    �� 5!   
   $��1��6   $��0��6"   $��10q�62   .+�5"      �� $��Настройки��6   $��16(�6)   $
��Bold"�67   $��0,0,0,10q�6I   �� 5#      $$��Источник данных:��6   $��0,0,0,5q�60   �� 5$      .@�5%      �� .��6   Камера6'   �� 5&      .��6   Микрофон6)   �� 5'      .��6   
Файл6%   5(      �� 5)      $&�� Категории эмоций:��6   $��0,10,0,5q�61   �� 5*      $��Радость��6    d� 	IsChecked$
 TrueY�6)   $	��0,2q�6:   �� 5+      $��Грусть��6   $
 TrueY�6(   $	��0,2q�69   �� 5,      $��Гнев��6   $
 TrueY�6&   $	��0,2q�67   �� 5-      $��Сценарий:��6   $��0,10,0,5q�6)   �� 5.      .@�5/      �� .��6   Собеседование6.   �� 50      .��6   Мониторинг6+   51      �� 52      $!��Запуск анализа��6   $��0,20,0,0q�6.   $��5q�6@   53      � 56   
   $��1��6   $��1��6   $��10q�6,    57      �� 58      $��* �6    �� 59      $��* �6    .+�5<      �� $��0��6   
�������$��1q�65   $��0,0,0,10q�6I   ._�5=      � .+�5>      �� 
�������6    �� 5@      $��Видеопоток��6    $��Center=�62   $��Center=�6O   $��14(�6j   �� 5A      $��Радость, 85%��6    
������� J� Opacity$	 0.8Q�6G   $��Right=�5B       $��Bottom=�6<   $��5q�6W   5C      5D      �� 5F      $��1��6   
�������$��1q�65   ._�5G      � .+�5H      �� 
����ح�6    �� 5J      $H��BГрафик эмоций (Радость: 60%, Грусть: 20%)��6    $��Center=�5K       $��Center=�6=   $��14(�6X   5L      5M      5N      �� 5Q   
   $��1��6   $��2��6"   $��10q�62   .+�5S      �� $��Уведомления��6   $��16(�6+   $
��Bold"�69   $��0,0,0,10q�6K   �� 5T      
���  ��$��1q�6'   $��0,0,0,10q�6;   $	��100��6M   ._�5U      �� $2��,Высокий уровень стресса��6   $��5q�6;   
���  ��6F   5V      �� 5X      $��Статистика��6   $��16(�6*   $
��Bold"�68   $��0,0,0,10q�6J   &   System.Windows.Controls.DataGrid  5Y         AutoGenerateColumns .  $	��150��63   $��0,0,0,10q�6@      Columns 5Z      0  *System.Windows.Controls.DataGridTextColumn  5[      ,  &System.Windows.Controls.DataGridColumn   Header$ Эмоция��6)      Width5  /System.Windows.Controls.DataGridLengthConverter$ * 6U   1  +System.Windows.Controls.DataGridBoundColumn	   Binding	 69   �� *	Emotion+6U     5\      $ Вероятность��6)   $ * 6^   	 6>   �� *Probability+6^   @�5^         UI.EmotionItem  5_      
   Emotion$
 Радость��6(      Probability$	 60%��6:     5`      $
 Грусть��6(   $	 20%��69     5a      $
 Нейтральное��6(   $	 20%��6>   5c      �� 5d      $��Экспорт в PDF/CSV��6   $��5q�61   5e      �� 5h   
   $��2��6   $��0��6"   $��3��62    �� Orientation$ 
Horizontal=�6F   $��Center=�5i      $��10q�62   .+�5j      �� $��
Пауза��6   $��5q�6%   $��5q�61   �� 5k      $��Возобновить��6   $��5q�6+   $��5q�67   �� 5l      $%��Сохранить данные��6   $��5q�60   $��5q�6<   �� 5m      $)��#Сформировать отчёт��6   $��5q�62   $��5q�6>   5n      5o      5p      