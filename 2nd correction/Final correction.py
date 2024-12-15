import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from library_system import LibrarySystem, Book


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        
        LibrarySystem.start()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_menu()

    def clear_frame(self):
        """Clear Frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        """Main Menu"""
        self.clear_frame()
        tk.Label(self.main_frame, text="Welcome to the Library Management System",
                 font=("Arial", 18)).pack(pady=20)

        tk.Button(self.main_frame, text="Donate Book", command=self.donate_book, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Borrow Book", command=self.borrow_book, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Return Book", command=self.return_book, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Display All Books", command=self.display_all_books, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="View User Borrowed Records", command=self.view_user_records_gui, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="View Overdue Books", command=self.display_overdue_books_gui, width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_system, width=20).pack(pady=10)

    def donate_book(self):
        """Donate Book"""
        self.clear_frame()
        tk.Label(self.main_frame, text="Donate a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Title").pack()
        title_entry = tk.Entry(self.main_frame, width=30)
        title_entry.pack()

        tk.Label(self.main_frame, text="Author").pack()
        author_entry = tk.Entry(self.main_frame, width=30)
        author_entry.pack()

        tk.Label(self.main_frame, text="Donor").pack()
        donor_entry = tk.Entry(self.main_frame, width=30)
        donor_entry.pack()

        def submit_donation():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            donor = donor_entry.get().strip()

            if not title or not author or not donor:
                messagebox.showerror("Error", "All fields are required!")
                return

            donatetime = datetime.date.today().strftime("%Y-%m-%d")
            book = Book(title, author, "Available", donor, donatetime)
            LibrarySystem.donate(book)
            messagebox.showinfo("Success", f"'{title}' has been donated by {donor}.")
            self.main_menu()

        tk.Button(self.main_frame, text="Donate", command=submit_donation, width=15).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_system, width=15).pack(pady=10)

    def borrow_book(self):
        """
        GUI interface for borrowing a book.
        """
        self.clear_frame()

        tk.Label(self.main_frame, text="Borrow a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Title").pack()
        title_entry = tk.Entry(self.main_frame, width=30)
        title_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Borrower Name").pack()
        borrower_entry = tk.Entry(self.main_frame, width=30)
        borrower_entry.pack(pady=5)

        def submit_borrow():
            title = title_entry.get().strip()
            borrower_name = borrower_entry.get().strip()
            message, book = LibrarySystem.borrowBook(title, borrower_name)

            if book:
                messagebox.showinfo("Borrow Successful", message)
            else:
                messagebox.showwarning("Borrow Failed", message)
            self.main_menu()

        tk.Button(self.main_frame, text="Borrow", command=submit_borrow, width=15).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_system, width=15).pack(pady=10)

    def return_book(self):
        """Return Book"""
        self.clear_frame()
        tk.Label(self.main_frame, text="Return a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Title").pack()
        title_entry = tk.Entry(self.main_frame, width=30)
        title_entry.pack()

        def return_selected():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Title is required!")
                return

            LibrarySystem.returnBook(title)
            messagebox.showinfo("Success", f"The book '{title}' has been returned.")
            self.main_menu()

        tk.Button(self.main_frame, text="Return", command=return_selected, width=15).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_system, width=15).pack(pady=10)

    def display_all_books(self):
        """Display_all_books"""
        self.clear_frame()
        tk.Label(self.main_frame, text="All Books and Donor Scores", font=("Arial", 16)).pack(pady=10)

        if not LibrarySystem.BookList:
            messagebox.showinfo("No Books", "No books in the library.")
            self.main_menu()
            return
        
        columns = ("ID", "Title", "Author", "Status", "Donor", "Donate Time", "Borrower", "Borrow Time")
        tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        for book in LibrarySystem.BookList:
            tree.insert("", tk.END, values=(
                book.bookID,
                book.title,
                book.author,
                book.status,
                book.donor,
                book.donatetime,
                book.borrower or "None",
                book.borrowtime or "None"
            ))
            
        if LibrarySystem.DonorScore:
            tk.Label(self.main_frame, text="\nDonor Scores", font=("Arial", 14)).pack(pady=10)

            donor_columns = ("Donor", "Score")
            donor_tree = ttk.Treeview(self.main_frame, columns=donor_columns, show="headings")
            for col in donor_columns:
                donor_tree.heading(col, text=col)
                donor_tree.column(col, width=150)
            donor_tree.pack(fill=tk.BOTH, expand=True)

            sorted_donors = sorted(LibrarySystem.DonorScore.items(), key=lambda x: x[1], reverse=True)
            for donor, score in sorted_donors:
                donor_tree.insert("", tk.END, values=(donor, score))
        else:
            tk.Label(self.main_frame, text="No donor scores available.", font=("Arial", 12)).pack()
            
        tk.Button(self.main_frame, text="Return to menu", command=self.main_menu).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_system).pack(pady=10)
        
    def view_user_records_gui(self):
        """View user's record"""
        self.clear_frame()
        tk.Label(self.main_frame, text="View User Borrowed Records", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Enter User Name").pack()
        user_name_entry = ttk.Entry(self.main_frame, width=30)
        user_name_entry.pack()

        def show_records():
            user_name = user_name_entry.get().strip()
            if not user_name:
                messagebox.showerror("Error", "User name cannot be empty.")
                return

            borrowed_books = [book for book in LibrarySystem.BookList if book.borrower == user_name]
            if not borrowed_books:
                messagebox.showinfo("No Records", f"No books currently borrowed by {user_name}.")
                return

            record_window = tk.Toplevel(self.root)
            record_window.title(f"Borrowed Records for {user_name}")
            record_window.geometry("800x400")

            tk.Label(record_window, text=f"Books borrowed by {user_name}:", font=("Arial", 14)).pack(pady=10)
            columns = ("ID", "Title", "Author", "BorrowTime")
            tree = ttk.Treeview(record_window, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=200)
            tree.pack(fill=tk.BOTH, expand=True)

            for book in borrowed_books:
                tree.insert("", tk.END, values=(book.bookID, book.title, book.author, book.borrowtime))

            ttk.Button(record_window, text="Close", command=record_window.destroy).pack(pady=10)

        ttk.Button(self.main_frame, text="Search", command=show_records).pack(pady=10)
        ttk.Button(self.main_frame, text="Return to Menu", command=self.main_menu).pack(pady=10)
    
    def display_overdue_books_gui(self):
        """overdue book"""
        self.clear_frame()
        tk.Label(self.main_frame, text="Overdue Books", font=("Arial", 16)).pack(pady=10)
        
        today = datetime.date.today()
        overdue_books = []

        for book in LibrarySystem.BookList:
            if book.status == "Lent" and book.borrowtime:
                borrow_duration = (today - book.borrowtime).days
                if borrow_duration > LibrarySystem.BORROW_TIME_LIMIT: 
                    overdue_books.append((book, borrow_duration))

        if not overdue_books:
            messagebox.showinfo("No Overdue Books", "No overdue books in the library.")
            self.main_menu()
            return

        columns = ("ID", "Title", "Author", "Borrower", "BorrowTime", "Days Overdue")
        tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        for book, duration in overdue_books:
            tree.insert("", tk.END, values=(
                book.bookID,
                book.title,
                book.author,
                book.borrower,
                book.borrowtime,
                duration
            ))

        tk.Button(self.main_frame, text="Return to Menu", command=self.main_menu).pack(pady=10)
            
    def exit_system(self):
        """Exit System"""
        try:
            LibrarySystem.exit()
            if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
                self.root.destroy() 
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exiting: {e}")

#start
if __name__ == "__main__":
    root = tk.Tk()
    gui = LibraryGUI(root)
    root.mainloop()