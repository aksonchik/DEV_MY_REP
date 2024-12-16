def file_reader(file_path):
    """Генератор для построчного чтения файла с учетом кодировки."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            for line in file:
                yield line
    except UnicodeDecodeError:
        print("Ошибка кодировки, пробуем использовать другую кодировку.")
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            for line in file:
                yield line

def python_lines(file_path):
    """Генератор для строк, содержащих слово 'Python' (не чувствительно к регистру)."""
    for line in file_reader(file_path):
        # Приводим строку к нижнему регистру и убираем пробелы в начале и конце
        if 'python' in line.strip().lower():  # Преобразуем строку в нижний регистр
            yield line.strip()  # Убираем лишние пробелы

# Пример использования:
for line in python_lines("example.txt"):
    print(line)
