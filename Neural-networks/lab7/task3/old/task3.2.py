import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, Bidirectional, Concatenate, Dot, Activation
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2

# Загрузка датасета
data = pd.read_csv("sentences.csv")

data = data[:1000]
data = data[['russian', 'english']]

# Подготовка данных
russian_sentences = data['russian'].tolist()
english_sentences = data['english'].tolist()

# # Список стоп-слов
# stop_words = set(['and', 'the', 'of', 'let', 'god', 'their'])
#
# # Удаление стоп-слов
# russian_sentences = [' '.join([word for word in sentence.split() if word not in stop_words]) for sentence in
#                      russian_sentences]
# english_sentences = [' '.join([word for word in sentence.split() if word not in stop_words]) for sentence in
#                      english_sentences]

# Токенизация
russian_tokenizer = Tokenizer()
russian_tokenizer.fit_on_texts(russian_sentences)
russian_sequences = russian_tokenizer.texts_to_sequences(russian_sentences)

english_tokenizer = Tokenizer()
english_tokenizer.fit_on_texts(english_sentences)
english_sequences = english_tokenizer.texts_to_sequences(english_sentences)

# Получение размеров
russian_vocab_size = len(russian_tokenizer.word_index) + 1
english_vocab_size = len(english_tokenizer.word_index) + 1

# Паддинг последовательностей
max_sequence_length = max(max(len(seq) for seq in russian_sequences), max(len(seq) for seq in english_sequences))
russian_sequences = pad_sequences(russian_sequences, maxlen=max_sequence_length, padding='post')
english_sequences = pad_sequences(english_sequences, maxlen=max_sequence_length, padding='post')

# Разделение данных на обучающую и тестовую выборки
russian_train, russian_test, english_train, english_test = train_test_split(
    russian_sequences, english_sequences, test_size=0.2, random_state=42
)


# Внимание (Attention) на основе механизма Bahdanau
def attention_layer(inputs):
    query = Dense(64)(inputs)
    key = Dense(64)(inputs)
    value = Dense(64)(inputs)

    score = Dot(axes=[2, 2])([query, key])
    attention_weights = Activation('softmax')(score)
    context_vector = Dot(axes=[2, 1])([attention_weights, value])

    return context_vector


# Создание модели Seq2Seq с BiLSTM и Attention
def create_model(input_dim, output_dim, input_length):
    # Кодировщик
    encoder_inputs = Input(shape=(input_length,))
    encoder_emb = Embedding(input_dim=input_dim, output_dim=512)(encoder_inputs)
    encoder_bilstm = Bidirectional(LSTM(256, return_sequences=True, return_state=True, kernel_regularizer=l2(0.01)))
    encoder_outputs, forward_h, forward_c, backward_h, backward_c = encoder_bilstm(encoder_emb)
    state_h = Concatenate()([forward_h, backward_h])
    state_c = Concatenate()([forward_c, backward_c])

    # Механизм внимания
    context_vector = attention_layer(encoder_outputs)

    # Декодировщик
    decoder_inputs = Input(shape=(input_length,))
    decoder_emb = Embedding(input_dim=output_dim, output_dim=512)(decoder_inputs)
    decoder_lstm = LSTM(512, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_emb, initial_state=[state_h, state_c])

    # Внимание к декодировщику
    decoder_combined_context = Concatenate()([decoder_outputs, context_vector])

    # Полносвязный слой
    output = Dense(output_dim, activation='softmax')(decoder_combined_context)

    # Модель
    model = Model([encoder_inputs, decoder_inputs], output)
    model.compile(optimizer=Adam(learning_rate=0.0003), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

print(f"Размер словаря русского языка: {russian_vocab_size}")
print(f"Размер словаря английского языка: {english_vocab_size}")
print(f"Максимальная длина последовательности: {max_sequence_length}")

# Проверка правильности индексации
print(f"Максимальный индекс в выходных данных: {np.max(english_sequences)}")
print(f"Максимальный индекс в русских данных: {np.max(russian_sequences)}")

print(f"Форма обучающих данных русского языка: {russian_train.shape}")
print(f"Форма обучающих данных английского языка: {english_train.shape}")


# Создание модели
model = create_model(russian_vocab_size, english_vocab_size, max_sequence_length)

# Обучение модели с разделением на тренировочную и тестовую выборки
history = model.fit(
    [russian_train, english_train],
    np.expand_dims(english_train, -1),
    epochs=100,
    batch_size=128,
    validation_data=([russian_test, english_test], np.expand_dims(english_test, -1)),
    callbacks = [EarlyStopping(patience=20, restore_best_weights=True)]  # Раннее завершение при переобучении
)

# Сохранение модели
model.save("model_with_attention_true.keras", include_optimizer=True)
model.save("model_with_attention_false.keras", include_optimizer=False)


# Функция для предсказания перевода
def predict_translation(sentence):
    # Токенизация входного предложения
    sentence_seq = russian_tokenizer.texts_to_sequences([sentence])
    sentence_seq = pad_sequences(sentence_seq, maxlen=max_sequence_length, padding='post')

    # Предсказание модели
    predicted_seq = model.predict([russian_train[:1], english_train[:1]])
    predicted_indices = np.argmax(predicted_seq, axis=-1)[0]
    predicted_sentence = [english_tokenizer.index_word.get(idx, '') for idx in predicted_indices if idx > 0]

    return ' '.join(predicted_sentence)


for i in range(len(russian_test * 0.95)):
    test_sentence = russian_test[i]
    test_original = english_test[i]
    print(f"Input: {' '.join([russian_tokenizer.index_word[int(x)] for x in test_sentence if x > 0])}")
    print(f"Translation: {predict_translation(' '.join([russian_tokenizer.index_word[int(x)] for x in test_sentence if x > 0]))}\n")
    print(f"Original: {' '.join([english_tokenizer.index_word[int(x)] for x in test_original if x > 0])}")

# Вывод 5 предложений из обучающей выборки
print('----------------------Данные из обучающей выборки---------------------------')
for i in range(len(russian_train * 0.95)):
    train_sentence = russian_train[i]
    test_original = english_test[i]
    train_original = english_train[i]
    print(f"Input: {' '.join([russian_tokenizer.index_word[int(x)] for x in train_sentence if x > 0])}")
    print(f"Translation: {predict_translation(' '.join([russian_tokenizer.index_word[int(x)] for x in train_sentence if x > 0]))}\n")
    print(f"Original: {' '.join([english_tokenizer.index_word[int(x)] for x in train_original if x > 0])}\n")