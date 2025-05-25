#include <conio.h>
#include <ctype.h>
#include <stdio.h>

// int mygetch() {
//   char c;
//   while (1) {
//     /* code */
//   char c = getchar();
//
//   if (isalnum(c)) {
//     printf("%d", (int)c);
//   }
//   if (iscntrl(c))
//      if ((c = getchar()) != '\n') break;
//     return 0;
//   printf("%c", isprint(c));
// };
//   // isdigit(c);
//   return c;
// }

int main() {
  printf("Enter Insert for exit\n");
  // char c = mygetch();
    char c;
    while (1) {
    char c = getchar();

    if (isalnum(c)) {
      printf("%d", (int)c);
    }
    // if (iscntrl(c))
    //    if ((c = getchar()) != '\n') break;
    //   return 0;
    printf("%d", c);
    printf("\n");
  };
    // isdigit(c);
  return 0;
}
