import os
import shutil


def main():
    # �������� ��� ������������ �������
    print(f"��� ����� ��: {os.name}")

    # �������� ������� ���� �� �����
    current_path = os.getcwd()
    print(f"���� �� ������� �����: {current_path}")

    # ������� ������� ��� �������� ���������� � ������������ ������
    file_info = {}

    # �������� �� ���� ������ � ������� ����������
    for file_name in os.listdir(current_path):
        if os.path.isfile(file_name):
            file_extension = os.path.splitext(file_name)[1][1:]  # �������� ���������� ����� ��� �����
            directory_name = f"{file_extension}_files"

            # ������� ����� ��� ������� ����������, ���� ��� ��� �� ����������
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)

            # ���������� ���� � ��������������� �����
            new_path = os.path.join(directory_name, file_name)
            shutil.move(file_name, new_path)

            # ��������� ���������� � ������������ ������
            if directory_name not in file_info:
                file_info[directory_name] = {'count': 0, 'size': 0}
            file_info[directory_name]['count'] += 1
            file_info[directory_name]['size'] += os.path.getsize(new_path)

    # ������� ���������� � ������������ ������
    for directory, info in file_info.items():
        print(
            f"� ����� '{directory}' ���������� {info['count']} ������, �� ��������� ������ - {info['size'] / (1024 ** 3):.2f} ��������")

    # ��������������� ���� ���� � ������ �������������
    for directory in file_info.keys():
        for file_name in os.listdir(directory):
            old_path = os.path.join(directory, file_name)
            new_file_name = f"renamed_{file_name}"
            new_path = os.path.join(directory, new_file_name)
            os.rename(old_path, new_path)
            print(f"���� {file_name} ��� ������������ � {new_file_name}")
            break  # ��������������� ������ ���� ���� � ������ �����


if __name__ == "__main__":
    main()
