// struct tm {
//    int tm_sec;   // seconds of minutes from 0 to 61
//    int tm_min;   // minutes of hour from 0 to 59
//    int tm_hour;  // hours of day from 0 to 24
//    int tm_mday;  // day of month from 1 to 317
//    int tm_mon;   // month of year from 0 to 11
//    int tm_year;  // year since 1900
//    int tm_wday;  // days since sunday
//    int tm_yday;  // days since January 1st
//    int tm_isdst; // hours of daylight savings time
// }
// #include <conio.h>
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
  float dep_time;       // departure time - время отбытия
  float arr_time;       // arrival time - время прибытия
  struct tm time_dep;
  struct tm time_arr;
} buses;

int input(struct buses *);
void print(struct buses *);
void delet(struct buses *);
void find(struct buses *);

// Игнорирование символов
void flush_input(void) {
  char c;
  while (scanf("%c", &c) == 1 && c != '\n')
    ;
}

// запись структуры в файл
void save(FILE *f, struct buses *bus) {
  for (int i = 0; i < count; i++)
    fprintf(f, "%d|%s|%d|%d|%d|%d\n", bus[i].number, bus[i].destination,
            bus[i].time_dep.tm_hour, bus[i].time_dep.tm_min,
            bus[i].time_arr.tm_hour, bus[i].time_arr.tm_min);
}

// Получение записей с файла
void load(FILE *f, struct buses *bus) {
  char str[255];
  char *istr;
  while (fgets(str, 256, f) != NULL) {
    istr = strtok(str, "|");
    bus[count].number = atoi(istr);

    istr = strtok(NULL, "|");
    sprintf(bus[count].destination, "%s", istr);

    istr = strtok(NULL, "|");
    bus[count].time_dep.tm_hour = atoi(istr);

    istr = strtok(NULL, "|");
    bus[count].time_dep.tm_min = atoi(istr);

    istr = strtok(NULL, "|");
    bus[count].time_arr.tm_hour = atoi(istr);

    istr = strtok(NULL, "|");
    bus[count].time_arr.tm_min = atoi(istr);

    count++;
  }
}

int main() {
  struct buses bus[100];
  FILE *file = fopen("12.txt", "r");
  int n;
  char c;

  while (1) {
    printf("\n1. Enter bus data.\n");
    printf("2. Display a list of buses.\n");
    printf("3. Delete bus data.\n");
    printf("4. Get data about buses going to a given city.\n");
    printf("5 to load the database from a file.\n");
    printf("6 to save the database to a file.\n");
    printf("7. Exit.\n");
    // c = getchar();
    // Получение запроса
    printf("--> ");
    scanf("%d", &n);
    if (n == 1) {
      // system("cls");
      system("clear");
      int k = input(bus);
    } else if (n == 2) {
      // system("cls");
      system("clear");
      print(bus);
    } else if (n == 3)

      delet(bus);

    else if (n == 4) {
      // system("cls");
      system("clear");
      find(bus);
    } else if (n == 5) {
      // system("cls");
      system("clear");
      load(file, bus);
      fclose(file);
    } else if (n == 6) {
      // system("cls");
      system("clear");
      file = fopen("12.txt", "w");
      save(file, bus);
      fclose(file);
    } else if (n == 7)

      return 0;
  }
}
//Добавление
int input(struct buses *bus) {
  printf("\nEnter the bus data separated by a space - number, destination \n");
  for (int i = count; i < count + 1; i++) {
    scanf("%d %s", &bus[i].number, bus[i].destination);

    printf("d.d\n");
    printf("Departure time -->");
    int hour, min;
  a:
    scanf("%d.%d", &hour, &min);
    if ((24 < hour) || (hour < 0) || (59 < min) || (min < 0)) {
      printf("Wrong time.\n Try again\n");
      printf("Departure time -->");
      goto a;
    }
    bus[i].time_dep.tm_hour = hour;
    bus[i].time_dep.tm_min = min;
  b:
    printf("Arrival time -->");
    scanf("%d.%d", &hour, &min);
    if ((24 < hour) || (hour < 0) || (59 < min) || (min < 0)) {
      printf("Wrong time.\nTry again\n");
      printf("Arrival time -->");
      goto b;
    }
    bus[i].time_arr.tm_hour = hour;
    bus[i].time_arr.tm_min = min;
  }
  count++;
}

//Вывод информации о существующих
void print(struct buses bus[]) {
  if (!count)
    printf("array empty\n");
  else
    for (int i = 0; i < count; i++) {
      char d_time[15];
      char a_time[15];
      strftime(d_time, 15, "%H.%M", &bus[i].time_dep);
      strftime(a_time, 15, "%H.%M", &bus[i].time_arr);
      printf("[%d]Bus number: %d, Destination: %s, Departure time: %s, Arrival "
             "time %s\n",
             i + 1, bus[i].number, bus[i].destination,
             // bus[i].dep_time, bus[i].arr_time);
             d_time, a_time);
    }
}

//Удаление
void delet(struct buses *bus) {
  if (count) {
    int i, num;

    printf("Type index number of the bus you want to delete: ");
    scanf("%d", &num);

    for (i = num; i < count + 1; ++i)
      bus[i - 1] = bus[i];

    --count;
  } else {
    system("cls");
    printf("The array is empty!\n");
  }
}
//Поиск
void find(struct buses *bus) {
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
