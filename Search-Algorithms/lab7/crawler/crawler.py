import requests
from bs4 import BeautifulSoup
import re
import hashlib
import logging
from queue import PriorityQueue
import sqlite3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = "search_engine.db"

def validlink(href):
    """Проверка, является ли ссылка валидной статьёй Википедии."""
    if href:
        if re.compile('^/wiki/').search(href):
            if not re.compile('/\w+:').search(href):  # Исключаем служебные страницы
                if not re.compile('/#').search(href):  # Исключаем ссылки на секции
                    return True
    return False

def extract_links(url, base_url='https://ru.wikipedia.org'):
    """Извлечение ссылок из статьи."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        links = []
        for link in soup.findAll("a"):
            href = link.get("href", "")
            if validlink(href):
                full_url = base_url + href
                links.append(full_url)
        return links
    except Exception as e:
        logging.error(f"Error extracting links from {url}: {e}")
        return []

def crawl():
    """Основная функция краулера с приоритизацией по глубине."""
    seed_url = 'https://ru.wikipedia.org/wiki/Список_музыкальных_жанров,_направлений_и_стилей'
    base_url = 'https://ru.wikipedia.org'
    
    # Инициализация очереди с приоритетами
    url_queue = PriorityQueue()
    url_queue.put((0, seed_url))  # (depth, url)
    
    # Словарь для отслеживания обработанных ссылок
    url_process_map = {}
    md5_encode = hashlib.md5(seed_url.encode())
    url_process_map[md5_encode.hexdigest()] = 1
    
    # Подключение к базе данных
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            content TEXT,
            links TEXT,
            depth INTEGER
        )
    ''')
    conn.commit()
    
    max_articles = 1000
    processed_count = 0
    
    while not url_queue.empty() and processed_count < max_articles:
        depth, current_url = url_queue.get()
        logging.info(f"Processing depth {depth}: {current_url}")
        
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.find('h1', {'class': 'firstHeading'}).text
            content = soup.get_text()
            
            # Извлечение ссылок
            links = extract_links(current_url, base_url)
            links_str = ",".join(links)
            
            # Сохранение в базу данных
            c.execute("INSERT OR IGNORE INTO documents (url, title, content, links, depth) VALUES (?, ?, ?, ?, ?)",
                      (current_url, title, content, links_str, depth))
            conn.commit()
            processed_count += 1
            logging.info(f"Saved article {processed_count}: {title}")
            
            # Добавление новых ссылок
            for link in links:
                md5_encode = hashlib.md5(link.encode())
                link_hash = md5_encode.hexdigest()
                if link_hash not in url_process_map:
                    url_process_map[link_hash] = 0
                    url_queue.put((depth + 1, link))
                    url_process_map[link_hash] = 1
                    logging.info(f"Added link {link} from {current_url} at depth {depth + 1}")
                    
        except Exception as e:
            logging.error(f"Error processing {current_url}: {e}")
            continue
    
    conn.close()
    logging.info(f"Crawling completed. Total articles processed: {processed_count}")

if __name__ == "__main__":
    crawl()