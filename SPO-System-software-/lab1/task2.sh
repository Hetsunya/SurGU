#!/bin/bash

# Проверяем, что передано хотя бы одно имя файла
if [ $# -eq 0 ]; then
  echo "Не указаны имена файлов"
  exit 1
fi

# Обрабатываем каждое имя файла из списка аргументов
for filename in "$@"; do
  # Проверяем, что файл существует
  if [ ! -f "$filename" ]; then
    echo "Файл $filename не найден"
    continue
  fi

  # Выводим три временных штампа для файла
  echo "Время создания файла $filename: $(stat -c %w "$filename")"
  echo "Время последнего изменения файла $filename: $(stat -c %y "$filename")"
  echo "Время последнего доступа к файлу $filename: $(stat -c %x "$filename")"
done

#2 ВЕРСИЯ

#!/bin/bash

# Проверяем, что передано хотя бы одно имя файла
if [ $# -eq 0 ]; then
  echo "Не указаны имена файлов"
  exit 1
fi

# Обрабатываем каждое имя файла из списка аргументов
for filename in "$@"; do
  # Проверяем, что файл существует
  if [ ! -f "$filename" ]; then
    echo "Файл $filename не найден"
    continue
  fi

  # Выводим три временных штампа для файла
  echo "Время создания файла $filename: $(gawk 'BEGIN { FS="\""; OFS=":" } { print $2 }' <<< "$(stat -c "%w\"%y\"%x" "$filename")")"
  echo "Время последнего изменения файла $filename: $(gawk 'BEGIN { FS="\""; OFS=":" } { print $4 }' <<< "$(stat -c "%w\"%y\"%x" "$filename")")"
  echo "Время последнего доступа к файлу $filename: $(gawk 'BEGIN { FS="\""; OFS=":" } { print $6 }' <<< "$(stat -c "%w\"%y\"%x" "$filename")")"
done