import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
src_dir = os.path.join(project_dir, "src")

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from src.structures.tree import CategoryTree
    from src.models.resource import Book
    from src.models.user import User
    
    exceptions_found = False
    
    item_not_found_classes = set()
    duplicate_item_classes = set()
    out_of_stock_classes = set()

    try:
        from utils.exceptions import (
            ItemNotFoundError as Ex1,
            DuplicateItemError as Ex2,
            OutOfStockError as Ex3,
        )
        item_not_found_classes.add(Ex1)
        duplicate_item_classes.add(Ex2)
        out_of_stock_classes.add(Ex3)
        exceptions_found = True
    except ImportError:
        pass

    try:
        from src.utils.exceptions import (
            ItemNotFoundError as Ex1,
            DuplicateItemError as Ex2,
            OutOfStockError as Ex3,
        )
        item_not_found_classes.add(Ex1)
        duplicate_item_classes.add(Ex2)
        out_of_stock_classes.add(Ex3)
        exceptions_found = True
    except ImportError:
        pass
        
    if not exceptions_found:
        raise ImportError("Cannot import utils.exceptions, please check path settings")
        
    ItemNotFoundError = tuple(item_not_found_classes)
    DuplicateItemError = tuple(duplicate_item_classes)
    OutOfStockError = tuple(out_of_stock_classes)

    Exception_available = True
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current File: {__file__}")
    print(f"Project Directory: {project_dir}")
    print(f"sys.path: {sys.path}")
    raise


class TestCategoryTree(unittest.TestCase):

    def setUp(self):
        self.tree = CategoryTree("Library")

    def test_add_root_category(self):
        result = self.tree.add_category("Library", "Science")
        self.assertTrue(result)
        self.assertIsNotNone(self.tree.root)
        self.assertEqual(self.tree.root.category_name, "Library")
        self.assertIsNotNone(self.tree.find_category("Science"))

    def test_add_child_category(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")
        self.tree.add_category("Science", "Physics")

        science_node = self.tree.find_category("Science")
        child_count = len(science_node.children)
        self.assertEqual(child_count, 2)

    def test_add_duplicate_category(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")

        with self.assertRaises(DuplicateItemError):
            self.tree.add_category("Science", "Mathematics")

    def test_add_category_with_nonexistent_parent(self):
        with self.assertRaises(ItemNotFoundError):
            self.tree.add_category("Nonexistent Category", "Mathematics")

    def test_search_category(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")
        self.tree.add_category("Mathematics", "Calculus")

        node = self.tree.find_category("Science")
        self.assertEqual(node.category_name, "Science")

        node = self.tree.find_category("Mathematics")
        self.assertEqual(node.category_name, "Mathematics")

        node = self.tree.find_category("Calculus")
        self.assertEqual(node.category_name, "Calculus")

        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("Chemistry")

    def test_get_path(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")
        self.tree.add_category("Mathematics", "Calculus")
        self.tree.add_category("Calculus", "Differentiation")

        path = self.tree.get_path("Differentiation")
        self.assertEqual(path, ["Library", "Science", "Mathematics", "Calculus", "Differentiation"])

        with self.assertRaises(ItemNotFoundError):
            self.tree.get_path("Nonexistent Category")

    def test_get_all_categories(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")
        self.tree.add_category("Science", "Physics")
        self.tree.add_category("Library", "Arts")
        self.tree.add_category("Arts", "Literature")
        self.tree.add_category("Library", "Engineering")

        all_cats = self.tree.get_all_categories()
        expected_cats = ["Library", "Science", "Mathematics", "Physics", "Arts", "Literature", "Engineering"]
        self.assertEqual(len(all_cats), 7)
        for cat in expected_cats:
            self.assertIn(cat, all_cats)

    def test_remove_category(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Science", "Mathematics")
        self.tree.add_category("Mathematics", "Calculus")

        result = self.tree.remove_category("Calculus")
        self.assertTrue(result)
        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("Calculus")

        result = self.tree.remove_category("Mathematics")
        self.assertTrue(result)
        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("Mathematics")

        result = self.tree.remove_category("Nonexistent")
        self.assertFalse(result)

    def test_move_category(self):
        self.tree.add_category("Library", "Science")
        self.tree.add_category("Library", "Arts")
        self.tree.add_category("Science", "Mathematics")

        result = self.tree.move_category("Mathematics", "Arts")
        self.assertTrue(result)

        path = self.tree.get_path("Mathematics")
        self.assertEqual(path, ["Library", "Arts", "Mathematics"])

        result = self.tree.move_category("Mathematics", "Nonexistent")
        self.assertFalse(result)

    def test_nested_categories_depth(self):
        self.tree.add_category("Library", "Level1")
        current = "Level1"
        for i in range(2, 7):
            name = f"Level{i}"
            self.tree.add_category(current, name)
            current = name

        path = self.tree.get_path("Level6")
        expected = ["Library", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6"]
        self.assertEqual(path, expected)


class TestResourceModels(unittest.TestCase):

    def test_book_creation(self):
        book = Book("B001", "Python Programming", 5, "Guido", "978-0-123456-47-2")
        self.assertEqual(book.resource_id, "B001")
        self.assertEqual(book.title, "Python Programming")
        self.assertEqual(book.total_copies, 5)
        self.assertEqual(book.available_copies, 5)
        self.assertEqual(book.author, "Guido")

    def test_borrow_return_flow(self):
        book = Book("B001", "Python Programming", 2, "Guido", "123")
        
        book.borrow_item()
        self.assertEqual(book.available_copies, 1)
        
        book.borrow_item()
        self.assertEqual(book.available_copies, 0)
        
        with self.assertRaises(OutOfStockError):
            book.borrow_item()
            
        book.return_item()
        self.assertEqual(book.available_copies, 1)

    def test_waitlist(self):
        book = Book("B001", "Popular Book", 1, "Author", "123")
        book.borrow_item()
        
        book.waitlist.enqueue("User1")
        book.waitlist.enqueue("User2")
        
        notified_user = book.return_item()
        self.assertEqual(notified_user, "User1")
        self.assertEqual(book.available_copies, 0)
        
        notified_user = book.return_item()
        self.assertEqual(notified_user, "User2")
        self.assertEqual(book.available_copies, 0)
        
        notified_user = book.return_item()
        self.assertIsNone(notified_user)
        self.assertEqual(book.available_copies, 1)


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        from src.structures.linked_list import DoublyLinkedList
        self.dll = DoublyLinkedList()

    def test_append_and_len(self):
        self.dll.append("A")
        self.dll.append("B")
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(self.dll.to_list(), ["A", "B"])

    def test_remove(self):
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        
        self.assertTrue(self.dll.remove("B"))
        self.assertEqual(self.dll.to_list(), ["A", "C"])
        self.assertEqual(len(self.dll), 2)
        
        self.assertTrue(self.dll.remove("A"))
        self.assertEqual(self.dll.to_list(), ["C"])
        
        self.assertTrue(self.dll.remove("C"))
        self.assertEqual(self.dll.to_list(), [])
        self.assertEqual(len(self.dll), 0)
        
        self.assertFalse(self.dll.remove("X"))


class TestStack(unittest.TestCase):

    def setUp(self):
        from src.structures.stack import Stack
        self.stack = Stack()

    def test_push_pop(self):
        self.stack.push("Action1")
        self.stack.push("Action2")
        
        self.assertEqual(self.stack.pop(), "Action2")
        self.assertEqual(self.stack.pop(), "Action1")
        self.assertIsNone(self.stack.pop())


class TestHashTable(unittest.TestCase):

    def setUp(self):
        from src.structures.hash_table import HashTable
        self.ht = HashTable(capacity=10)

    def test_insert_get(self):
        user = User("U001", "Alice")
        self.ht.insert("U001", user)
        
        retrieved = self.ht.get("U001")
        self.assertEqual(retrieved.name, "Alice")

    def test_collision(self):
        user1 = User("AB", "User1")
        user2 = User("BA", "User2")
        
        self.ht.insert("AB", user1)
        self.ht.insert("BA", user2)
        
        self.assertEqual(self.ht.get("AB").name, "User1")
        self.assertEqual(self.ht.get("BA").name, "User2")

    def test_remove(self):
        user = User("U001", "Alice")
        self.ht.insert("U001", user)
        
        self.ht.remove("U001")
        with self.assertRaises(ItemNotFoundError):
            self.ht.get("U001")

    def test_duplicate_insert(self):
        user = User("U001", "Alice")
        self.ht.insert("U001", user)
        with self.assertRaises(DuplicateItemError):
            self.ht.insert("U001", user)


class TestQueue(unittest.TestCase):

    def setUp(self):
        from src.structures.queue import Queue
        self.queue = Queue()

    def test_enqueue_dequeue(self):
        self.queue.enqueue("User1")
        self.queue.enqueue("User2")
        
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.dequeue(), "User1")
        self.assertEqual(self.queue.dequeue(), "User2")
        self.assertTrue(self.queue.is_empty())


class TestBST(unittest.TestCase):

    def setUp(self):
        from src.structures.bst import BST
        from src.models.resource import Book
        self.bst = BST()
        self.book1 = Book("B1", "Python Basics", 5, "Author A", "ISBN1")
        self.book2 = Book("B2", "Advanced Python", 3, "Author B", "ISBN2")
        self.book3 = Book("B3", "Data Structures", 4, "Author C", "ISBN3")

    def test_insert_search(self):
        self.bst.insert("Python Basics", self.book1)
        self.bst.insert("Advanced Python", self.book2)
        
        found = self.bst.search("Python Basics")
        self.assertEqual(found.title, "Python Basics")
        
        found = self.bst.search("Advanced Python")
        self.assertEqual(found.title, "Advanced Python")
        
        with self.assertRaises(ItemNotFoundError):
            self.bst.search("Nonexistent Book")

    def test_update_existing(self):
        self.bst.insert("Python Basics", self.book1)
        new_book = Book("B1-New", "Python Basics", 10, "Author A", "ISBN1")
        self.bst.insert("Python Basics", new_book)
        
        found = self.bst.search("Python Basics")
        self.assertEqual(found.total_copies, 10)


class TestIntegration(unittest.TestCase):

    def setUp(self):
        from src.structures.hash_table import HashTable
        from src.structures.bst import BST
        from src.models.user import User
        from src.models.resource import Book
        
        self.users = HashTable()
        self.books = BST()
        
        self.user = User("U001", "Alice")
        self.users.insert("U001", self.user)
        
        self.book = Book("B001", "Python Guide", 2, "Guido", "12345")
        self.books.insert("Python Guide", self.book)

    def test_borrow_flow(self):
        user = self.users.get("U001")
        book = self.books.search("Python Guide")
        
        book.borrow_item()
        user.borrow_book("Python Guide")
        
        self.assertEqual(book.available_copies, 1)
        self.assertIn("Python Guide", user.borrowed_items.to_list())
        
        book.borrow_item()
        user.borrow_book("Python Guide")
        self.assertEqual(book.available_copies, 0)
        
        with self.assertRaises(OutOfStockError):
            book.borrow_item()

    def test_return_flow(self):
        user = self.users.get("U001")
        book = self.books.search("Python Guide")
        
        book.borrow_item()
        user.borrow_book("Python Guide")
        
        book.return_item()
        user.return_book("Python Guide")
        
        self.assertEqual(book.available_copies, 2)
        self.assertNotIn("Python Guide", user.borrowed_items.to_list())


def create_test_suite():
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()

    test_classes = [
        TestCategoryTree,
        TestResourceModels,
        TestLinkedList,
        TestStack,
        TestHashTable,
        TestQueue,
        TestBST,
        TestIntegration,
    ]

    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))
    return suite


def run_tests():
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'=' * 60}")
    print(" Test Report")
    print(f"{'=' * 60}")
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"{'=' * 60}")

    if result.skipped:
        print("\n Skipped Tests (Waiting for other team members):")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")

    return result


if __name__ == "__main__":
    run_tests()
