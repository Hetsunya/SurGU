import sqlite3
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc
from razdel import tokenize as razdel_tokenize
from functools import lru_cache
import logging

nltk.download("stopwords")

DB_PATH = "search_engine.db"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Natasha components
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

# Стоп-слова
custom_stop_words = {"статья", "википедия", "раздел", "страница", "см", "также"}
stop_words = set(stopwords.words("russian")).union(custom_stop_words)

@lru_cache(maxsize=10000)
def lemmatize_word(word):
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        return token.lemma.lower() if token.lemma else word.lower()
    return word.lower()

def tokenize(text, title, first_sentences_weight=2, max_sentences=3):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    
    words = []
    sentence_count = 0
    for sentence in doc.sents[:max_sentences]:
        for token in sentence.tokens:
            token.lemmatize(morph_vocab)
            word = token.lemma.lower()
            if word and word.isalnum() and not word.isdigit() and word not in stop_words and len(word) >= 3:
                words.append((word, first_sentences_weight))
        sentence_count += 1
    for sentence in doc.sents[max_sentences:]:
        for token in sentence.tokens:
            token.lemmatize(morph_vocab)
            word = token.lemma.lower()
            if word and word.isalnum() and not word.isdigit() and word not in stop_words and len(word) >= 3:
                words.append((word, 1))
    
    title_words = [(lemmatize_word(w.text), 3) for w in razdel_tokenize(title)
                   if w.text.isalnum() and w.text.lower() not in stop_words and len(w.text) >= 3]
    
    return words, title_words

def create_index_table():
    logging.info("Creating index tables...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS index_table')
    c.execute('''
        CREATE TABLE index_table (
            word TEXT,
            doc_id INTEGER,
            frequency INTEGER,
            PRIMARY KEY (word, doc_id),
            FOREIGN KEY (doc_id) REFERENCES documents(id)
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_word ON index_table (word)')
    c.execute('DROP TABLE IF EXISTS word_stats')
    c.execute('''
        CREATE TABLE word_stats (
            word TEXT PRIMARY KEY,
            doc_count INTEGER
        )
    ''')
    conn.commit()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='index_table'")
    if c.fetchone():
        logging.info("Table index_table created successfully")
    else:
        logging.error("Failed to create index_table")
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word_stats'")
    if c.fetchone():
        logging.info("Table word_stats created successfully")
    else:
        logging.error("Failed to create word_stats")
    conn.close()

def build_index():
    logging.info("Starting indexing...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM documents")
    docs = c.fetchall()
    conn.close()

    doc_count = len(docs)
    logging.info(f"Total documents to index: {doc_count}")
    index = defaultdict(lambda: defaultdict(int))
    word_doc_count = defaultdict(int)

    for doc_id, title, content in docs:
        words, title_words = tokenize(content, title)
        for word, weight in words:
            index[word][doc_id] += weight
            word_doc_count[word] += 1
        for word, weight in title_words:
            index[word][doc_id] += weight
            word_doc_count[word] += 2 #больший вес у названий
        logging.info(f"Indexed document ID {doc_id}, title: {title}, words: {len(words)}, title words: {len(title_words)}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    batch = []
    batch_size = 1000
    total_records = 0
    logging.info(f"Total unique words to index: {len(index)}")
    for word, doc_dict in index.items():
        for doc_id, freq in doc_dict.items():
            batch.append((word, doc_id, freq))
            total_records += 1
            if len(batch) >= batch_size:
                logging.info(f"Inserting batch of {len(batch)} records into index_table...")
                c.executemany("INSERT OR IGNORE INTO index_table (word, doc_id, frequency) VALUES (?, ?, ?)", batch)
                conn.commit()
                batch = []
    if batch:
        logging.info(f"Inserting final batch of {len(batch)} records into index_table...")
        c.executemany("INSERT OR IGNORE INTO index_table (word, doc_id, frequency) VALUES (?, ?, ?)", batch)
        conn.commit()

    logging.info(f"Total records inserted into index_table: {total_records}")

    stats_batch = []
    total_stats_records = 0
    logging.info(f"Total unique words for word_stats: {len(word_doc_count)}")
    for word, count in word_doc_count.items():
        stats_batch.append((word, count))
        total_stats_records += 1
        if len(stats_batch) >= batch_size:
            logging.info(f"Inserting batch of {len(stats_batch)} records into word_stats...")
            c.executemany("INSERT OR IGNORE INTO word_stats (word, doc_count) VALUES (?, ?)", stats_batch)
            conn.commit()
            stats_batch = []
    if stats_batch:
        logging.info(f"Inserting final batch of {len(stats_batch)} records into word_stats...")
        c.executemany("INSERT OR IGNORE INTO word_stats (word, doc_count) VALUES (?, ?)", stats_batch)
        conn.commit()

    c.execute("SELECT COUNT(*) FROM index_table")
    index_table_count = c.fetchone()[0]
    logging.info(f"Total rows in index_table: {index_table_count}")
    c.execute("SELECT COUNT(*) FROM word_stats")
    word_stats_count = c.fetchone()[0]
    logging.info(f"Total rows in word_stats: {word_stats_count}")

    conn.commit()
    conn.close()
    logging.info("Indexing completed.")

if __name__ == "__main__":
    create_index_table()
    build_index()