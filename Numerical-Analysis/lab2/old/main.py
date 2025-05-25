import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from graph_library import GraphPlotter  # Импортируем библиотеку графиков
from simple_iteration import simple_iteration_method, plot_function_and_solution
from sympy import symbols, parse_expr

def extract_g_from_f(func_str):
    # Символьная переменная
    x = symbols('x')

    # Преобразуем строку функции в символьное выражение
    f_expr = parse_expr(func_str)

    # Найдём все слагаемые функции
    terms = f_expr.as_ordered_terms()

    # Ищем компонент, который не содержит -x (т.е. нашу g)
    g_expr = None
    for term in terms:
        if not term.has(x):
            continue
        # Проверяем, что это не линейная часть (например, -x)
        if term != -x:
            g_expr = term

    # Если нашли выражение для g(x), возвращаем его, иначе None
    if g_expr is not None:
        return g_expr
    else:
        raise ValueError("Не удалось найти подходящее выражение для g(x)")


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("График функции и Метод простых итераций")

        self.plotter = GraphPlotter()

        # Поля ввода для функции и диапазона
        self.create_input_fields()

        # Кнопки управления
        self.create_control_buttons()

        # Поле для графика
        self.create_plot_canvas()

        # Поле для ввода начального приближения
        self.init_label = tk.Label(root, text="Начальное приближение (x0):")
        self.init_label.pack()
        self.init_entry = tk.Entry(root)
        self.init_entry.pack()

        # Кнопка для запуска метода простых итераций
        self.iterate_button = tk.Button(root, text="Запустить метод", command=self.run_iteration)
        self.iterate_button.pack()

        # Обновляем график при запуске
        self.update_plot()

    def create_input_fields(self):
        self.function_label = tk.Label(self.root, text="Функция:")
        self.function_label.pack()
        self.function_entry = tk.Entry(self.root)
        self.function_entry.pack()
        self.function_entry.insert(0, self.plotter.function)

        self.start_label = tk.Label(self.root, text="Начало X:")
        self.start_label.pack()
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()
        self.start_entry.insert(0, str(self.plotter.start))

        self.end_label = tk.Label(self.root, text="Конец X:")
        self.end_label.pack()
        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack()
        self.end_entry.insert(0, str(self.plotter.end))

    def create_control_buttons(self):
        self.update_button = tk.Button(self.root, text="Обновить график", command=self.update_plot)
        self.update_button.pack()

        self.export_button = tk.Button(self.root, text="Экспортировать в файл", command=self.export_to_file)
        self.export_button.pack()

        self.import_button = tk.Button(self.root, text="Импортировать из файла", command=self.import_from_file)
        self.import_button.pack()

    def create_plot_canvas(self):
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Добавляем панель инструментов для интерактивности
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def update_plot(self):
        try:
            function = self.function_entry.get()
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())

            self.plotter.function = function
            self.plotter.start = start
            self.plotter.end = end

            if self.plotter.points and len(self.plotter.points) < 3:
                # Используем уже загруженные точки
                pass
            else:
                self.plotter.generate_data()

            self.ax.clear()
            self.plotter.plot(self.ax)
            self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.plotter.export_to_file(file_path)

    def import_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.plotter.import_from_file(file_path)
            # Обновляем поля ввода после импорта
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, self.plotter.function)
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, str(self.plotter.start))
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, str(self.plotter.end))
            self.update_plot()

    def run_iteration(self):
        try:
            # Получаем начальное приближение от пользователя
            x0 = float(self.init_entry.get())

            # Получаем функцию из поля ввода
            function_str = self.function_entry.get()

            # Преобразуем строку в символьное выражение
            from sympy import lambdify, symbols
            x_symbol = symbols('x')

            # Преобразуем символьную строку в функцию для вычислений
            g_expr = extract_g_from_f(function_str)  # Находим g(x)
            print(f"g_expr = {g_expr}")
            g_func = lambdify(x_symbol, g_expr, 'numpy')  # Преобразуем g(x) в вычисляемую функцию

            # Полная функция для графика
            f_func = lambdify(x_symbol, parse_expr(function_str), 'numpy')

            # Запускаем метод простых итераций для нахождения корня
            solution = simple_iteration_method(g_func, x0)

            if solution is not None:
                # Очищаем текущий график
                self.ax.clear()

                # Построение графика исходной функции f(x)
                self.plotter.plot(self.ax)  # Вызов отрисовки для полной функции (f)

                # Отметка на графике найденного решения
                self.ax.plot(solution, f_func(solution), 'ro', label=f"Найденный корень: x = {solution:.4f}")

                # Отображаем график
                self.ax.legend()
                self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обработке функции: {e}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
