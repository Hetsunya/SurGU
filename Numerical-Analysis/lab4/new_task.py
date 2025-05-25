import numpy as np

def read_augmented_matrix(filename):
    """Читает расширенную матрицу [A|b] из файла."""
    with open(filename, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    matrix = [list(map(float, line.split())) for line in lines[1:]]
    augmented_matrix = np.array(matrix)
    return augmented_matrix, n

def gaussian_elimination_with_partial_pivoting(A, n):
    """Решает СЛАУ методом Гаусса с выбором ведущего элемента, выводя матрицу после каждого изменения."""
    logs = []
    for k in range(n):
        # Постолбцовый выбор ведущего элемента
        max_row = max(range(k, n), key=lambda i: abs(A[i][k]))
        logs.append(
            f"Выбор ведущего элемента в столбце {k + 1}: max |A[{max_row + 1},{k + 1}]| = {abs(A[max_row][k]):.3f}")
        if A[max_row][k] == 0:
            logs.append("Система не имеет решений или имеет бесконечно много решений.")
            return None, logs

        # Перестановка строк
        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            logs.append(f"Перестановка строк {k + 1} и {max_row + 1}.")
            logs.append(f"Матрица после перестановки строк:\n{A}")

        # Прямой ход
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            A[i, k:] -= factor * A[k, k:]
            logs.append(f"Обновление строки {i + 1}: A[{i + 1}] -= ({factor:.3f}) * A[{k + 1}]")
            logs.append(f"Матрица после обновления строки {i + 1}:\n{A}")

    # Обратный ход
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        dot_product = np.dot(A[i, i + 1:n], x[i + 1:n])
        x[i] = (A[i, -1] - dot_product) / A[i, i]
        # logs.append(
        #     f"Вычисление x[{i + 1}]: x[{i + 1}] = {x[i]:.3f}, "
        #     f"A[i, -1] = {A[i, -1]:.3f}, dot_product = {dot_product:.3f}, A[i, i] = {A[i, i]:.3f}"
        # )

    return x, logs

def main():
    filename = "data.txt"
    try:
        augmented_matrix, n = read_augmented_matrix(filename)
        print("Исходная расширенная матрица [A|b]:")
        print(augmented_matrix)
        print("-" * 50)

        solution, logs = gaussian_elimination_with_partial_pivoting(augmented_matrix.copy(), n)

        for log in logs:
            print(log)

        if solution is not None:
            print("-" * 50)
            print(f"Решение СЛАУ: {solution}")
        else:
            print("Система не имеет решений или имеет бесконечно много решений.")
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
