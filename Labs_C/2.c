#include <stdio.h>
#include <math.h>

int main()
{
  double x;
  printf("x -->");
  scanf("%lf", &x);
  if (x > 2)
  {
  double y = -log(x + 2.0) - log(x - 2.0);
      if(y >= 0 )
      {
      double z = sqrt(3.0 * y - y);
      printf("%lf\n", y);
      printf("%lf", z);
    }
    else
    {
      printf("x value is incorrect!");
    }
 }
 else
 {
   printf("x value is incorrect!");
 }
}
//2.1
