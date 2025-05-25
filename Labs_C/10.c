#include <conio.h>
#include <malloc.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//Заполнение
int fill(int n, int m, int **a) {
  srand(time(NULL));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++) {
      a[i][j] = i * m + j + 1;
      printf("%d ", a[i][j]);
    }
}
//Вывод
void output(int n, int m, int **a) {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++)
      printf("%4d ", *(*(a + i) + j));

    printf("\n");
  }
}
//Сортировка
void sort(int n, int m, int **a, int r) {

  // for (int i = 0; i < r; i++)
  //   for (int j = 0; j < r; j++)
  //     if (a[i][0] > a[j][0]) {
  //       // if ((a[i][0] || a[j][0]) > 100)
  //       //  printf("%d --- %d\n", i, j);
  //       for (int k = 0; k < n; k++) {
  //         int t = a[i][k];
  //         a[i][k] = a[j][k];
  //         a[j][k] = t;
  //       }
  //     }
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
      if (a[i][0] > a[j][0])
        for (int k = 0; k < m; k++) {
          int t = a[i][k];
          a[i][k] = a[j][k];
          a[j][k] = t;
        }
}// Если n>m или m<n на >= 2 то пиздец

int main() {
  int n, m;
  printf("rows -> ");
  scanf("%d", &n);
  int r = n;
  printf("columns -> ");
  scanf("%d", &m);

  int **a = (int **)malloc(n * sizeof(int *));
  if (!a) {
    printf(" Memory allocation error ! \n ");
    exit(EXIT_FAILURE);
  }

  for (int i = 0; i < n; i++)
    a[i] = malloc(m * sizeof(int));

  fill(n, m, a);
  printf("\nMatrix before sorting:\n");
  output(n, m, a);
  sort(n, m, a, r);
  printf("Matrix after sorting:\n");
  output(n, m, a);

  for (int i = 0; i < n; i++)
    free(a[i]);

  free(a);
  return 0;
}

// *(*(arr + i) + j) = 5; /*eq. arr[i][j] = 5 */

// II способ требует использования двухуровневых указателей:
// int **a = (int **)malloc(n * sizeof(int *));
// if (!a) {
//   printf(" Memory allocation error !\ n ");
//   exit(EXIT_FAILURE);
// }
//
// int i, j;
// for (i = 0; i < n; i++)
//   p[i] = malloc(m * sizeof(int));
// for (i = 0; i < n; i++)
//   for (j = 0; j < m; j++)
//     a[i][j] = i * m + j + 1;
//
// for (i = 0; i < n; i++)
//   free(a[i]);
// free(a);

// int **p = (int **)malloc(m * sizeof(int *));
// for (int i = 0; i < m; i++)
//   p[i] = (int *)malloc(n * sizeof(int *));
// m - число строк
// n - число столбцов
