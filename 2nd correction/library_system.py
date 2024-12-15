import datetime
class Book:
    '''
    The Book class is used to create instances of books in the system.

    Each book includes the following attributes:
        title: the title of the book (string)
        author: the author of the book (string)
        status: the availability status of the book, which could be "Available" or "Lent"
        donor: the person who donated the book (string)
        borrower: the person who borrowed the book (default: empty string)
    '''
    next_id = 1
    
    def __init__(self, title, author, status, donor,donatetime = None, borrower = None, borrowtime = None,  ):
        self.bookID = Book.next_id
        Book.next_id += 1
        self.title = title
        self.author = author
        self.status = status
        self.donor = donor
        self.borrower = borrower
        self.donatetime = donatetime
        self.borrowtime = borrowtime

    def toString(self):
        """
        Returns a string description of the book with details separated by commas.
        """
        return f"{self.bookID},{self.title},{self.author},{self.status},{self.donor},{self.donatetime},{self.borrower},{self.borrowtime}"

class LibrarySystem:
    MAX_BORROW_LIMIT = 3
    BORROW_TIME_LIMIT = 40
    
    BookList = []  
    DonorScore = {}  
    BookIndex = {}
    
    def build_index():
        """
        Build an index mapping book titles (lowercase) to their corresponding book objects.
        """
        LibrarySystem.BookIndex.clear()
        for book in LibrarySystem.BookList:
            title_key = book.title.lower()
            if title_key not in LibrarySystem.BookIndex:
                LibrarySystem.BookIndex[title_key] = []
            LibrarySystem.BookIndex[title_key].append(book)

    def start():
        """
        Starts the system by loading data from the 'library.csv' and 'donors.csv' files.
        Updates the Book.next_id and initializes the donor scores.
        """
        try:
            with open("library.csv", "r") as book_file:
                records = book_file.read().strip().split("\n")
                max_book_id = 0 

                for record in records:
                    if not record.strip():
                        continue
                    bookID, title, author, status, donor, donatetime, borrower, borrowtime = record.split(",")
                    bookID = int(bookID.strip())
                    max_book_id = max(max_book_id, bookID)
                    donatetime = datetime.datetime.strptime(donatetime.strip(), "%Y-%m-%d").date() if donatetime.strip() and donatetime.strip() != "None" else None
                    borrowtime = datetime.datetime.strptime(borrowtime.strip(), "%Y-%m-%d").date() if borrowtime.strip() and borrowtime.strip() != "None" else None

                    book = Book(
                        title=title.strip(),
                        author=author.strip(),
                        status=status.strip(),
                        donor=donor.strip(),
                        donatetime=donatetime,
                        borrower=borrower.strip() if borrower.strip() else None,
                        borrowtime=borrowtime,
                    )
                    book.bookID = bookID
                    LibrarySystem.BookList.append(book)

                Book.next_id = max_book_id + 1
                print("Library inventory loaded successfully from 'library.csv'.")

        except FileNotFoundError:
            print("No existing library inventory found. Starting with an empty system.")
        except Exception as e:
            print(f"Error loading library inventory: {e}")

        try:
            with open("donors.csv", "r") as donor_file:
                lines = donor_file.read().strip().split("\n")[1:]
                for line in lines:
                    if not line.strip():
                        continue
                    donor, score = line.split(",")
                    LibrarySystem.DonorScore[donor.strip()] = int(score.strip())
                print("Donor scores loaded successfully from 'donors.csv'.")

        except FileNotFoundError:
            print("No existing donor scores found. Starting with an empty donor list.")
        except Exception as e:
            print(f"Error loading donor scores: {e}")
        LibrarySystem.build_index()

        print("\nLibrary System has been successfully initialized.")
        
    def exit():
        """
        Exits the system by saving the current inventory and donor scores to files.
        Clears all global data structures to ensure a clean shutdown.
        """
        try:
            with open("library.csv", "w") as book_file:
                for book in LibrarySystem.BookList:
                    book_file.write(book.toString() + "\n")
            print("Library inventory has been successfully saved to 'library.csv'.")
        except Exception as e:
            print(f"Error saving library inventory: {e}")

        try:
            with open("donors.csv", "w") as donor_file:
                donor_file.write("Donor,Score\n")
                for donor, score in LibrarySystem.DonorScore.items():
                    donor_file.write(f"{donor},{score}\n")
            print("Donor scores have been successfully saved to 'donors.csv'.")
        except Exception as e:
            print(f"Error saving donor scores: {e}")
        LibrarySystem.BookList.clear()
        LibrarySystem.DonorScore.clear()
        LibrarySystem.BookIndex.clear()

        print("\nLibrary System has been closed.\n")

    def donate(book):
        """
        Adds a donated book to the system and updates the donor's score.
        """
        # Add book to system
        LibrarySystem.BookList.append(book)
        title_key = book.title.lower()
        if title_key not in LibrarySystem.BookIndex:
            LibrarySystem.BookIndex[title_key] = []
        LibrarySystem.BookIndex[title_key].append(book)

        # Update donor score
        book.donatetime = datetime.date.today()
        donor_name = book.donor
        LibrarySystem.DonorScore[donor_name] = LibrarySystem.DonorScore.get(donor_name, 0) + 1

        print(f"New book '{book.title}' donated by {book.donor} on {book.donatetime}. Current donor score: {LibrarySystem.DonorScore[donor_name]}")
        
    def borrowBook(title, borrower_name):
        """
        Allows a user to borrow a book by title and borrower name.
        """
        title_key = title.lower()
        matching_books = LibrarySystem.BookIndex.get(title_key, [])

        if not matching_books:
            return f"No books found with the title '{title}'. Please check the title and try again.", None

        available_books = [book for book in matching_books if book.status == "Available"]
        if not available_books:
            return f"No available copies of '{title}' at the moment.", None

        if not borrower_name:
            return "Borrower name cannot be empty. Please try again.", None

        user_borrowed_books = [b for b in LibrarySystem.BookList if b.borrower == borrower_name]
        if len(user_borrowed_books) >= LibrarySystem.MAX_BORROW_LIMIT:
            return f"You have reached the maximum borrow limit of {LibrarySystem.MAX_BORROW_LIMIT}. Please return a book before borrowing another.", None

        # Borrow the first available book
        book = available_books[0]
        book.status = "Lent"
        book.borrower = borrower_name
        book.borrowtime = datetime.date.today()

        return f"'{book.title}' (ID: {book.bookID}) has been successfully borrowed by {borrower_name} on {book.borrowtime}.", book
            
        
    
    def returnBook(title):
        """
        Allows a user to return a book by title. If multiple books have the same title,
        display all matching books with their IDs and let the user select one to return.
        """
        title_key = title.lower()
        matching_books = LibrarySystem.BookIndex.get(title_key, [])

        if not matching_books:
            print(f"No books found with the title '{title}'.")
            return

        print(f"Found {len(matching_books)} book(s) with the title '{title}':")
        print(f"\n{'ID':<5}{'Title':<30}{'Author':<20}{'Status':<15}{'Borrower':<20}{'BorrowTime':<20}")
        print("-" * 120)
        for book in matching_books:
            print(f"{book.bookID:<5}{book.title:<30}{book.author:<20}{book.status:<15}{book.borrower or '/':<20}{book.borrowtime or '/':<20}")

        try:
            book_id = int(input("\nEnter the book ID you want to return: ").strip())
            id_to_book = {book.bookID: book for book in matching_books} 
            book = id_to_book.get(book_id) 

            if book:
                if book.status == "Lent":
                    print(f"'{book.title}' (ID: {book.bookID}) has been successfully returned by {book.borrower}.")
                    book.status = "Available"
                    book.borrower = None
                    book.borrowtime = None
                    return
                else:
                    print(f"'{book.title}' (ID: {book.bookID}) is already available in the library.")
            else:
                print("Invalid book ID. No changes made.")
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
            
    def display():
        """
        Displays all books in the inventory, including their status and donor information.
        """
        if not LibrarySystem.BookList:
            print("The library inventory is empty.")
            return

        print("\nChoose a type of display:")
        print("Enter 1 to display all books")
        print("Enter 2 to display lent books")
        print("Enter 3 to display available books")

        try:
            chosen = int(input("Your choice is: ").strip())
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        print(f"\n{'ID':<5}{'Title':<30}{'Author':<20}{'Status':<15}{'Donor':<20}{'DonateTime':<20}{'Borrower':<20}{'BorrowTime':<20}")
        print("-" * 150)
        for book in LibrarySystem.BookList:
            donatetime = book.donatetime or "/"
            borrowtime = book.borrowtime or "/"
            borrower = book.borrower or "/"

            if chosen == 1 or (chosen == 2 and book.status == "Lent") or (chosen == 3 and book.status == "Available"):
                print(f"{book.bookID:<5}{book.title:<30}{book.author:<20}{book.status:<15}{book.donor:<20}{donatetime:<20}{borrower:<20}{borrowtime:<20}")

        if LibrarySystem.DonorScore:
            print("\nDonor Leaderboard (Sorted by Contributions):")
            print(f"{'Donor':<20}{'Score':<10}")
            print("-" * 30)
            for donor, score in sorted(LibrarySystem.DonorScore.items(), key=lambda x: x[1], reverse=True):
                print(f"{donor:<20}{score:<10}")
        else:
            print("\nNo donors in the leaderboard yet.")
            
    def viewUserRecords(user_name):
        """
        Displays all books currently borrowed by the given user.
        """
        borrowed_books = [book for book in LibrarySystem.BookList if book.borrower == user_name]

        if not borrowed_books:
            print(f"No books currently borrowed by {user_name}.")
            return

        print(f"Books borrowed by {user_name}:")
        print(f"\n{'ID':<5}{'Title':<30}{'Author':<20}{'BorrowTime':<20}")
        print("-" * 75)
        for book in borrowed_books:
            print(f"{book.bookID:<5}{book.title:<30}{book.author:<20}{book.borrowtime}")

    def displayOverdueBooks():
        """
        Displays all books that have been borrowed longer than the allowed time limit.
        """
        today = datetime.date.today()
        overdue_books = []

        for book in LibrarySystem.BookList:
            if book.status == "Lent" and book.borrowtime:
                borrow_duration = (today - book.borrowtime).days
                if borrow_duration > BORROW_TIME_LIMIT: # type: ignore
                    overdue_books.append((book, borrow_duration))

        if not overdue_books:
            print("No overdue books in the library.")
            return

        print("Overdue books:")
        print(f"\n{'ID':<5}{'Title':<30}{'Author':<20}{'Borrower':<20}{'BorrowTime':<20}{'Days Overdue':<15}")
        print("-" * 120)
        for book, duration in overdue_books:
            print(f"{book.bookID:<5}{book.title:<30}{book.author:<20}{book.borrower:<20}{book.borrowtime:<20}{duration:<15}")
                