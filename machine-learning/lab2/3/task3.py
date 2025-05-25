import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_3d_graph(x1, x2, y, title, color='b'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, x2, y, c=color, marker='o')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    plt.title(title)
    plt.show()

n = 100
x1 = list(range(1, n+1))
x2 = list(range(1, n+1))

data = np.full((n, n), np.nan)

for i in range(n):
    x1_val = x1[i]
    x2_val = x2[i]
    if x1_val == x2_val:  # Только для x1 = x2
        data[i, i] = 6 * x1_val + 5 * x2_val 

df = pd.DataFrame(data, index=x1, columns=x2)
df.index.name = 'x1'
df.columns.name = 'x2'

df.to_excel('data.xlsx')

diag_x1 = []
diag_x2 = []
diag_y = []
for i in range(n):
    x1_val = x1[i]
    x2_val = x2[i]
    if x1_val == x2_val:
        y_val = 6 * x1_val + 5 * x2_val
        diag_x1.append(x1_val)
        diag_x2.append(x2_val)
        diag_y.append(y_val)

plot_3d_graph(diag_x1, diag_x2, diag_y, '3D график без шума', color='b')

noise = np.random.uniform(0.01, 0.1, size=len(diag_y))
diag_y_noisy = [y + n for y, n in zip(diag_y, noise)]

plot_3d_graph(diag_x1, diag_x2, diag_y_noisy, '3D график с шумом', color='r')

df_csv = pd.DataFrame({'x1': diag_x1, 'x2': diag_x2, 'y': diag_y_noisy})
df_csv.to_csv('data.csv', index=False, sep=',')