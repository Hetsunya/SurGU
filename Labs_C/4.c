#include <math.h>
#include <stdio.h>

int main() {
  double n;
  double sum = 0;
  double h = 0.02;
  double old_I = 0;

  printf("Enter n: ");
  scanf("%lf", &n);

  do {
    old_I = sum;
    sum = 0;
    h /= 2.0;
    for (int i = 0; i < 1.6 / h; i++)
    // i * h + h / 2.0
    {
      if (i * h <= 0.6)
        sum += 1 / (1 + 25 * pow(i * h + h / 2.0, 2));
      else
        sum += ((i * h + h / 2.0 + 2 * pow(i * h + h / 2.0, 4)) *
                sin(pow(i * h + h / 2.0, 2)));
    }
    sum *= h;
  } while (fabs(sum - old_I) / 3.0 >= n);
  printf("%lf", sum);
  return 0;
}
