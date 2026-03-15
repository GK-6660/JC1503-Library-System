
import sys
import os
import unittest

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from structures.hash_table import HashTable
from structures.bst import BST
from models.user import User
from models.resource import Book
from utils.exceptions import OutOfStockError

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.users = HashTable()
        self.books = BST()
        
        # Setup initial data
        self.book1 = Book("B001", "Python Programming", 2, "Guido", "123456")
        self.books.insert(self.book1.title, self.book1)
        
        self.user1 = User("U001", "Alice")
        self.users.insert(self.user1.user_id, self.user1)
        
        self.user2 = User("U002", "Bob")
        self.users.insert(self.user2.user_id, self.user2)
        
        self.user3 = User("U003", "Charlie")
        self.users.insert(self.user3.user_id, self.user3)

    def test_borrow_flow(self):
        print("\nTesting borrow flow...")
        # 1. Alice borrows book
        self.book1.borrow_item()
        self.user1.borrow_book(self.book1.title)
        self.assertEqual(self.book1.available_copies, 1)
        self.assertIn(self.book1.title, self.user1.borrowed_items.to_list())
        print("Alice borrowed successfully.")
        
        # 2. Bob borrows book
        self.book1.borrow_item()
        self.user2.borrow_book(self.book1.title)
        self.assertEqual(self.book1.available_copies, 0)
        print("Bob borrowed successfully.")
        
        # 3. Charlie tries to borrow (out of stock)
        with self.assertRaises(OutOfStockError):
            self.book1.borrow_item()
        print("Charlie correctly received OutOfStockError.")
        
        # 4. Charlie joins waitlist
        self.book1.waitlist.enqueue(self.user3.user_id)
        self.assertEqual(self.book1.waitlist.size, 1)
        print("Charlie joined waitlist.")
        
        # 5. Alice returns book -> Charlie gets it
        self.user1.return_book(self.book1.title)
        next_user_id = self.book1.return_item()
        
        self.assertEqual(next_user_id, "U003")
        self.assertEqual(self.book1.available_copies, 0) # Still 0 because Charlie took it
        print(f"Alice returned. Book automatically assigned to {next_user_id}.")
        
        # Simulate system assigning to Charlie
        next_user = self.users.get(next_user_id)
        next_user.borrow_book(self.book1.title)
        self.assertIn(self.book1.title, next_user.borrowed_items.to_list())
        print("Charlie received the book.")

    def test_bst_remove(self):
        print("\nTesting BST remove...")
        self.books.insert("Book A", Book("B1", "Book A", 1, "A", "1"))
        self.books.insert("Book B", Book("B2", "Book B", 1, "B", "2"))
        self.books.insert("Book C", Book("B3", "Book C", 1, "C", "3"))
        
        # Remove leaf (Book A or C depending on insertion order. A < B < C. Root is B? No, root is Book A first?
        # Insert order: Book A (root), Book B (right of A), Book C (right of B).
        # Remove B (middle).
        self.books.remove("Book B")
        with self.assertRaises(Exception): # ItemNotFoundError is raised by search, but remove doesn't raise if not found?
             # My remove implementation returns None if not found, doesn't raise.
             # So search should raise ItemNotFoundError
             self.books.search("Book B")
        
        # Check if A and C are still there
        self.assertIsNotNone(self.books.search("Book A"))
        self.assertIsNotNone(self.books.search("Book C"))
        print("BST remove passed.")

    def test_storage(self):
        print("\nTesting storage serialization...")
        # Create some data
        user = User("U100", "Dave")
        user.borrow_book("Test Book")
        user_dict = user.to_dict()
        
        user_restored = User.from_dict(user_dict)
        self.assertEqual(user_restored.user_id, "U100")
        self.assertEqual(user_restored.name, "Dave")
        self.assertIn("Test Book", user_restored.borrowed_items.to_list())
        print("User serialization passed.")
        
        book = Book("B100", "Test Book", 5, "Author", "ISBN")
        book.available_copies = 3
        book.waitlist.enqueue("U999")
        book_dict = book.to_dict()
        
        book_restored = Book.from_dict(book_dict)
        self.assertEqual(book_restored.title, "Test Book")
        self.assertEqual(book_restored.available_copies, 3)
        self.assertEqual(book_restored.waitlist.dequeue(), "U999")
        print("Book serialization passed.")

if __name__ == '__main__':
    unittest.main()
