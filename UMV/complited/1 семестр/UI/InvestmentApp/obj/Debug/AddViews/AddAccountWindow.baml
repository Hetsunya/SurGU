   M S B A M L   `   `   `  ����  InvestmentApp$    InvestmentApp.AddAccountWindow   5   	   R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	     � Title$  Добавить счёт��5   	   $	��250��6   $	��400��6,   .��5      � $��10q�6    � RowDefinitions 5   
   �� 5      $
��Auto �6   �� 5      $
��Auto �6   �� 5	      $
��Auto �6   �� 5
      $��* �6   .+�5   
   �� $��Клиент:��6   $��0��6"   �� 5   
   -   5         ��Name$ ClientComboBox��5      $��0��6+   $��	100,0,0,5q�68    �� DisplayMemberPath$ FullName��6K    �� SelectedValuePath$ ClientId��6h   �� 5   
   $��Тип счёта:��6   $��1��6%   �� 5   
   -   5        $ AccountTypeComboBox��5      $��1��60   $��	100,0,0,5q�6=   .@�5      �� $��Брокерский��6   �� 5      $��ИИС��6   �� 5      $ ��Доверительный��6   5      �� 5   
   $ ��Дата открытия:��6   $��2��6)   (  "System.Windows.Controls.DatePicker  5   
   -   5          Name$ OpenDatePicker��5      $��2��6-   $��	100,0,0,5q�6:   �� 5   
   $��3��6    �� Orientation$ 
Horizontal=�6"   $��Right=�6;   $��0,10,0,0q�6W   .+�5      �� -   5        $��Сохранить��5      $��80��6<   $��0,0,10,0q�6G   �� 5      -   5        $��Отмена��5      $��80��6;   5      5      5      