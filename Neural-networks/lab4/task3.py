import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.utils import shuffle

radius = 10.0
x = np.linspace(-radius, radius, 2000)
y_positive = np.sqrt(radius**2 - x**2)
y_negative = -np.sqrt(radius**2 - x**2)
target = np.column_stack((y_positive, y_negative))

x_shuffled, target = shuffle(x, target, random_state=42)
split_index = int(0.8 * len(x))
train_x, test_x = x_shuffled[:split_index], x_shuffled[split_index:]
train_target, test_target = target[:split_index], target[split_index:]

model = Sequential()
model.add(Dense(16, input_dim=1, activation='tanh'))
model.add(Dense(128, activation='tanh'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error')

history = model.fit(train_x, train_target, epochs=15, batch_size=16)

train_loss = model.evaluate(train_x, train_target, verbose=0)
test_loss = model.evaluate(test_x, test_target, verbose=0)
print(f"Train MSE: {train_loss:.4f}")
print(f"Test MSE: {test_loss:.4f}")

predictions = model.predict(test_x, verbose=0)
pred_y_positive = predictions[:, 0]
pred_y_negative = predictions[:, 1]

plt.figure(figsize=(8, 8))
x_sorted = np.sort(x)
y_positive_sorted = np.sqrt(radius**2 - x_sorted**2)
y_negative_sorted = -np.sqrt(radius**2 - x_sorted**2)
plt.scatter(x_sorted, y_positive_sorted, label='True Circle (Positive)', alpha=0.5, color='red')
plt.scatter(x_sorted, y_negative_sorted, label='True Circle (Negative)', alpha=0.5, color='red')
plt.scatter(test_x, pred_y_positive, label='Predicted (Positive)', alpha=0.5, color='limegreen', marker='x')
plt.scatter(test_x, pred_y_negative, label='Predicted (Negative)', alpha=0.5, color='cyan', marker='x')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Circle Approximation (x to y)')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()