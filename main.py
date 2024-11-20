while True:
    name = input("Введите ваше имя (или 'выход' для завершения): ")

    if name.lower() == 'выход':
        print("До свидания!")
        break

    print(f"Привет, {name}!")
