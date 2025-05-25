#include <stdio.h>

int main(int argc, char const *argv[]) {
  char c;
  while (1) {
    c = getchar();
    if (c == 224) {
      c = getchar();
      if(c == 79) return 0;
    }
  }
  return 0;
}
