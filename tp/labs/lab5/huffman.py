import heapq
from collections import Counter
import os
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

# Построение дерева Хаффмана и создание кодов
def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, HuffmanNode(char, freq))
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)
    
    return heap[0]

def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
    
    if node.char is not None:
        codes[node.char] = current_code if current_code else "0"
        return
    
    if node.left:
        build_huffman_codes(node.left, current_code + "0", codes)
    if node.right:
        build_huffman_codes(node.right, current_code + "1", codes)
    
    return codes

# Сжатие текста
def huffman_compress(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return
    
    if not text:
        print("Файл пуст.")
        return
    
    # Подсчет частот символов
    freq_dict = Counter(text)
    print(freq_dict)
    if len(freq_dict) == 1:  # Если только один символ в тексте 
        freq_dict[text[0]] += 1
    
    # Построение дерева и кодов
    root = build_huffman_tree(freq_dict)
    huffman_codes = build_huffman_codes(root)
    
    # Кодирование текста в биты
    encoded_text = "".join(huffman_codes[char] for char in text)
    
    # Преобразование строки битов в байты
    padding = (8 - len(encoded_text) % 8) % 8  # Дополнение до кратности 8
    encoded_text += "0" * padding
    byte_data = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_data.append(int(byte, 2))
    
    # Запись в файл: заголовок (частоты) + padding + сжатые данные
    try:
        with open(output_file_path, 'wb') as file:
            # Записываем количество уникальных символов
            file.write(len(freq_dict).to_bytes(2, 'big'))
            # Записываем частотную таблицу
            for char, freq in freq_dict.items():
                char_bytes = char.encode('utf-8')
                file.write(len(char_bytes).to_bytes(1, 'big'))
                file.write(char_bytes)
                file.write(freq.to_bytes(4, 'big'))
            # Записываем количество дополненных битов
            file.write(padding.to_bytes(1, 'big'))
            # Записываем сжатые данные
            file.write(byte_data)
        
        print("Сжатие завершено.")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

# Декомпрессия текста
def huffman_decompress(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'rb') as file:
            # Читаем заголовок
            num_chars = int.from_bytes(file.read(2), 'big')
            freq_dict = {}
            for _ in range(num_chars):
                char_len = int.from_bytes(file.read(1), 'big')
                char = file.read(char_len).decode('utf-8')
                freq = int.from_bytes(file.read(4), 'big')
                freq_dict[char] = freq
            
            padding = int.from_bytes(file.read(1), 'big')
            compressed_data = file.read()
    except Exception as e:
        print(f"Ошибка при чтении сжатого файла: {e}")
        return
    
    # Преобразование байтов в биты
    bit_string = ""
    for byte in compressed_data:
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits
    bit_string = bit_string[:-padding]  # Убираем дополнение
    
    # Построение дерева
    root = build_huffman_tree(freq_dict)
    
    # Декодирование
    decompressed_text = []
    current_node = root
    with tqdm(total=len(bit_string), desc="Декомпрессия", unit="bit") as progress:
        for bit in bit_string:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right
            
            if current_node.char is not None:
                decompressed_text.append(current_node.char)
                current_node = root
            progress.update(1)
    
    # Запись результата
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write("".join(decompressed_text))
        print("Декомпрессия завершена.")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

# Основная функция
def main():
    root = tk.Tk()
    root.withdraw()
    
    input_file_path = filedialog.askopenfilename(title="Выберите файл для сжатия")
    if not input_file_path:
        print("Файл не выбран.")
        return
    
    compressed_file_path = input_file_path + '.huffman'
    decompressed_file_path = input_file_path + '.decompressed.txt'
    
    # Сжатие
    huffman_compress(input_file_path, compressed_file_path)
    
    # Декомпрессия
    huffman_decompress(compressed_file_path, decompressed_file_path)
    
    # Вывод статистики
    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(compressed_file_path)
    decompressed_size = os.path.getsize(decompressed_file_path)
    compression_ratio = (1 - compressed_size / original_size) * 100
    
    print(f"\nСтатистика:")
    print(f"Размер исходного файла: {original_size} байт")
    print(f"Размер сжатого файла: {compressed_size} байт")
    print(f"Размер разжатого файла: {decompressed_size} байт")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}%")
    
    # Проверка корректности
    with open(input_file_path, 'r', encoding='utf-8') as orig, \
         open(decompressed_file_path, 'r', encoding='utf-8') as dec:
        if orig.read() == dec.read():
            print("Декомпрессия прошла успешно: файлы идентичны.")
        else:
            print("Ошибка: декомпрессированный файл отличается от исходного.")

if __name__ == "__main__":
    main()