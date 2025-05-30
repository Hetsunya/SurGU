package main

import (
    "fmt"
    "math"
)

func main() {
    // 1. Ошибка точности IEEE754
    // Проблема: float32 теряет точность для больших чисел (123456789, 123456788).
    // Разность может быть неточной из-за ограниченной мантиссы (23 бита).
    fmt.Println("Test 1 - IEEE754 precision:")
    a1 := float32(123456789)
    b1 := float32(123456788)
    f1 := a1 - b1
    fmt.Printf("Result: %f (expected 1.0)\n\n", f1)
    // Ожидаемый результат: ~1.0 или неточное значение (например, 0.0).

    // 2. Ошибка приведения типов
    // Проблема: float32 теряет точность в дробной части числа 123456789.123457.
    // float64 сохраняет больше точности, и разность показывает ошибку.
    fmt.Println("Test 2 - Type casting:")
    a2 := float32(123456789.123457)
    b2 := float64(123456789.123457)
    f2 := float64(a2) - b2
    fmt.Printf("Result: %f (expected 0)\n\n", f2)
    // Ожидаемый результат: Не 0 (например, -0.000031).

    // 3. Ошибка промежуточных данных
    // Проблема: Числа 0.6000006 и 0.09999994 не представлены точно в float32.
    // Деление 1/3 в float32 также неточное, и вычитание не даёт 0.
    fmt.Println("Test 3 - Intermediate data:")
    fmt.Printf("0.6000006 + 0.09999994 = %f\n", 0.6000006+0.09999994)
    var a3, b3, c3 float32
    a3 = 1
    b3 = 3
    c3 = a3 / b3
    c3 = c3 - 1.0/3
    fmt.Printf("Result: %f (expected 0)\n\n", c3)
    // Ожидаемый результат: Не 0 (например, 0.700001 и ~1e-8).

    // 4. Ошибка сдвига мантиссы
    // Проблема: Многократное вычитание малого числа из большого в float32.
    // Накопление ошибок округления приводит к неточному результату.
    fmt.Println("Test 4 - Mantissa shift:")
    a4 := float32(0.00001)
    c4 := float32(300)
    for n := int64(1); n < 10000000; n++ {
        c4 = c4 - a4
    }
    fmt.Printf("Result: %f (expected 200)\n\n", c4)
    // Ожидаемый результат: Не 200 (например, 199.999985).

    // 5. Ошибка коммутативности
    // Проблема: Порядок операций влияет на результат из-за ошибок округления.
    // Вычитание и сложение малых чисел в float64 даёт разные результаты.
    fmt.Println("Test 5 - Commutativity:")
    variable_d := 100.0
    variable_u := 0.0
    for i := int64(0); i < 1000000000; i++ {
        variable_d -= 1.0 / 1000000000
        variable_u += 1.0 / 1000000000
    }
    fmt.Printf("variable_d: %f, variable_u: %f\n\n", variable_d, variable_u)
    // Ожидаемый результат: variable_d ~99.999999, variable_u ~1.0, но не точно.

    // 6. Ошибка циклов
    // Проблема: Сравнение float64 с 0 ненадёжно из-за ошибок округления.
    // Вычитание 0.1 из 0.2 не приводит к точному 0.
    fmt.Println("Test 6 - Loop processing:")
    x := 0.2
    found := false
    for i := 0; i < 40; i++ {
        x -= 0.1
        if math.Abs(x) < 1e-10 { // Используем epsilon вместо x == 0
            fmt.Println("ok")
            found = true
            break
        }
    }
    if !found {
        fmt.Println("not found")
    }
    // Ожидаемый результат: "not found", так как x не станет точно 0.
}
