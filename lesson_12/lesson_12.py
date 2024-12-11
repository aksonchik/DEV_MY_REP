# -*- coding: utf-8 -*-

import json
import random


class Book:
    def __init__(self, title, author, year, isbn=None):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn if isbn else self.generate_isbn()
        self.is_available = True
        self.borrowed_by = None
        self.due_date = None

    def generate_isbn(self):
        return str(random.randint(1000000000, 9999999999))

    def borrow(self, user):
        if self.is_available:
            self.is_available = False
            self.borrowed_by = user
            self.due_date = "14 дней с момента взятия"
        else:
            print("Книга уже взята.")

    def return_book(self):
        self.is_available = True
        self.borrowed_by = None
        self.due_date = None

    def __repr__(self):
        return f"{self.title} by {self.author}, {self.year} (ISBN: {self.isbn}) - {'Available' if self.is_available else 'Borrowed'}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, identifier, by='isbn'):
        if by == 'isbn':
            self.books = [book for book in self.books if book.isbn != identifier]
        elif by == 'title':
            self.books = [book for book in self.books if book.title.lower() != identifier.lower()]
        elif by == 'author':
            self.books = [book for book in self.books if book.author.lower() != identifier.lower()]
        elif by == 'year':
            self.books = [book for book in self.books if str(book.year) != str(identifier)]

    def find_books_by_author_and_title(self, author, title):
        return next((book for book in self.books if book.author.lower() == author.lower() and book.title.lower() == title.lower()), None)

    def find_books_by_author(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]

    def list_available_books(self):
        return [book for book in self.books if book.is_available]

    def borrow_book(self, identifier, user, by='isbn'):
        if by == 'isbn':
            for book in self.books:
                if book.isbn == identifier:
                    book.borrow(user)
                    break
        elif by == 'author_title':
            author, title = identifier
            book = self.find_books_by_author_and_title(author, title)
            if book:
                book.borrow(user)
            else:
                print(f"Книга '{title}' автора {author} не найдена или уже взята.")

    def return_book(self, identifier, by='isbn'):
        if by == 'isbn':
            for book in self.books:
                if book.isbn == identifier:
                    book.return_book()
                    break
        elif by == 'author_title':
            author, title = identifier
            book = self.find_books_by_author_and_title(author, title)
            if book:
                book.return_book()
            else:
                print(f"Книга '{title}' автора {author} не найдена.")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([book.__dict__ for book in self.books], file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.books = [Book(d['title'], d['author'], d['year'], d['isbn']) for d in data]
                for book, d in zip(self.books, data):
                    book.is_available = d['is_available']
                    book.borrowed_by = d['borrowed_by']
                    book.due_date = d['due_date']
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Начинаем с пустой библиотеки.")
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла {filename}. Убедитесь, что файл не поврежден.")


def main():
    library = Library()
    library.load_from_file("library.json")

    while True:
        print("\nДобро пожаловать в библиотеку!")
        print("1. Показать доступные книги")
        print("2. Добавить книгу")
        print("3. Удалить книгу")
        print("4. Найти книги по автору")
        print("5. Взять книгу")
        print("6. Вернуть книгу")
        print("7. Сохранить библиотеку")
        print("8. Загрузить библиотеку")
        print("9. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            print("\nДоступные книги:")
            for book in library.list_available_books():
                print(book)

        elif choice == '2':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(Book(title, author, year))
            print(f"Книга '{title}' добавлена.")

        elif choice == '3':
            print("Удалить книгу по:")
            print("1. ISBN")
            print("2. Названию")
            print("3. Автору")
            print("4. Году издания")
            remove_choice = input("Выберите параметр: ")
            identifier = input("Введите значение: ")
            if remove_choice == '1':
                library.remove_book(identifier, by='isbn')
            elif remove_choice == '2':
                library.remove_book(identifier, by='title')
            elif remove_choice == '3':
                library.remove_book(identifier, by='author')
            elif remove_choice == '4':
                library.remove_book(identifier, by='year')
            print("Книга удалена.")

        elif choice == '4':
            author = input("Введите имя автора: ")
            books = library.find_books_by_author(author)
            if books:
                print(f"Книги автора {author}:")
                for book in books:
                    print(book)
            else:
                print(f"Книг автора {author} не найдено.")

        elif choice == '5':
            print("Взять книгу по:")
            print("1. ISBN")
            print("2. Автору и названию")
            borrow_choice = input("Выберите параметр: ")
            if borrow_choice == '1':
                isbn = input("Введите ISBN книги: ")
                user = input("Введите ваше имя: ")
                library.borrow_book(isbn, user, by='isbn')
            elif borrow_choice == '2':
                author = input("Введите имя автора: ")
                title = input("Введите название книги: ")
                user = input("Введите ваше имя: ")
                library.borrow_book((author, title), user, by='author_title')

        elif choice == '6':
            print("Вернуть книгу по:")
            print("1. ISBN")
            print("2. Автору и названию")
            return_choice = input("Выберите параметр: ")
            if return_choice == '1':
                isbn = input("Введите ISBN книги: ")
                library.return_book(isbn, by='isbn')
            elif return_choice == '2':
                author = input("Введите имя автора: ")
                title = input("Введите название книги: ")
                library.return_book((author, title), by='author_title')

        elif choice == '7':
            library.save_to_file("library.json")
            print("Состояние библиотеки сохранено в файл.")

        elif choice == '8':
            library.load_from_file("library.json")
            print("Состояние библиотеки загружено из файла.")

        elif choice == '9':
            library.save_to_file("library.json")
            print("До свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
