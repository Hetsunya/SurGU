import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dense, Dropout, MultiHeadAttention, LayerNormalization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras import regularizers
from nltk.translate.bleu_score import sentence_bleu

import re
import string

# Загрузка и очистка данных
data = pd.read_csv("sentences.csv")
data = data[:1000][['russian', 'english']]

# Очистка текста
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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

# Получение размеров
russian_vocab_size = len(russian_tokenizer.word_index) + 1
english_vocab_size = len(english_tokenizer.word_index) + 1

# Паддинг последовательностей
max_sequence_length = max(max(len(seq) for seq in russian_sequences), max(len(seq) for seq in english_sequences))
russian_sequences = pad_sequences(russian_sequences, maxlen=max_sequence_length, padding='post')
english_sequences = pad_sequences(english_sequences, maxlen=max_sequence_length, padding='post')

# Разделение данных
russian_train, russian_test, english_train, english_test = train_test_split(
    russian_sequences, english_sequences, test_size=0.2, random_state=42
)

# Создание модели biRNN с Attention
def create_improved_model(input_dim, output_dim, input_length):
    inputs = Input(shape=(input_length,))

    # Слой встраивания слов
    x = Embedding(input_dim=input_dim, output_dim=512, mask_zero=True)(inputs)

    # Блок LSTM + Attention
    x_res = Bidirectional(LSTM(512, return_sequences=True, dropout=0.3))(x)
    x = MultiHeadAttention(num_heads=16, key_dim=64)(x_res, x_res)
    x = Dropout(0.3)(x)
    x = LayerNormalization()(x)
    x = layers.add([x, x_res])  # Остаточная связь

    # Ещё один LSTM для обработки выходов
    x = Bidirectional(LSTM(256, return_sequences=True, dropout=0.3))(x)

    # Полносвязные слои
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)

    # Выходной слой
    outputs = Dense(output_dim, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model


# Создание модели
model = create_improved_model(russian_vocab_size, english_vocab_size, max_sequence_length)

# Колбэки
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-5)

# Обучение модели
history = model.fit(
    russian_train,
    np.expand_dims(english_train, -1),
    epochs=50,
    batch_size=4,
    validation_data=(russian_test, np.expand_dims(english_test, -1)),
    callbacks=[early_stopping, reduce_lr]
)

# Функция для предсказания перевода
def predict_translation(sentence):
    sentence_seq = russian_tokenizer.texts_to_sequences([sentence])
    sentence_seq = pad_sequences(sentence_seq, maxlen=max_sequence_length, padding='post')
    predicted_seq = model.predict(sentence_seq)
    predicted_seq = np.argmax(predicted_seq, axis=-1)[0]
    predicted_sentence = []
    for idx in predicted_seq:
        word = english_tokenizer.index_word.get(int(idx), '')
        if word == '<end>':
            break
        predicted_sentence.append(word)
    return ' '.join(predicted_sentence)

from nltk.translate.bleu_score import SmoothingFunction
smoothie = SmoothingFunction().method4

def calculate_bleu(reference, hypothesis):
    reference = [reference.split()]
    hypothesis = hypothesis.split()
    return sentence_bleu(reference, hypothesis, smoothing_function=smoothie)


# Тестирование
for i in range(5):
    test_sentence = russian_test[i]
    input_sentence = ' '.join([russian_tokenizer.index_word.get(x, '') for x in test_sentence if x > 0])
    print(f"Input: {input_sentence}")
    predicted = predict_translation(input_sentence)
    print(f"Predicted: {predicted}")
    original_sentence = ' '.join([english_tokenizer.index_word.get(x, '') for x in english_test[i] if x > 0])
    print(f"Original: {original_sentence}")
    print(f"BLEU Score: {calculate_bleu(original_sentence, predicted)}\n")

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()
