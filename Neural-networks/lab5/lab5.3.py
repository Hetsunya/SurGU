import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf

def sigm(x):
    return tf.sin(x)

x = np.arange(-20, 20, 0.1)
y = np.sin(x) + np.sin(np.sqrt(2) * x)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=13)

model_T = keras.Sequential([
    layers.Dense(32, activation=sigm, input_shape=(1,)),
    layers.Dense(1)
])
model_T.compile(loss='mse', optimizer='rmsprop', metrics=['mae'])
model_T.fit(X_train, X_train // (2 * np.pi), epochs=150, batch_size=10)


model_fi = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(1,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

model_fi.compile(loss='mse', optimizer='rmsprop', metrics=['mae'])
model_fi.fit(X_train, X_train % (2 * np.pi), epochs=150, batch_size=10)

input_T = keras.Input(shape=(1,))
input_fi = keras.Input(shape=(1,))
concatenated = layers.Concatenate(axis=-1)([model_T(input_T), model_fi(input_fi)])
output = layers.Dense(16, activation=sigm)(concatenated)
output = layers.Dense(1)(output)

model_combined = keras.Model(inputs=[input_T, input_fi], outputs=output)

model_combined.compile(loss='mse', optimizer='rmsprop', metrics=['mae'])
model_combined.fit([X_train, X_train], y_train, epochs=150, batch_size=10)

accuracy = model_combined.evaluate([X_train, X_train], y_train)
print("Точность на обучающей выборке:", accuracy)

accuracy2 = model_combined.evaluate([X_test, X_test], y_test)
print("Точность на тестовой выборке:", accuracy2)

y_pred = model_combined.predict([X_test, X_test])

import matplotlib.pyplot as plt
plt.plot(x, y, label='f(x)')
plt.scatter(X_test, y_pred, label='Предсказания', color='red', alpha=1)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
