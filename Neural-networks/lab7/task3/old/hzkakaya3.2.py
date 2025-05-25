import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


data = []
file_path = 'rus.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) >= 2:  # Если есть оба текста
            rus_text = parts[1]  # Русский текст
            eng_text = parts[0]  # Английский текст
            data.append((rus_text, eng_text))\


# Загружаем датасет (замените путь на ваш)
# data = pd.DataFrame({
#     'russian': ['Привет', 'Как дела?', 'Спасибо', 'До свидания'],
#     'english': ['Hello', 'How are you?', 'Thank you', 'Goodbye']
# })
df = pd.DataFrame(data, columns=['russian', 'english'])

# Разделение на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Подготовка данных
def preprocess_data(data, tokenizer, max_len):
    sequences = tokenizer.texts_to_sequences(data)
    padded = pad_sequences(sequences, maxlen=max_len, padding='post')
    return padded

# Токенизация
rus_tokenizer = Tokenizer()
eng_tokenizer = Tokenizer()
rus_tokenizer.fit_on_texts(train_data['russian'])
eng_tokenizer.fit_on_texts(train_data['english'])

max_rus_len = max(len(seq) for seq in rus_tokenizer.texts_to_sequences(data['russian']))
max_eng_len = max(len(seq) for seq in eng_tokenizer.texts_to_sequences(data['english']))

X_train = preprocess_data(train_data['russian'], rus_tokenizer, max_rus_len)
y_train = preprocess_data(train_data['english'], eng_tokenizer, max_eng_len)
X_test = preprocess_data(test_data['russian'], rus_tokenizer, max_rus_len)
y_test = preprocess_data(test_data['english'], eng_tokenizer, max_eng_len)

# Построение модели
vocab_size_rus = len(rus_tokenizer.word_index) + 1
vocab_size_eng = len(eng_tokenizer.word_index) + 1
embedding_dim = 128
units = 256

model = Sequential([
    Embedding(vocab_size_rus, embedding_dim, input_length=max_rus_len),
    Bidirectional(LSTM(units, return_sequences=True)),
    Dense(units, activation='relu'),
    Dense(vocab_size_eng, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
y_train = y_train.reshape(-1, max_eng_len, 1)
y_test = y_test.reshape(-1, max_eng_len, 1)

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Проверка модели
def translate_sentence(sentence):
    seq = preprocess_data([sentence], rus_tokenizer, max_rus_len)
    pred = model.predict(seq)
    pred_sentence = ' '.join(
        [eng_tokenizer.index_word[idx] for idx in pred.argmax(axis=-1)[0] if idx > 0]
    )
    return pred_sentence

# Пример
print("Перевод 'Привет':", translate_sentence("Привет"))
