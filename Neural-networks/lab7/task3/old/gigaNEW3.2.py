import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers, models

# Разделяем текст из файла на русский и английский
data = []
file_path = 'rus.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) >= 2:  # Если есть оба текста
            rus_text = parts[1]  # Русский текст
            eng_text = parts[0]  # Английский текст
            data.append((rus_text, eng_text))


# data = data[:int(len(data) * 0.5)]
data = data[:30000]
# Преобразуем в DataFrame
df = pd.DataFrame(data, columns=['russian', 'english'])

# Очищаем данные от лишних символов
df['russian'] = df['russian'].str.replace(r'[^а-яА-Я0-9\s]', '', regex=True)
df['english'] = df['english'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)

# Пример очищенных данных
print(df.head())

# Токенизация для русского (вход) и английского (выход)
russian_tokenizer = Tokenizer()
english_tokenizer = Tokenizer()

# Обучаем токенизаторы
russian_tokenizer.fit_on_texts(df['russian'])
english_tokenizer.fit_on_texts(df['english'])

# Получаем размер словаря
russian_vocab_size = len(russian_tokenizer.word_index) + 1
english_vocab_size = len(english_tokenizer.word_index) + 1

# Преобразуем текст в последовательности
rus_sequences = russian_tokenizer.texts_to_sequences(df['russian'])
eng_sequences = english_tokenizer.texts_to_sequences(df['english'])

# Дополняем последовательности до одинаковой длины
max_sequence_length = max(max(len(seq) for seq in rus_sequences), max(len(seq) for seq in eng_sequences))
rus_sequences = pad_sequences(rus_sequences, maxlen=max_sequence_length, padding='post')
eng_sequences = pad_sequences(eng_sequences, maxlen=max_sequence_length, padding='post')

# Пример подготовленных данных
print(rus_sequences[:5], eng_sequences[:5])

from tensorflow.keras import regularizers
from tensorflow.keras.layers import Attention

# Создаем модель biRNN
def create_birnn_model(russian_vocab_size, english_vocab_size, embedding_dim=256, hidden_units=512, max_sequence_length=40):
    input_rus = layers.Input(shape=(max_sequence_length,))
    x = layers.Embedding(russian_vocab_size, embedding_dim)(input_rus)

    # Уменьшаем количество слоев LSTM и скрытых нейронов
    x = layers.Bidirectional(layers.LSTM(hidden_units, return_sequences=True))(x)
    x = layers.Dropout(0.4)(x)  # Dropout после LSTM
    x = layers.Bidirectional(layers.LSTM(int(hidden_units / 2), return_sequences=True))(x)
    x = layers.Dropout(0.2)(x)  # Dropout после LSTM
    # После последнего слоя LSTM
    context_vector = Attention()([x, x])

    # Добавляем Dense слои с меньшей размерностью
    x = layers.Dense(hidden_units, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(int(hidden_units / 2), activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(english_vocab_size, activation='softmax')(x)

    model = models.Model(inputs=input_rus, outputs=x)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

# Создаем модель
model = create_birnn_model(russian_vocab_size, english_vocab_size, max_sequence_length=max_sequence_length)

# Обучаем модель
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Настроим EarlyStopping
early_stopping = EarlyStopping(
    monitor='val_loss',       # Отслеживаем валидационную потерю
    patience=3,               # Останавливаем обучение, если валидационная потеря не улучшается в течение 3 эпох
    min_delta=0.001,          # Минимальное улучшение, которое должно быть для продолжения
    restore_best_weights=True # Восстанавливаем лучшие веса модели
)

# Настроим ReduceLROnPlateau
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',  # Отслеживаем валидационную потерю
    factor=0.3,          # Уменьшаем скорость обучения в два раза
    patience=2,          # Через 2 эпохи без улучшений уменьшаем lr
    min_lr=1e-16          # Минимальная скорость обучения
)
# Обучаем модель с использованием EarlyStopping
model.fit(
    rus_sequences,
    np.expand_dims(eng_sequences, -1),
    epochs=2000,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping, reduce_lr]  # Указываем оба колбэка
)

model.save('biRNN_russian_to_english_model.keras')

# Пример предсказания
def predict_translation(model, russian_text):
    rus_seq = russian_tokenizer.texts_to_sequences([russian_text])
    rus_seq = pad_sequences(rus_seq, maxlen=max_sequence_length, padding='post')

    pred_seq = model.predict(rus_seq)
    pred_seq = np.argmax(pred_seq, axis=-1)[0]

    # Преобразуем обратно в текст
    translated_text = ' '.join([english_tokenizer.index_word.get(i) for i in pred_seq if i != 0])
    return translated_text


# Пример использования
translated_text = predict_translation(model, "Привет, как дела?")
print(translated_text)
