import pandas as pd
import numpy as np
import string
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Очистка текста
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Загрузка данных
data = pd.read_csv('sentences.csv')

# Очистка данных
data['russian'] = data['russian'].apply(clean_text)
data['english'] = data['english'].apply(lambda x: '<start> ' + clean_text(x) + ' <end>')

# Подготовка данных
russian_sentences = data['russian'].tolist()
english_sentences = data['english'].tolist()

# Токенизация
russian_tokenizer = Tokenizer(oov_token="<OOV>", filters='')
russian_tokenizer.fit_on_texts(russian_sentences)
russian_sequences = russian_tokenizer.texts_to_sequences(russian_sentences)

english_tokenizer = Tokenizer(oov_token="<OOV>", filters='')
english_tokenizer.fit_on_texts(english_sentences)
english_sequences = english_tokenizer.texts_to_sequences(english_sentences)

# Паддинг последовательностей
max_sequence_length = max(max(len(seq) for seq in russian_sequences), max(len(seq) for seq in english_sequences))
russian_sequences = pad_sequences(russian_sequences, maxlen=max_sequence_length, padding='post')
english_sequences = pad_sequences(english_sequences, maxlen=max_sequence_length, padding='post')

# Разделение данных
russian_train, russian_test, english_train, english_test = train_test_split(
    russian_sequences, english_sequences, test_size=0.2, random_state=42
)

# Размерности после разделения
print(f'Размерность русских обучающих данных: {russian_train.shape}')
print(f'Размерность английских обучающих данных: {english_train.shape}')

# Подготовка входных и выходных последовательностей для английского текста
# Входные последовательности: все кроме последнего токена (без <end>)
english_input_sequences = english_train[:, :-1]  # Без последнего токена
# Выходные последовательности: все кроме первого токена (без <start>)
english_output_sequences = english_train[:, 1:]  # Без первого токена

# Проверка размерности входных и выходных последовательностей для английского
print(f"Размерность входных последовательностей для английского текста: {english_input_sequences.shape}")
print(f"Размерность выходных последовательностей для английского текста: {english_output_sequences.shape}")

# Убедитесь, что размерности совпадают перед обучением
assert len(russian_train) == len(english_input_sequences), f"Размерности не совпадают! {len(russian_train)} != {len(english_input_sequences)}"

# Модель biRNN
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense

# Создание модели
model = Sequential()
model.add(Embedding(input_dim=len(russian_tokenizer.word_index) + 1, output_dim=256, input_length=max_sequence_length))
model.add(Bidirectional(LSTM(512, return_sequences=True)))
model.add(Dense(len(english_tokenizer.word_index) + 1, activation='softmax'))

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(russian_train, english_input_sequences, epochs=10, batch_size=64, validation_data=(russian_test, english_test))

# Оценка модели
test_loss, test_acc = model.evaluate(russian_test, english_test)
print(f'Test Loss: {test_loss}, Test Accuracy: {test_acc}')
