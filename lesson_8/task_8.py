# Задание 1
def calculate_bmi():
    try:
        # Запросить у пользователя информацию о росте в сантиметрах
        height_cm = float(input("Введите свой рост в сантиметрах: "))
        # Перевод высоты в метры
        height_m = height_cm / 100
        # Запросить у пользователя вес в килограммах
        weight_kg = float(input("Введите свой вес в килограммах: "))

        # Рассчет ИМТ
        bmi = weight_kg / (height_m ** 2)

        # Определите категорию ИМТ
        if bmi < 18.5:
            category = "Недостаточный вес"
        elif 18.5 <= bmi < 24.9:
            category = "Нормальный вес"
        elif 25 <= bmi < 29.9:
            category = "Избыточный вес"
        else:
            category = "Ожирение"

        # Отображение результатов
        print(f"Ваш ИМТ равен {bmi:.2f}, который классифицируется как {category}.")

    except ValueError:
        print("Неверный ввод. Пожалуйста, введите числовые значения для роста и веса.")


calculate_bmi()


# Задание 2
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def exponentiate(a, b):
    return a ** b


def modulo(a, b):
    return a % b


operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '**': exponentiate,
    '%': modulo
}


def calculator():
    while True:
        print("Добро пожаловать в программу Калькулятор!")
        print("Доступные операции: +, -, *, /, **, %")

        while True:
            try:
                num1 = float(input("Введите первое число: "))
                break
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение.")

        while True:
            try:
                num2 = float(input("Введите второе число: "))
                break
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение.")

        operation = input("Введите к операции (+, -, *, /, **, %): ")
        if operation not in operations:
            print("Недопустимая операция. Пожалуйста, выберите одну из доступных операций.")
            continue

        try:
            if operation == '/' and num2 == 0:
                print("Ошибка: Деление на ноль недопустимо.")
            else:
                result = operations[operation](num1, num2)
                print(f"Результат: {num1} {operation} {num2} = {result}")
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль недопустимо.")

        choice = input("Вы хотите выполнить другой расчет? (да/нет): ")
        if choice.lower() != 'да':
            print("Благодарим вас за использование калькулятора. До свидания!")
            break


calculator()
