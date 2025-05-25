import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, TimeDistributed
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.utils import to_categorical

# Предположим, у нас есть два списка: rus_sentences и eng_sentences
rus_sentences = ['привет мир', 'как дела', 'это тест']
eng_sentences = ['hello world', 'how are you', 'this is a test']

# Предобработка
def preprocess(sentences):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentences)
    return tokenizer, tokenizer.texts_to_sequences(sentences)

# Токенизация
rus_tokenizer, rus_sequences = preprocess(rus_sentences)
eng_tokenizer, eng_sequences = preprocess(eng_sentences)

# Паддинг
max_len_rus = max(len(seq) for seq in rus_sequences)
max_len_eng = max(len(seq) for seq in eng_sequences)

rus_padded = pad_sequences(rus_sequences, maxlen=max_len_rus, padding='post')
eng_padded = pad_sequences(eng_sequences, maxlen=max_len_eng, padding='post')

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(rus_padded, eng_padded, test_size=0.2, random_state=42)

# Изменение y_train для работы с TimeDistributed
y_train = np.expand_dims(y_train, -1)  # Добавление размерности
y_test = np.expand_dims(y_test, -1)

# Преобразование y_train и y_test в one-hot encoding
y_train = to_categorical(y_train, num_classes=len(eng_tokenizer.word_index) + 1)
y_test = to_categorical(y_test, num_classes=len(eng_tokenizer.word_index) + 1)

# Создание модели biRNN
embedding_dim = 256
vocab_size_rus = len(rus_tokenizer.word_index) + 1
vocab_size_eng = len(eng_tokenizer.word_index) + 1

model = Sequential([
    Embedding(vocab_size_rus, embedding_dim, input_length=max_len_rus),
    Bidirectional(LSTM(128, return_sequences=True)),
    TimeDistributed(Dense(vocab_size_eng, activation='softmax'))
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучение модели
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1)

# Оценка модели
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')

# Функция для перевода
def translate(sentence):
    seq = rus_tokenizer.texts_to_sequences([sentence])
    padded = pad_sequences(seq, maxlen=max_len_rus, padding='post')
    pred = model.predict(padded)
    pred_indices = np.argmax(pred, axis=-1)
    return ' '.join(eng_tokenizer.sequences_to_texts(pred_indices))

# Пример перевода
translated_sentence = translate('привет мир')
print(f'Translated: {translated_sentence}')
