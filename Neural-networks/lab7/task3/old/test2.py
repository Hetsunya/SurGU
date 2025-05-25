from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers, models

# 2. Загрузка модели
loaded_model = load_model('biRNN_russian_to_english_model.keras')
print("Модель загружена!")

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
data = data[:5000]
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


# Пример предсказания
def predict_translation(model, russian_text):
    rus_seq = russian_tokenizer.texts_to_sequences([russian_text])
    rus_seq = pad_sequences(rus_seq, maxlen=max_sequence_length, padding='post')

    pred_seq = model.predict(rus_seq)
    pred_seq = np.argmax(pred_seq, axis=-1)[0]

    # Преобразуем обратно в текст
    translated_text = ' '.join([english_tokenizer.index_word.get(i) for i in pred_seq if i != 0])
    return translated_text

# Теперь можно использовать загруженную модель для предсказаний
translated_text = predict_translation(loaded_model, "Как дела?")
print(f"Перевод: {translated_text}")