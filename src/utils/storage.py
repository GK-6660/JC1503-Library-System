import json
import os
from structures.hash_table import HashTable
from structures.bst import BST
from models.user import User
from models.resource import Book, Magazine

DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/library_data.json")

class Storage:
    @staticmethod
    def save_data(users_data_to_save, books_data_to_save):
        data_to_dump = {}
        data_to_dump["users"] = []
        for user_obj in users_data_to_save.to_list():
            data_to_dump["users"].append(user_obj.to_dict())
            
        data_to_dump["books"] = []
        for book_obj in books_data_to_save.to_list():
            data_to_dump["books"].append(book_obj.to_dict())
        
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        file_handle = open(DATA_FILE, 'w', encoding='utf-8')
        json.dump(data_to_dump, file_handle, indent=4)
        file_handle.close()
        print("Data saved to file: " + DATA_FILE)

    @staticmethod
    def generate_initial_data(user_hash_table, book_bst_tree):
        print("Starting to generate a large initial dataset for the library system...")
        for i in range(1, 31):
            new_user_instance = User(f"U{i:03}", f"User_Name_{i}")
            user_hash_table.insert(new_user_instance.user_id, new_user_instance)
            print(f"Generated user: {new_user_instance.name}")

        for i in range(1, 41):
            new_book_instance = Book(f"B{i:03}", f"Book_Title_{i}", 5, f"Author_{i}", f"ISBN-{i}")
            book_bst_tree.insert(new_book_instance.title, new_book_instance)
            print(f"Generated book: {new_book_instance.title}")
            
        for i in range(1, 21):
            new_magazine_instance = Magazine(f"M{i:03}", f"Magazine_Title_{i}", 3, f"Issue_{i}")
            book_bst_tree.insert(new_magazine_instance.title, new_magazine_instance)
            print(f"Generated magazine: {new_magazine_instance.title}")
            
        user_one = user_hash_table.get("U001")
        book_one_node = book_bst_tree.search("Book_Title_1")
        book_one = book_one_node.value
        book_one.borrow_item()
        user_one.borrow_book("Book_Title_1")
        print(f"User {user_one.name} borrowed {book_one.title}.")
        
        user_two = user_hash_table.get("U002")
        magazine_one_node = book_bst_tree.search("Magazine_Title_1")
        magazine_one = magazine_one_node.value
        magazine_one.borrow_item()
        user_two.borrow_book("Magazine_Title_1")
        print(f"User {user_two.name} borrowed {magazine_one.title}.")

        Storage.save_data(user_hash_table, book_bst_tree)
        print("Initial dataset generation and saving completed.")

    @staticmethod
    def load_data():
        user_hash_table_loaded = HashTable()
        book_bst_tree_loaded = BST()

        if not os.path.exists(DATA_FILE):
            print("Data file not found. Generating initial data...")
            Storage.generate_initial_data(user_hash_table_loaded, book_bst_tree_loaded)
            return user_hash_table_loaded, book_bst_tree_loaded
        
        try:
            file_to_read = open(DATA_FILE, 'r', encoding='utf-8')
            loaded_data_dict = json.load(file_to_read)
            file_to_read.close()
            print("Data loaded from file: " + DATA_FILE)
                
            user_list_from_data = loaded_data_dict.get("users", [])
            for user_dict_data in user_list_from_data:
                user_object = User.from_dict(user_dict_data)
                user_hash_table_loaded.insert(user_object.user_id, user_object)
                
            book_list_from_data = loaded_data_dict.get("books", [])
            for book_dict_data in book_list_from_data:
                item_type_str = book_dict_data.get("type")
                if item_type_str == "Book":
                    item_object = Book.from_dict(book_dict_data)
                elif item_type_str == "Magazine":
                    item_object = Magazine.from_dict(book_dict_data)
                else:
                    print(f"Warning: Unknown item type '{item_type_str}' encountered during load.")
                    continue
                book_bst_tree_loaded.insert(item_object.title, item_object)
                
        except Exception as e:
            print(f"An error occurred during data loading: {e}")
            pass
            
        return user_hash_table_loaded, book_bst_tree_loaded