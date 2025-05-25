#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int n, max = -1099, min1, sum, min2, g, i, i;
void fill(int n, int a[]) {
  for (i = 0; i < n; i++)
    a[i] = rand() % 101 - 50;
}

void find(int n) {
  int A[n];
  int t1 = 0, t2 = 0;
  fill(n, A);
  // min1 = A[0];
  // min2 = A[1];
  min1 = 1000;
  min2 = 1000;

  //Поиск max
  for (i = 0; i < n; i++) {
    sum = A[i] + A[i + 1];
    if (i == n - 1)
      sum = A[i] + A[i - 1];

    if (sum > max)
      max = sum;
  }

  printf("\nmax ---> %d\n", max);

  //Поиск min
  for (int i = 0; i < n; i++) {
    printf("%4d", A[i]);
    if (A[i] <= min1) {
      min2 = min1;
      min1 = A[i];

      t2 = t1;
      t1 = i;
      printf("<--");
    } else if (A[i] <= min2) {
      min2 = A[i];

      t2 = i;
      printf("<--");
    }
  }
  printf("\nmin1 ---> %d", min1);
  printf("\nmin2 ---> %d\n", min2);

  A[t1] = A[t1] + max;
  A[t2] = A[t2] + max;

  for (int i = 0; i < n; i++)
    printf("%4d", A[i]);
}

int main() {
  srand(time(NULL));
  printf(" n ---> ");
  scanf("%d", &n);
  find(n);


  return 0;
}
//  Найти два подряд идущих элемента в массиве целых чисел, сумма которых
//  максимальна и прибавить эту сумму к двум минимумам этого массива.
