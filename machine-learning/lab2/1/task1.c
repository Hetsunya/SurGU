#include "stdio.h"

int main(int argc, char *argv[])
{
    // 1. Ошибка точности IEEE754
    printf("Test 1 - IEEE754 precision:\n");
    float a1 = 123456789;
    float b1 = 123456788;
    float f1 = a1 - b1;
    printf("Result: %f (expected 1.0)\n\n", f1);

    // 2. Ошибка приведения типов
    printf("Test 2 - Type casting:\n");
    float a2 = 123456789.123457;
    double b2 = 123456789.123457;
    double f2 = a2 - b2;
    printf("Result: %f (expected 0)\n\n", f2);

    // 3. Ошибка промежуточных данных
    printf("Test 3 - Intermediate data:\n");
    printf("0.6000006 + 0.09999994 = %f\n", 0.6000006 + 0.09999994);
    float a3, b3, c3;
    a3 = 1;
    b3 = 3;
    c3 = a3 / b3;
    c3 = c3 - 1.0f/3;
    printf("Result: %f (expected 0)\n\n", c3);

    // 4. Ошибка сдвига мантиссы
    printf("Test 4 - Mantissa shift:\n");
    float a4 = 0.00001;
    float c4 = 300;
    long n;
    for (n = 1; n < 10000000; n++)
        c4 = c4 - a4;
    printf("Result: %f (expected 200)\n\n", c4);

    // 5. Ошибка коммутативности (переписано для C)
    printf("Test 5 - Commutativity:\n");
    double variable_d = 100;
    double variable_u = 0;
    for (long i = 0; i < 1000000000; i++) {
        variable_d -= 1.0/1000000000;
        variable_u += 1.0/1000000000;
    }
    printf("variable_d: %f, variable_u: %f\n\n", variable_d, variable_u);

    // 6. Ошибка циклов (переписано для C)
    printf("Test 6 - Loop processing:\n");
    double x = 0.2;
    int found = 0;
    for (int i = 0; i < 40; i++) {
        x -= 0.1;
        if (x == 0) {
            printf("ok\n");
            found = 1;
            break;
        }
    }
    if (!found) printf("not found\n");

    return 0;
}