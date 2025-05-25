#include <ctype.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>


int mygetch()
{
    struct termios oldt, newt;
    int c;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    c = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return c;
}

int main()
{
    unsigned char a;
    for (;;)
    {
        a = mygetch();

        {
            if (a == 27)
            {
                a = mygetch();
                if (a == 91)
                {
                    a = mygetch();
                    if (a == 50)
                    {
                        printf("\x1B[31mЗакрой за мной дверь,\nЯ ухожу\x1B[0m\n");
                        return 0;
                    }
                    else
                    {
                        printf("\x1B[35mАбоба\x1B[0m ");
                        continue;
                    }
                }
                else
                {
                    printf("\x1B[35mАбоба\x1B[0m ");
                    continue;
                }
            }
            else
            {
                if (!((a >=48 && a <= 57) || (a >=65 && a <= 90) || (a >=97 && a <= 122)))
                    printf("\x1B[33m%c\x1B[0m ", a);
                else
                    printf("\x1B[32m%d\x1B[0m ", a);
            }
        }
    }
}
