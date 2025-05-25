import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, lambdify
import csv

class GraphPlotter:
    def __init__(self, function="cos(sqrt(abs(x))) - x", start=-10.0, end=10.0, step=0.0001):
        self.function = function
        self.start = start
        self.end = end
        self.step = step
        self.x_symbol = symbols('x')
        self.points = []

    def generate_data(self):
        try:
            expression = lambdify(self.x_symbol, self.function, 'numpy')
        except Exception as e:
            raise ValueError(f"Ошибка в функции: {e}")

        x_values = np.arange(self.start, self.end, self.step)
        y_values = expression(x_values)
        self.points = list(zip(x_values, y_values))
        return self.points

    def plot(self, ax=None):
        if not self.points:
            print("Нет данных для отображения.")
            return

        x, y = zip(*self.points)
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"График функции: {self.function}")
        ax.grid(True)

    def export_to_file(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            if self.function != "":
                writer.writerow([self.function, self.start, self.end])
            else:
                for point in self.points:
                    writer.writerow(point)
        print(f"Данные успешно сохранены в {file_path}")

    def import_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.points = []
            reader = csv.reader(file)
            header = next(reader)
            if len(header) == 3:
                print("мы в 3")
                self.function, self.start, self.end = header[0], float(header[1]), float(header[2])
                self.generate_data()
                print("Импортированные точки:", self.points[0])
            else:
                print("мы в 2")
                self.function = ""
                # Добавляем первую строку данных
                self.points.append((float(header[0]), float(header[1])))

                # Добавляем остальные строки данных
                for row in reader:
                    self.points.append((float(row[0]), float(row[1])))

                print("Импортированные точки:", self.points)

        print(f"Данные успешно импортированы из {file_path}")
