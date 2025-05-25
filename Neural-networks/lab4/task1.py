import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense

x = np.arange(-20, 20, 0.1)
y = x

split_idx = int(0.8 * len(x))
x_train, x_test = x[:split_idx], x[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

model = Sequential()
model.add(Dense(units=1, input_dim=1))

model.compile(optimizer='sgd', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=10, batch_size=4)

plt.scatter(y_test, model.predict(x_test), color='r', label='Predictions')
plt.plot(x, y, label='True Function')
plt.legend()
plt.show()
