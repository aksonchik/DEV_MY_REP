# Задание 8
import json
import csv


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        print("Ошибка: данные должны быть списком словарей")


def save_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def add_employee_to_json(json_file, new_employee):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data.append(new_employee)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_employee_to_csv(csv_file, new_employee):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_employee.keys())
        writer.writerow(new_employee)


def get_employee_by_name(json_file, name):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for employee in data:
        try:
            if isinstance(employee, dict) and 'name' in employee and employee['name'] == name:
                return employee
        except TypeError as e:
            print(f"Ошибка типа данных: {e} для элемента {employee}")

    return None


def filter_by_language(json_file, language):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    employees_with_language = []
    for employee in data:
        try:
            if isinstance(employee, dict) and 'programming_languages' in employee and language in employee[
                'programming_languages']:
                employees_with_language.append(employee)
        except TypeError as e:
            print(f"Ошибка типа данных: {e} для элемента {employee}")

    return employees_with_language


def average_height_by_year(json_file, year):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_employees = [employee for employee in data if
                          isinstance(employee, dict) and employee.get('birth_year', 0) < year]
    if not filtered_employees:
        return 0

    total_height = sum(employee['height'] for employee in filtered_employees)
    return total_height / len(filtered_employees)


def main():
    # Укажите путь к вашему JSON-файлу
    json_file = "C:\PyProgramms\DEV_MY_REP\lesson_9\json_files\employees.json"
    csv_file = "C:\PyProgramms\DEV_MY_REP\lesson_9\csv_files\employees.csv"

    while True:
        print("Выберите действие:")
        print("1. Преобразовать JSON в CSV")
        print("2. Сохранить данные в CSV")
        print("3. Добавить сотрудника в JSON")
        print("4. Добавить сотрудника в CSV")
        print("5. Найти сотрудника по имени")
        print("6. Фильтр по языку программирования")
        print("7. Средний рост по году рождения")
        print("8. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            json_to_csv(json_file, csv_file)
        elif choice == '2':
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            save_to_csv(data, csv_file)
        elif choice == '3':
            new_employee = {
                "name": input("Введите имя: "),
                "birth_year": int(input("Введите год рождения: ")),
                "height": int(input("Введите рост: ")),
                "programming_languages": input("Введите языки программирования (через запятую): ").split(",")
            }
            add_employee_to_json(json_file, new_employee)
        elif choice == '4':
            new_employee = {
                "name": input("Введите имя: "),
                "birth_year": int(input("Введите год рождения: ")),
                "height": int(input("Введите рост: ")),
                "programming_languages": input("Введите языки программирования (через запятую): ").split(",")
            }
            add_employee_to_csv(csv_file, new_employee)
        elif choice == '5':
            name = input("Введите имя сотрудника: ")
            print(get_employee_by_name(json_file, name))
        elif choice == '6':
            language = input("Введите язык программирования: ")
            print(filter_by_language(json_file, language))
        elif choice == '7':
            year = int(input("Введите год рождения: "))
            print(average_height_by_year(json_file, year))
        elif choice == '8':
            break
        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()


# Задание 7
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            result += char
    return result


def encrypt_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for i, line in enumerate(lines):
            encrypted_line = caesar_cipher(line.strip(), i + 1)
            file.write(encrypted_line + '\n')


# Пример использования
input_file = r"C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\caesar_input.txt"
output_file = r"C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\caesar_output.txt"
encrypt_file(input_file, output_file)

print(f"Файл '{input_file}' был зашифрован и сохранен как '{output_file}'")

# Задание 6
import re


def sum_numbers_in_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()

    # Извлекаем все последовательности цифр
    numbers = re.findall(r'\d+', content)

    # Преобразуем каждую последовательность в число и суммируем их
    total_sum = sum(int(number) for number in numbers)

    return total_sum


# Пример использования
file_path = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\data.txt'
total_sum = sum_numbers_in_file(file_path)
print(f"Сумма всех чисел в файле: {total_sum}")


# Задание 5
def read_students(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                last_name, first_name, grade = parts
                if grade.isdigit() and int(grade) < 3:
                    print(f"{last_name} {first_name}: {grade}")

# Пример использования
file_path = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\students.txt'
read_students(file_path)


# Задание 4
import re

def load_stop_words(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        stop_words = file.read().strip().split()
    return stop_words

def censor_text(file_path, stop_words, output_file):
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()

    # Заменяем запрещенные слова на звездочки
    for word in stop_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        content = pattern.sub('*' * len(word), content)

    # Записываем результат в файл
    with open(output_file, 'w', encoding='latin-1') as file:
        file.write(content)

    print(f"Цензурированный текст записан в файл: {output_file}")

# Пример использования
stop_words_file = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\stop_words.txt'
text_file = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\text_to_censor.txt'
output_file = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\censored_text.txt'

stop_words = load_stop_words(stop_words_file)
censor_text(text_file, stop_words, output_file)

# Задание 3
from collections import Counter

def find_most_common_word(line):
    words = line.split()
    count = Counter(words)
    most_common_word, frequency = count.most_common(1)[0]
    return most_common_word, frequency

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip():  # Проверяем, что строка не пустая
                most_common_word, frequency = find_most_common_word(line)
                file.write(f"{most_common_word} {frequency}\n")

# Пример использования
input_file = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\input.txt'
output_file = r'C:\PyProgramms\DEV_MY_REP\lesson_9\txt_files\output.txt'
process_file(input_file, output_file)

print(f"Самые частые слова и их количество записаны в файл: {output_file}")


# Задание 2
import re

def replace_names(text):
    pattern = re.compile(r'\b[A-ZА-Я][a-zа-я]*(?:-[A-ZА-Я][a-zа-я]*)?\s+[A-ZА-Я][a-zа-я]*\s+[A-ZА-Я][a-zа-я]*\b')

    # Замена всех найденных ФИО на "N"
    result = pattern.sub('N', text)

    return result

# Пример использования
text = """Подсудимая Эверт-Колокольцева Елизавета Александровна
в судебном заседании вину инкриминируемого
правонарушения признала в полном объёме и суду показала,
что 14 сентября 1876 года, будучи в состоянии алкогольного
опьянения от безысходности, в связи с состоянием здоровья
позвонила со своего стационарного телефона в полицию,
сообщив о том, что у неё в квартире якобы заложена бомба.
После чего приехали сотрудники полиции, скорая
и пожарные, которым она сообщила, что бомба — это она."""

print(replace_names(text))
