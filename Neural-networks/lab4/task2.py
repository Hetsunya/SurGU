import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense

x = np.arange(-20, 20, 0.1)
y = np.abs(x)

split_idx = int(0.8 * len(x))
x_train, x_test = x[:split_idx], x[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

model = Sequential()
model.add(Dense(10, input_dim=1, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam')

history = model.fit(x_train, y_train, epochs=100, batch_size=32)

train_loss = model.evaluate(x_train, y_train, verbose=0)
test_loss = model.evaluate(x_test, y_test, verbose=0)
print(f"Train MSE: {train_loss:.4f}")
print(f"Test MSE: {test_loss:.4f}")

y_pred = model.predict(x_test)
plt.plot(x, y, label='True Function')
plt.scatter(x_test, y_pred, color='r', label='Predictions')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('f(x) = |x|')
plt.legend()
plt.show()