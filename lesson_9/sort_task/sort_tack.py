import os
import shutil


def main():
    # Получаем имя операционной системы
    print(f"Имя вашей ОС: {os.name}")

    # Получаем текущий путь до папки
    current_path = os.getcwd()
    print(f"Путь до текущей папки: {current_path}")

    # Создаем словарь для хранения информации о перемещенных файлах
    file_info = {}

    # Проходим по всем файлам в текущей директории
    for file_name in os.listdir(current_path):
        if os.path.isfile(file_name):
            file_extension = os.path.splitext(file_name)[1][1:]  # Получаем расширение файла без точки
            directory_name = f"{file_extension}_files"

            # Создаем папку для каждого расширения, если она еще не существует
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)

            # Перемещаем файл в соответствующую папку
            new_path = os.path.join(directory_name, file_name)
            shutil.move(file_name, new_path)

            # Обновляем информацию о перемещенных файлах
            if directory_name not in file_info:
                file_info[directory_name] = {'count': 0, 'size': 0}
            file_info[directory_name]['count'] += 1
            file_info[directory_name]['size'] += os.path.getsize(new_path)

    # Выводим информацию о перемещенных файлах
    for directory, info in file_info.items():
        print(
            f"В папке '{directory}' перемещено {info['count']} файлов, их суммарный размер - {info['size'] / (1024 ** 3):.2f} гигабайт")

    # Переименовываем один файл в каждой поддиректории
    for directory in file_info.keys():
        for file_name in os.listdir(directory):
            old_path = os.path.join(directory, file_name)
            new_file_name = f"renamed_{file_name}"
            new_path = os.path.join(directory, new_file_name)
            os.rename(old_path, new_path)
            print(f"Файл {file_name} был переименован в {new_file_name}")
            break  # Переименовываем только один файл в каждой папке


if __name__ == "__main__":
    main()
