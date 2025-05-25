// Написать программу, реализующую считывание данных с клавиатуры, их
// обработку и вывод на экран результатов
// запроса согласно вашему варианту. Требования и ограничения Предусмотреть
// возможноть просмотра всего списка, добавления и удаления записей. Необходимые
// операции с записями реализовать в виде отдельных
// функций . Междугородние автобусы. Номер
// автобуса, пункты и время отправления и прибытия. Получить данные об
// автобусах, следующих в заданный город.
#include <conio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

struct buses {
  int number;           // номер автобуса
  char destination[15]; // пункт назначения
  float dep_time;       // departure time - время отбытия
  float arr_time;       // arrival time - время прибытия
};
struct buses bus[100];

// int input(struct buses *, int, int);
int input(struct buses *, int);
void print(struct buses *, int);
int delet(struct buses *, int);
void find(struct buses *, int);

int main() {
  char c;
  int k = 0;
  // struct buses bus[100];

  while (1) {
    printf("\n1. Enter bus data.\n");
    printf("2. Display a list of buses.\n");
    printf("3. Delete bus data.\n");
    printf("4. Get data about buses going to a given city.\n");
    printf("5. Exit.\n");
    c = _getch();

    switch (c) {
    case '1':
      system("cls");
      k = input(bus, k);
      break;
    case '2':
      system("cls");
      print(bus, k);
      break;
    case '3':
      // system("cls");
      delet(bus, k);
      break;
    case '4':
      system("cls");
      find(bus, k);
      return 0;
      break;
    case '5':
      return 0;
      break;
      system("cls");
    default:
      system("cls");
      printf("\nthe menu item is selected incorrectly!\n\n");
    }
  }
  return 0;
}
//Вывод информации о существующих
void print(struct buses *bus, int count) {
  if (count) {
    for (int i = 0; i < count; i++) {
      if (bus[i].number <= 0)
        continue;
      printf(
          "[%d]Bus number: %d, Destination: %s, Departure time: %0.2f, Arrival "
          "time %0.2f\n",
          i + 1, bus[i].number, bus[i].destination, bus[i].dep_time,
          bus[i].arr_time);
    }
  } else
    printf("The array is empty!\n");
}
//Добавление
int input(struct buses *bus, int count) {
  if (!count) {
    do {
      printf("Enter the number of buses [1-100]: ");
      scanf("%d", &count);
    } while (count < 1 || count > 100);

    printf("\nEnter the bus data separated by a space - number, destination, "
           "Departure time, Arrival time \n");
    for (int i = 0; i < count; i++) {
    a:
      scanf("%d %s %f %f", &bus[i].number, bus[i].destination, &bus[i].dep_time,
            &bus[i].arr_time);
      if ( ((bus[i].arr_time || bus[i].dep_time ) < 0) || ((bus[i].arr_time || bus[i].dep_time) > 24.00) ) {
        printf("Incorrect time\n");
        goto a;
      }
    }
  } else {
    for (int i = count; i > -1; i--)
      bus[i + 1] = bus[i];
    printf("\nEnter the bus data separated by a space - number, destination, "
           "Departure time, Arrival time \n");
    scanf("%d %s %f %f", &bus[0].number, bus[0].destination, &bus[0].dep_time,
          &bus[0].arr_time);
    count++;

    // printf("\nEnter the bus data separated by a space - number, destination,
    // "
    //        "Departure time, Arrival time \n");
    // scanf("%d %s %f %f", &bus[count + 1].number, bus[count + 1].destination,
    //       &bus[count + 1].dep_time, &bus[count + 1].arr_time);
    // count = count + 1;
  }
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
  } else
    printf("The array is empty!\n");
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
      printf(
          "[%d]Bus number: %d, Destination: %s, Departure time: %0.2f, Arrival "
          "time %0.2f\n",
          i + 1, bus[i].number, bus[i].destination, bus[i].dep_time,
          bus[i].arr_time);
      temp = temp + 1;
    }
  }
  if (!temp)
    printf("There are no flights to this city\n ");
}
