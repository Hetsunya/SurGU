#https://www.kaggle.com/datasets/ligtfeather/englishrussiansentencepairs/data
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

train_file = "data/train.csv"
test_file = "data/test.csv"

train_data = pd.read_csv(train_file)
test_data = pd.read_csv(test_file)

train_data = train_data[:75000]
test_data = test_data[:25000]

train_data = train_data[['rus', 'eng']].dropna()
test_data = test_data[['rus', 'eng']].dropna()

rus_tokenizer = Tokenizer()
eng_tokenizer = Tokenizer()

rus_tokenizer.fit_on_texts(train_data['rus'])
eng_tokenizer.fit_on_texts(train_data['eng'])

max_rus_len = 70
max_eng_len = 70

def preprocess_data(data, tokenizer, max_len):
    sequences = tokenizer.texts_to_sequences(data)
    padded = pad_sequences(sequences, maxlen=max_len, padding='post')
    return padded

X_train = preprocess_data(train_data['rus'], rus_tokenizer, max_rus_len)
y_train = preprocess_data(train_data['eng'], eng_tokenizer, max_eng_len)
X_test = preprocess_data(test_data['rus'], rus_tokenizer, max_rus_len)
y_test = preprocess_data(test_data['eng'], eng_tokenizer, max_eng_len)

# Построение модели
vocab_size_rus = len(rus_tokenizer.word_index) + 1
vocab_size_eng = len(eng_tokenizer.word_index) + 1
embedding_dim = 256
units = 512

model = Sequential([
    Embedding(vocab_size_rus, embedding_dim, input_length=max_rus_len),
    Bidirectional(LSTM(units, return_sequences=True)),
    Dense(units, activation='relu'),
    Dense(vocab_size_eng, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

y_train = y_train.reshape(-1, max_eng_len, 1)
y_test = y_test.reshape(-1, max_eng_len, 1)

model.fit(X_train, y_train, epochs=5, batch_size=50, validation_data=(X_test, y_test))

def translate_sentence(sentence):
    seq = preprocess_data([sentence], rus_tokenizer, max_rus_len)
    pred = model.predict(seq)
    pred_sentence = ' '.join(
        [eng_tokenizer.index_word.get(idx, '') for idx in pred.argmax(axis=-1)[0] if idx > 0]
    )
    return pred_sentence

print("Перевод 'Как дела?':", translate_sentence("Как дела?"))
print("Где находится ближайший магазин?':", translate_sentence("Где находится ближайший магазин?"))
print("Сколько времени займет поездка?':", translate_sentence("Сколько времени займет поездка?"))
print("Сегодня прекрасная погода':", translate_sentence("Сегодня прекрасная погода"))
print("Мне нужно купить продукты для ужина':", translate_sentence("Мне нужно купить продукты для ужина"))
print("Этот фильм был очень интересным':", translate_sentence("Этот фильм был очень интересным"))

translation_file = "data/translation.csv"
translation_data = pd.read_csv(translation_file)

def generate_translations(data, rus_col):
    translations = []
    for sentence in data[rus_col]:
        translation = translate_sentence(sentence)  # Используем ранее определённую функцию
        translations.append(translation)
    return translations

row_limit = 1000

# Ограничиваем данные
limited_translation_data = translation_data.head(row_limit)

# Генерация переводов для ограниченного набора строк
limited_translation_data['model_translation'] = generate_translations(limited_translation_data, 'rus')

# Сохранение результата в новый файл
output_file = "data/best/translation_with_model_limited.csv"
limited_translation_data.to_csv(output_file, index=False, encoding='utf-8')

print(f"Переводы для первых {row_limit} строк сохранены в {output_file}")
