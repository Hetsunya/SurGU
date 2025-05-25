import tkinter as tk
from tkinter import messagebox
from math import log
import numpy as np


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Operations")
        self.created_objects = []
        self.str_count = 0
        self.stlb_count = 0

        # Interface setup
        tk.Label(root, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_entry = tk.Entry(root)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        self.cols_entry = tk.Entry(root)
        self.cols_entry.grid(row=1, column=1, padx=5, pady=5)

        self.combo_var = tk.StringVar()
        self.combo_var.set("A")
        tk.OptionMenu(root, self.combo_var, "A", "B", "C").grid(row=2, column=0, columnspan=2, pady=5)

        self.create_btn = tk.Button(root, text="Create Matrix", command=self.create_matrix)
        self.create_btn.grid(row=3, column=0, columnspan=2, pady=5)

        self.calc_btn = tk.Button(root, text="Calculate", command=self.calculate)
        self.calc_btn.grid(row=4, column=0, columnspan=2, pady=5)
        self.calc_btn.config(state="disabled")

        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.grid(row=5, column=0, columnspan=2, pady=10)

    def create_matrix(self):
        # Clear existing widgets
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.created_objects.clear()

        try:
            self.str_count = int(self.rows_entry.get())
            self.stlb_count = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for rows or columns.")
            return

        for i in range(self.str_count):
            row = []
            for j in range(self.stlb_count):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.created_objects.append(row)

        if self.combo_var.get() == "A":
            for i in range(self.stlb_count):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=self.str_count, column=i, padx=2, pady=2)
                self.created_objects.append([entry])
        elif self.combo_var.get() == "B":
            for i in range(self.str_count):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=self.stlb_count, padx=2, pady=2)
                self.created_objects.append([entry])

        self.calc_btn.config(state="normal")

    def calculate(self):
        matrix = []
        try:
            for i in range(self.str_count):
                row = [float(entry.get()) for entry in self.created_objects[i]]
                matrix.append(row)
            matrix = np.array(matrix)

            if self.combo_var.get() == "A":
                ensemble = [float(entry[0].get()) for entry in self.created_objects[self.str_count:]]
                self.third_method(matrix, ensemble)
            elif self.combo_var.get() == "B":
                ensemble = [float(entry[0].get()) for entry in self.created_objects[self.str_count:]]
                self.first_method(matrix, ensemble)
            else:
                self.second_method(matrix)

        except ValueError:
            messagebox.showerror("Error", "Invalid input in the matrix.")

    def func(self, x):
        return -x * log(x, 2) if x > 0 else 0

    def second_method(self, matrix):
        A = matrix.sum(axis=0)
        B = matrix.sum(axis=1)
        h_A = round(sum(self.func(a) for a in A), 3)
        h_B = round(sum(self.func(b) for b in B), 3)

        # Display results
        messagebox.showinfo("Results", f"H(A): {h_A}\nH(B): {h_B}")

    def first_method(self, matrix, ensemble):
        h_A = round(sum(self.func(e) for e in ensemble), 3)
        p_ab = matrix * ensemble[:, np.newaxis]
        Z = p_ab.sum(axis=0)
        h_Z = round(sum(self.func(z) for z in Z), 3)

        # Display results
        messagebox.showinfo("Results", f"H(Z): {h_Z}\nH(A): {h_A}")

    def third_method(self, matrix, ensemble):
        h_A = round(sum(self.func(e) for e in ensemble), 3)
        p_ab = matrix * ensemble[np.newaxis, :]
        Z = p_ab.sum(axis=1)
        h_Z = round(sum(self.func(z) for z in Z), 3)

        # Display results
        messagebox.showinfo("Results", f"H(A): {h_A}\nH(Z): {h_Z}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
