from zad_1 import Student


class Library:
    def __init__(self, city, street, zip_code, open_hours, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self):
        return f"Biblioteka {self.city} {self.zip_code}, {self.street}. Godziny otwarcia: {self.open_hours} | Kontakt: {self.phone}"


class Employee:
    def __init__(self, first_name, last_name, hire_date, birth_date,
                 city, street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self):
        return (f"Pracownik: {self.first_name} {self.last_name}, zatrudniony od: {self.hire_date}, "
                "urodzony: {self.birth_date}, adres: {self.city}, {self.street} {self.zip_code}, kontakt: {self.phone}")


class Book:
    def __init__(self, library: Library, publication_date, author_name: str,
                 author_surname: str, number_of_pages: int):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self):
        return (f"Książka autorstwa {self.author_name} {self.author_surname}, "
                f"opublikowana: {self.publication_date}, ilość stron: {self.number_of_pages}, "
                f"{self.library}")


class Order:
    def __init__(self, employee, student: Student, books: list[Book], order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self):
        books_list = ",\n\t".join(str(book) for book in self.books)
        return (f"Zamówienie od: {self.employee.first_name} {self.employee.last_name}, "
                f"student: {self.student.name}, data zamówienia: {self.order_date}, książki:\n\t{books_list}")


lib1 = Library("Warszawa", "Kwiatowa 12", "00-001", "8:00-18:00", "123456789")
lib2 = Library("Kraków", "Długa 4", "30-002", "9:00-17:00", "987654321")

book1 = Book(lib1, "2001", "Adam", "Mickiewicz", 350)
book2 = Book(lib1, "1999", "Henryk", "Sienkiewicz", 420)
book3 = Book(lib2, "2010", "J.K.", "Rowling", 500)
book4 = Book(lib2, "2020", "George", "Martin", 900)
book5 = Book(lib1, "2018", "Andrzej", "Sapkowski", 450)

emp1 = Employee("Jan", "Kowalski", "2020-05-01", "1985-03-02", "Warszawa", "Polna 1", "00-100", "111222333")
emp2 = Employee("Ewa", "Nowak", "2019-02-12", "1990-11-23", "Kraków", "Lipowa 3", "30-300", "222333444")
emp3 = Employee("Paweł", "Malinowski", "2021-07-15", "1995-09-14", "Warszawa", "Słoneczna 7", "00-200", "333444555")

student1 = Student("Kamil", [60.0, 70.0, 80.0])
student2 = Student("Marysia", [40.0, 55.0, 50.0])
student3 = Student("Ola", [90.0, 85.0, 88.0])

order1 = Order(emp1, student1, [book1, book2], "2024-01-15")
order2 = Order(emp3, student3, [book3, book5, book4], "2024-01-20")

print(f"Zamówienie 1:\n{order1}\n\nZamówienie 2:\n{order2}")

"""
Zamówienie 1:
Zamówienie od: Jan Kowalski, student: Kamil, data zamówienia: 2024-01-15, książki:
        Książka autorstwa Adam Mickiewicz, opublikowana: 2001, ilość stron: 350, Biblioteka Warszawa 00-001, Kwiatowa 12. Godziny otwarcia: 8:00-18:00 | Kontakt: 123456789,
        Książka autorstwa Henryk Sienkiewicz, opublikowana: 1999, ilość stron: 420, Biblioteka Warszawa 00-001, Kwiatowa 12. Godziny otwarcia: 8:00-18:00 | Kontakt: 123456789

Zamówienie 2:
Zamówienie od: Paweł Malinowski, student: Ola, data zamówienia: 2024-01-20, książki:
        Książka autorstwa J.K. Rowling, opublikowana: 2010, ilość stron: 500, Biblioteka Kraków 30-002, Długa 4. Godziny otwarcia: 9:00-17:00 | Kontakt: 987654321,
        Książka autorstwa Andrzej Sapkowski, opublikowana: 2018, ilość stron: 450, Biblioteka Warszawa 00-001, Kwiatowa 12. Godziny otwarcia: 8:00-18:00 | Kontakt: 123456789,
        Książka autorstwa George Martin, opublikowana: 2020, ilość stron: 900, Biblioteka Kraków 30-002, Długa 4. Godziny otwarcia: 9:00-17:00 | Kontakt: 987654321
"""
