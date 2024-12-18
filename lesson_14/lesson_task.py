import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Удаление старой таблицы, если она существует
cursor.execute('DROP TABLE IF EXISTS books')
conn.commit()

cursor.execute('''
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INTEGER,
    available BLOB
)
''')
conn.commit()

# Вставка данных в таблицу books
# Используем b'\x01' для True и b'\x00' для False
cursor.executemany('''
INSERT INTO books (title, author, year, available) VALUES (?, ?, ?, ?)
''', [
    ("1984", "George Orwell", 1949, b'\x01'),  # b'\x01' - True
    ("To Kill a Mockingbird", "Harper Lee", 1960, b'\x01'),  # b'\x01' - True
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, b'\x00'),  # b'\x00' - False
    ("Moby Dick", "Herman Melville", 1851, b'\x01'),  # b'\x01' - True
    ("War and Peace", "Leo Tolstoy", 1869, b'\x00')  # b'\x00' - False
])
conn.commit()

# Выбор всех доступных книг
cursor.execute('SELECT * FROM books WHERE available = ?', (b'\x01',))
available_books = cursor.fetchall()
print("Доступные книги:")
for book in available_books:
    print(book)

# Поиск книг, выпущенных после 1950 года
cursor.execute('SELECT * FROM books WHERE year > 1950')
books_after_1950 = cursor.fetchall()
print("Книги, выпущенные после 1950 года:")
for book in books_after_1950:
    print(book)

# Обновление доступности книги "The Great Gatsby"
cursor.execute('UPDATE books SET available = ? WHERE title = ?', (b'\x01', "The Great Gatsby"))
conn.commit()
print("Доступность книги 'The Great Gatsby' обновлена.")

# Удаление книги "Moby Dick"
cursor.execute('DELETE FROM books WHERE title = ?', ("Moby Dick",))
conn.commit()
print("Книга 'Moby Dick' удалена.")

# Закрытие соединения
conn.close()
