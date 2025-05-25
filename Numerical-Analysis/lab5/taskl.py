import numpy as np


def read_augmented_matrix(filename):
    """Читает расширенную матрицу [A|b] из файла."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    matrix = [list(map(float, line.split())) for line in lines[1:]]
    augmented_matrix = np.array(matrix)
    return augmented_matrix, n

#проверка на диагонально преобладающей
def is_diagonally_dominant(A):
    for i in range(len(A)):
        if abs(A[i][i]) <= sum(abs(A[i][j]) for j in range(len(A)) if j != i):
            return False
    return True

def relaxation_method(A, b, n, omega=1.5, tol=1e-6, max_iter=1000):
    """
    Решает СЛАУ методом релаксации.
    :param A: матрица коэффициентов (n x n)
    :param b: вектор правых частей (n,)
    :param n: размерность системы
    :param omega: параметр релаксации
    :param tol: точность (когда изменение вектора решений становится меньше tol)
    :param max_iter: максимальное количество итераций
    :return: решение системы или None, если решение не сходится
    """
    # Инициализация начального приближения (вектора случайных значений)
    x = np.random.rand(n)

    # Список для логов
    logs = []

    for iteration in range(max_iter):
        x_new = np.copy(x)  # Создаем копию текущего решения для обновлений

        for i in range(n):
            # Вычисление нового значения для x_i по формуле метода релаксации
            sum1 = np.dot(A[i, :i], x[:i])  # Сумма по всем элементам до i
            sum2 = np.dot(A[i, i + 1:], x[i + 1:])  # Сумма по всем элементам после i
            x_new[i] = (1 - omega) * x[i] + omega * (b[i] - sum1 - sum2) / A[i, i]

        # Логирование текущего приближения
        logs.append(f"Итерация {iteration + 1}: {x_new}")

        # Проверка на сходимость
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            logs.append(f"Решение найдено после {iteration + 1} итераций.")
            return x_new, logs

        x = np.copy(x_new)  # Обновляем вектор x для следующей итерации

    logs.append("Метод не сошелся за максимальное количество итераций.")
    return None, logs


def validate_solution(A, b, x, tol=1e-6):
    """
    Проверяет, является ли найденное решение корректным.
    :param A: матрица коэффициентов
    :param b: вектор правых частей
    :param x: предполагаемое решение
    :param tol: допустимая погрешность
    """
    logs = []
    n = len(b)

    # Проверка каждого уравнения
    for i in range(n):
        left_side = np.dot(A[i], x)  # Левая часть уравнения
        right_side = b[i]  # Правая часть уравнения
        difference = abs(left_side - right_side)

        log = (f"Уравнение {i + 1}: "
               f"левая часть = {left_side:.6f}, "
               f"правая часть = {right_side:.6f}, "
               f"разница = {difference:.2e}")

        logs.append(log)

    return logs


def main():
    filename = "data_dom.txt"
    augmented_matrix, n = read_augmented_matrix(filename)
    A = augmented_matrix[:, :-1]  # Матрица коэффициентов A
    b = augmented_matrix[:, -1]  # Вектор правых частей b

    print("Исходная расширенная матрица [A|b]:")
    print(augmented_matrix)
    print("-" * 50)

    if is_diagonally_dominant(A):
        print("Матрица является диагонально преобладающей.")
    else:
        print("Матрица не является диагонально преобладающей.")

    solution, logs = relaxation_method(A, b, n, omega=1)

    for log in logs:
        print(log)

    if solution is not None:
        print("-" * 50)
        print(f"Решение СЛАУ: {solution}")

        # Проверка решения
        validation_logs = validate_solution(A, b, solution)
        for log in validation_logs:
            print(log)
    else:
        print("Система не имеет решения или не сошлась.")



if __name__ == "__main__":
    main()
