#include <stdio.h>

int main()
{
  float c1, c2 , c3, sum, d, r;
  int s1, s2;
  int max;
  printf("c1 -->");
  scanf("%f", &c1);
  printf("c2 -->");
  scanf("%f", &c2);
  printf("c3 -->");
  scanf("%f", &c3);
  //printf("%f\n%f\n%f\n", c1, c2, c3);
  if(c1>c2 && c1>c3){
    max = (float)c1;
    s1 = 2;
    s2 = 3;
  }else if (c2>c3 && c2>c1){
      s1 = 1;
      max = (float)c2;
      s2 = 3;
   }else{
        s1 = 1;
        s2 = 2;
        max = (float)c3;
      }

  sum = s1 + s2;
  r = max - sum;
  d = sum / max;

  if(max%3 == 0){
    printf("%f\n", r);
  }
  else
  printf("%f\n", d);
  //printf("%f\n%f\n%f\n", sum, d, r);


    // вывести разность r, если r / 3 == 0 и sum / max
  return 0;
}
