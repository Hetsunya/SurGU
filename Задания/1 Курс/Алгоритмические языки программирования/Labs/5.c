#include <math.h>
#include <stdio.h>
#include <stdlib.h>
void rec(int n) {
  int x;
  x = n % 10;
  if ((((n / 10) == 0)) && ((n % 10) == 0))
    return;
  printf("%d", x);
  if (n)
    rec(n / 10);
  else
    return;
}

void cy(int n) {
  int a, x, n1;
  n1 = n;
  for (int i = 0; i < n1; i++) {
    if (n == 0)
      break;
    if (n < 10) {
      printf("%d", n);
      n = n / 10;
    } else {
      printf("%d", n % 10);
      n = n / 10;
    }
  }
  return;
}

int main() {
  int n;
  printf("Num--->");
  scanf("%d", &n);
  printf("\n");
  printf("\n");

  printf("recursion:");
  rec(n);

  printf("\n");
  printf("\n");

  printf("cycle:");
  cy(n);
  return 0;
}
