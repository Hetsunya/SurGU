// Задания для самостоятельного выполнения
// Добавить в код своего варианта лабораторной работы №11 функции
// сохранения данных в файл перед
// завершением работы программы и их загрузки из файла при старте программы, для
// обеспечения хранения данных между запусками. Требования и ограничения
// Предусмотреть возможноть просмотра всего списка, добавления и удаления
// записей. Необходимые операции с записями реализовать в виде отдельных
// функций Написать программу, реализующую
// считывание данных с клавиатуры, их
// обработку и вывод на экран результатов
// запроса согласно вашему варианту. Требования и ограничения Предусмотреть
// возможноть просмотра всего списка, добавления и удаления записей. Необходимые
// операции с записями
// реализовать в виде отдельных функций .
// Междугородние автобусы. Номер автобуса, пункты и время отправления и
// прибытия. Получить данные об автобусах, следующих в заданный город.

//////РАБОЧАЯ ВЕРСИЯ БЕЗ FLOAT

#include <conio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_SIZE 15

int count = 0;

typedef struct buses bus;

struct buses {
  int number;           // номер автобуса
  char destination[15]; // пункт назначения
  struct tm time;
  float dep_time;       // departure time - время отбытия
  float arr_time;       // arrival time - время прибытия
  // char dep_time[15];       // departure time - время отбытия
  // char arr_time[15];
} buses;
// struct buses bus[10];

int input(struct buses *, int);
void print(struct buses *, int);
int delet(struct buses *, int);
void find(struct buses *, int);

// запись структуры в файл
void save(FILE *f, struct buses *bus, int count) {
  for (int i = 0; i < count; i++)
    fprintf(f, "%d|%s|%f|%f\n", bus[i].number, bus[i].destination,
            bus[i].dep_time, bus[i].arr_time);
}

// Получение записей с файла
void load(FILE *f, struct buses bus[]) {
  char str[255];
  char *istr;

while (fgets(str, 256, f) != NULL){
    istr = strtok(str, "|");
    // sprintf(bus[count].number, "%d", istr);
    bus[count].number = atoi(istr);

    istr = strtok(NULL, "|");
    sprintf(bus[count].destination, "%s", istr);

    istr = strtok(NULL, "|");
    // sprintf(bus[count].dep_time, "%f", istr);
    bus[count].dep_time = atoi(istr);
    // fscanf(f, "%f", &bus[count].dep_time);

    istr = strtok(NULL, "|");
    // istr[strlen(istr) - 1] = 0;
    bus[count].arr_time = atoi(istr);
    // sprintf(bus[count].arr_time, "%f", istr);
    // fscanf(f, "%f", &bus[count].arr_time);

    count++;
  }
}

int main() {

  // struct buses bus[100] = {1, "Surgut", 15.00, 23.40};
  struct buses bus[100];
  // Получение предыдущих данных
  FILE *file = fopen("12.txt", "r");
  load(file, bus);
  fclose(file);

  char c;
  int k = 0;

  // struct buses bus[MAX_SIZE] = {1, "Surgut", 15.00, 23.40};
  while (1) {
    printf("\n1. Enter bus data.\n");
    printf("2. Display a list of buses.\n");
    printf("3. Delete bus data.\n");
    printf("4. Get data about buses going to a given city.\n");
    // printf("5 to load the database from a file.\n");
    // printf("6 to save the database to a file.\n");
    printf("7. Exit.\n");
    c = _getch();
    switch (c) {
    case '1':
      system("cls");
      k = input(bus, count);
      break;
    case '2':
      system("cls");
      print(bus, count);
      break;
    case '3':
      // system("cls");
      delet(bus, count);
      break;
    case '4':
      system("cls");
      find(bus, count);
      break;
    case '5':
      goto a;
      break;
    default:
      system("cls");
      printf("\nthe menu item is selected incorrectly!\n\n");
    }
  }
a:
  file = fopen("12.txt", "w");
  save(file, bus, k);
  fclose(file);
  return 0;
}
//Вывод информации о существующих
void print(struct buses bus[], int count) {
  if (!count)
    printf("array empty\n");
  else
    for (int i = 0; i < count; i++) {
      char d_time[15];
      char a_time[15];
      strftime(d_time, 15, "%H.%M", &bus[i].time);
      strftime(a_time, 15, "%H.%M", &bus[i].time);
      printf("[%d]Bus number: %d, Destination: %s, Departure time: %s, Arrival time %s\n",i + 1, bus[i].number, bus[i].destination, a_time, d_time);
    }
}
//Добавление
int input(struct buses *bus, int count) {
    printf("\nEnter the bus data separated by a space - number, destination, "
           "Departure time, Arrival time \n");
    for (int i = count; i < count + 1; i++) {
      scanf("%d %s %f %f", &bus[i].number, bus[i].destination, &bus[i].dep_time,
            &bus[i].arr_time);
    }
    count++;
  // if (!count) {
  //   do {
  //     printf("Enter the number of buses [1-100]: ");
  //     scanf("%d", &count);
  //   } while (count < 1 || count > 100);
  //
  //   printf("\nEnter the bus data separated by a space - number, destination, "
  //          "Departure time, Arrival time \n");
  //   for (int i = count; i < count; i++) {
  //     scanf("%d %s %f %f", &bus[i].number, bus[i].destination, &bus[i].dep_time,
  //           &bus[i].arr_time);
  //   }
  //
  // } else {
  //   for (int i = count; i > -1; i--)
  //     bus[i + 1] = bus[i];
  //   printf("\nEnter the bus data separated by a space - number, destination, "
  //          "Departure time, Arrival time \n");
  //   scanf("%d %s %f %f", &bus[0].number, bus[0].destination, &bus[0].dep_time,
  //         &bus[0].arr_time);
  //   count = count + 1;
  // }
  return count;
}

//Удаление
int delet(struct buses *bus, int count) {
  if (count) {
    int i, num;

    printf("Type index number of the bus you want to delete: ");
    scanf("%d", &num);

    for (i = num; i < count + 1; ++i)
      bus[i - 1] = bus[i];

    --count;
    if (count == 0) {
      printf("The array is empty!\n");
      count = 0;
    }
  } else {
    system("cls");
    printf("The array is empty!\n");
  }
  return count;
}
//Поиск
void find(struct buses *bus, int count) {
  char c[15];
  int temp = 0;
  printf("Enter city\n");
  scanf("%s", c);
  for (int i = 0; i < count; i++) {
    // if (bus[i].destination == c)
    if (!strcmp(bus[i].destination, c)) {
      printf("[%d]Bus number: %d, Destination: %s, Departure time: %0.2f, "
             "Arrival "
             "time %0.2f\n",
             i + 1, bus[i].number, bus[i].destination, bus[i].dep_time,
             bus[i].arr_time);
      temp = temp + 1;
    }
  }
  if (!temp)
    printf("There are no flights to this city\n ");
}
