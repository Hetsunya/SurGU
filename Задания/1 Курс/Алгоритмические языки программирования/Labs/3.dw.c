#include <stdio.h>
#include <math.h>

int main()
{
  float x = 0;
  float f;

  printf("x        f(x)\n");
  printf("--------------\n");

  do
  {
    if (x >= 0 && x <= 0.6)
    {
      f = 1 / (1 + 25 * pow(x, 2));
    }

    if (x >= 0.6 && x <= 1.6)
    {
      f = (x + 2 * pow(x, 2))*pow(sin(x), 2);
    }

    printf("%0.1f        %0.1f\n",x, f);

    f = 0;
    x = x + 0.1;
  } while (x <= 1.7);

  return 0;
}
