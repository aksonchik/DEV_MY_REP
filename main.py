import time
from functools import wraps, reduce

# Задание 1
numbers = [1, 2, 3]

string_list = list(map(str, numbers))

print(string_list)

# Задание 2
numbers = [1, -2, 3, 0, -5]

filtered_numbers = list(filter(lambda x: x > 0, numbers))

print(filtered_numbers)

# Задание 3
strings = ['abc', 'abcba', '12321', 'hello', 'level']

palindromes = list(filter(lambda s: s == s[::-1], strings))

print(palindromes)


# Задание 4
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.6f} seconds to execute.")
        return result

    return wrapper


@timing_decorator
def example_function(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


example_function(1000000)

# Задание 5
rooms = [
    {"name": "Kitchen", "length": 6, "width": 4},
    {"name": "Room 1", "length": 5.5, "width": 4.5},
    {"name": "Room 2", "length": 5, "width": 4},
    {"name": "Room 3", "length": 7, "width": 6.3},
]

areas = map(lambda room: room["length"] * room["width"], rooms)

total_area = reduce(lambda x, y: x + y, areas)

print(f"Total apartment area: {total_area} square units.")
