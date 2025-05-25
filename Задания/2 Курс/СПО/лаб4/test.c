/* FILENAME : task_1_1.c */
/* Eugene V. Ogurtsov */
/* Last update : 23.05.2000 */
/* Физико-математический лицей № 30 */
/* Простейшая база данных.
/* Написать программу, которая позволяет оперировать
 * с базой данных учеников: добавлять нового ученика,
 * удалять ученика (по номеру), выводить на экран список
 * всех учеников, сохранять в файле и восстанавливать
 * из файла базу данных, упорядочивать учеников по фамилии.
 * В базе данных имеются поля: номер, фамилия, имя и возраст
 * ученика. Программа должна предоставлять возможность
 * выбора с помощью меню одной из перечисленной операций. */

#include <stdio.h>
#include <conio.h>
#include <string.h>

/* Структура для хранения информации про одного человека */
typedef struct tagITEM
{
  char Surname[20], Name[20];
  int Age;
} ITEM;

/* Массив максимум на 20 человек */
ITEM Men[20];

/* Количество занятых элементов в массиве */
int Number;

/* Функция для вывода всех элеиентов */
void Print( void )
{
  int i;

  printf(" N  Second              Name                  Age\n");
  for (i = 0; i < Number; i ++)
    printf("%2i. %-20s %-20s %3i\n", i + 1, Men[i].Surname,
           Men[i].Name, Men[i].Age);
} /* End of 'Print' function */

/* Функция для добавления элемента */
void Add( void )
{
  if (Number == 19)
  {
    fprintf(stderr, "HE CANNOT ADD\n");
    return;
  }

  printf("Second name > ");
  scanf("%s", Men[Number].Surname);
  printf("Name > ");
  scanf("%s", Men[Number].Name);
  printf("Age > ");
  scanf("%i", &Men[Number].Age);

  Number ++;
} /* End of 'Add' function */

/* Функция для удаления элемента */
void Del( void )
{
  int i;

  Print();
  printf("# element > ");
  scanf("%i", &i);
  if (i < 1 || i > Number)
  {
    fprintf(stderr, "Элемент с номером %i не существует\n", i);
    return;
  }

  for (i --; i < Number - 1; i ++)
    Men[i] = Men[i + 1];

  Number --;
} /* End of 'Del' function */

/* Функция для сохранения массива в файле */
void Save( void )
{
  FILE *F;
  int i;

  if ((F = fopen("task1.dat", "wt")) == NULL)
  {
    fprintf(stderr, "Невозможно открыть для записи файл 'task1.dta'\n");
    return;
  }

  fprintf(F, "%i\n", Number);
  for (i = 0; i < Number; i ++)
    fprintf(F, "%s\n%s\n%i\n", Men[i].Surname, Men[i].Name, Men[i].Age);

  fclose(F);
} /* End of 'Save' function */

/* Функция для чтения массива из файла */
void Load( void )
{
  FILE *F;
  int i;

  if ((F = fopen("task1.dat", "rt")) == NULL)
  {
    fprintf(stderr, "HE CANNOT OPEN 'task1.dta'\n");
    return;
  }

  fscanf(F, "%i", &Number);
  for (i = 0; i < Number; i ++)
    fscanf(F, "%s%s%i", Men[i].Surname, Men[i].Name, &Men[i].Age);

  fclose(F);
} /* End of 'Load' function */

/* Функция для упорядочивания массива по фамилии */
void Sort( void )
{
  int i, j;
  ITEM Temp;

  for (j = Number - 1; j > 0; j --)
    for (i = 0; i < j; i ++)
      if (strcmp(Men[i].Surname, Men[i + 1].Surname) > 0)
      {
        Temp = Men[i];
        Men[i] = Men[i + 1];
        Men[i + 1] = Temp;
      }
} /* End of 'Sort' function */

/* Вывод меню и чтение номера выбранного пункта */
int Menu( void )
{
  int c = 0;

  while ((c < '0' || c > '6') && c != 27)
  {
    printf("0 : Exit\n"
           "1 : Add\n"
           "2 : Save\n"
           "3 : Loae\n"
           "4 : Out\n"
           "5 : Sort\n"
           "6 : Del\n"
           ">");
    c = getch();
    printf("%c\n", c);
  }
  return c;
} /* End of 'Menu' function */

/* Основная функция */
void main( void )
{
  int Selection;

  Number = 0;
  while ((Selection = Menu()) != '0' && Selection != 27)
    switch (Selection)
    {
    case '1':
      Add();
      break;
    case '2':
      Save();
      break;
    case '3':
      Load();
      break;
    case '4':
      Print();
      break;
    case '5':
      Sort();
      break;
    case '6':
      Del();
      break;
    }
} /* End of 'main' function */

/* End of 'task_1_1.c' file */