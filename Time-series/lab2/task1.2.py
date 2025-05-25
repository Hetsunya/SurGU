import matplotlib.pyplot as plt
import numpy as np

def step_signal(x, a, b):
    return np.where((a <= x) & (x < b), 1, 0)

x = np.arange(-1, 3, 0.01)
f_signal = step_signal(x, 0, 1)
g_signal = step_signal(x, 0, 1)
conv_result = np.convolve(f_signal, g_signal, mode='full')[:len(x)]

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(x, f_signal, label='f(x)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(x, g_signal, label='g(x)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(x, conv_result, label='(f * g)(x)')
plt.legend()

plt.tight_layout()
plt.show()
