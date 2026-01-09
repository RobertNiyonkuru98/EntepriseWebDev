class Book:
    def __init__(self, title,author,year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True
        # What attribute are we missing here?

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
        # What functionalities can we implement

    def borrow_book(self, book):
        if book.is_available:
            book.is_available= False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"'{book.title}' is not available")


    def return_book(self, book):
        if book in self.borrowed_books:
            book.is_available = True
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'")

    def view_borrowed_books(self):
        for book in self.borrowed_books:
            print(book.title)

if __name__ == "__main__":
    book1 = Book("Python Basics", "John Doe", 2022)
    book2 = Book("Da Vinci Code", "Samme", 2020)

    user1 = User("Tony")

    user1.borrow_book(book1)
    user1.borrow_book(book2)

    user1.view_borrowed_books()

    user1.return_book(book1)

    user1.view_borrowed_books()