import sys
from utils.storage import Storage
from structures.hash_table import HashTable
from structures.bst import BST
from structures.stack import Stack
from models.user import User
from models.resource import Book, Magazine
from utils.exceptions import LibraryBaseException, ItemNotFoundError, DuplicateItemError, OutOfStockError

class LibSys:
    def __init__(self):
        print("Loading...")
        self.users, self.books = Storage.load_data()
        self.history_stack = Stack()
        
        self.is_running = True
        self.temp_counter = 0

    def run(self):
        is_system_active = self.is_running
        while is_system_active == True:
            self.temp_counter = self.temp_counter + 1 
            self.print_menu()
            user_input_choice = input("Enter choice: ").strip()
            
            if user_input_choice == "1":
                self.add_user()
            elif user_input_choice == "2":
                self.add_book()
            elif user_input_choice == "3":
                self.borrow_item()
            elif user_input_choice == "4":
                self.return_item()
            elif user_input_choice == "7":
                self.delete_user()
            elif user_input_choice == "8":
                self.delete_book()
            elif user_input_choice == "5":
                self.undo_last_action()
            elif user_input_choice == "6":
                self.show_history()
            elif user_input_choice == "0":
                self.exit_system()
                is_system_active = False 
            else:
                print("Wrong choice!")

    def print_menu(self):
        print("\n" + "=" * 30)
        print("  Library System  ")
        print("=" * 30)
        print("1. Add user")
        print("2. Add book")
        print("3. Borrow book")
        print("4. Return book")
        print("7. Delete user")
        print("8. Delete book")
        print("5. Undo")
        print("6. Show History")
        print("0. Exit")
        print("=" * 30)

    def add_user(self):
        user_id_input = input("ID: ")
        user_name_input = input("Name: ")
        
        if user_id_input == "" or user_name_input == "":
             print("Empty input! Try again.")
             return

        new_user_obj = User(user_id_input, user_name_input)
        self.users.insert(user_id_input, new_user_obj)
        self.history_stack.push({"action_type": "add_user", "user_id": user_id_input})
        print("User added ok!")

    def add_book(self):
        item_type_choice_str = input("1. Book  2. Mag: ").strip()
        
        resource_id_val = input("ID: ")
        item_title_val = input("Title: ")
        total_copies_num = int(input("Total: "))
            
        if item_type_choice_str == "1":
            book_author_name = input("Author: ")
            book_isbn_code = input("ISBN: ")
            new_item_obj = Book(resource_id_val, item_title_val, total_copies_num, book_author_name, book_isbn_code)
        elif item_type_choice_str == "2":
            magazine_issue_num = input("Issue: ")
            new_item_obj = Magazine(resource_id_val, item_title_val, total_copies_num, magazine_issue_num)
        else:
            print("Invalid type. No item added.")
            return

        self.books.insert(item_title_val, new_item_obj)
        self.history_stack.push({"action_type": "add_book", "item_title": item_title_val})
        print("Item added successfully!")

    def borrow_item(self):
        user_id_to_borrow = input("User ID: ")
        item_title_to_borrow = input("Title: ")
        
        try:
            current_user_obj = self.users.get(user_id_to_borrow)
            current_book_obj = self.books.search(item_title_to_borrow)
            
            current_book_obj.borrow_item()
            current_user_obj.borrow_book(item_title_to_borrow)
            
            self.history_stack.push({
                "action_type": "borrow", 
                "user_id": user_id_to_borrow, 
                "item_title": item_title_to_borrow
            })
            print("Borrow operation successful!")
            
        except OutOfStockError as e:
            print(f"Error: {e}. Item is out of stock.")
            user_answer_queue = input("Do you want to join the waitlist? (y/n): ").strip()
            if user_answer_queue == 'y':
                try:
                    book_for_queue = self.books.search(item_title_to_borrow) 
                    book_for_queue.waitlist.enqueue(user_id_to_borrow)
                    print("You have been added to the waitlist.")
                except ItemNotFoundError:
                    print("Could not add to waitlist, item not found.")
        except ItemNotFoundError as e:
            print(f"Error: {e}. User or item not found.")

    def return_item(self):
        user_id_return = input("User ID: ")
        item_title_return = input("Title: ")
        
        try:
            current_user_for_return = self.users.get(user_id_return)
            current_book_for_return = self.books.search(item_title_return)
            
            return_successful = current_user_for_return.return_book(item_title_return)
            if return_successful == True: 
                next_borrower_id_from_queue = current_book_for_return.return_item()
                print("Item returned successfully!")
                
                if next_borrower_id_from_queue != None: 
                    print(f"Book given to new user: {next_borrower_id_from_queue}!")
                    try:
                        next_user_from_queue = self.users.get(next_borrower_id_from_queue)
                        next_user_from_queue.borrow_book(item_title_return)
                    except LibraryBaseException:
                        print("Error giving book to next user.")
                        pass
                        
                self.history_stack.push({
                    "action_type": "return", 
                    "user_id": user_id_return, 
                    "item_title": item_title_return
                })
            else:
                print("User did not borrow this item.")

        except ItemNotFoundError:
            print("Error: User or item not found for return.")

    def delete_user(self):
        user_id_to_delete = input("ID: ").strip()
        if user_id_to_delete == "":
            print("Empty input! Try again.")
            return

        try:
            user_obj_to_delete = self.users.get(user_id_to_delete)
            borrowed_count_num = len(user_obj_to_delete.borrowed_items)
            if borrowed_count_num > 0:
                print("Cannot delete user: user still has borrowed items.")
                return

            self.users.remove(user_id_to_delete)
            self.history_stack.push({
                "action_type": "delete_user",
                "user_id": user_id_to_delete,
                "user_obj": user_obj_to_delete
            })
            print("User deleted ok!")
        except ItemNotFoundError:
            print("Error: User not found.")
        except LibraryBaseException as e:
            print(f"Error: {e}")

    def delete_book(self):
        item_title_to_delete = input("Title: ").strip()
        if item_title_to_delete == "":
            print("Empty input! Try again.")
            return

        try:
            item_obj_to_delete = self.books.search(item_title_to_delete)

            if item_obj_to_delete.available_copies != item_obj_to_delete.total_copies:
                print("Cannot delete book: item is currently borrowed.")
                return

            if item_obj_to_delete.waitlist.is_empty() == False:
                print("Cannot delete book: waitlist is not empty.")
                return

            self.books.remove(item_title_to_delete)
            self.history_stack.push({
                "action_type": "delete_book",
                "item_title": item_title_to_delete,
                "item_obj": item_obj_to_delete
            })
            print("Book deleted ok!")
        except ItemNotFoundError:
            print("Error: Book not found.")
        except LibraryBaseException as e:
            print(f"Error: {e}")

    def undo_last_action(self):
        last_action_data = self.history_stack.pop()
        if last_action_data == None:
            print("No actions to undo in history.")
            return
        
        action_type_to_undo = last_action_data.get("action_type")
        
        try:
            if action_type_to_undo == "add_user":
                user_id_to_remove = last_action_data["user_id"]
                self.users.remove(user_id_to_remove)
                print(f"User {user_id_to_remove} removed as part of undo.")
                
            elif action_type_to_undo == "add_book":
                item_title_to_remove = last_action_data["item_title"]
                self.books.remove(item_title_to_remove)
                print(f"Book {item_title_to_remove} removed as part of undo.")
                
            elif action_type_to_undo == "delete_user":
                user_obj_to_restore = last_action_data["user_obj"]
                self.users.insert(user_obj_to_restore.user_id, user_obj_to_restore)
                print(f"User {user_obj_to_restore.user_id} restored as part of undo.")

            elif action_type_to_undo == "delete_book":
                item_obj_to_restore = last_action_data["item_obj"]
                self.books.insert(item_obj_to_restore.title, item_obj_to_restore)
                print(f"Book {item_obj_to_restore.title} restored as part of undo.")

            elif action_type_to_undo == "borrow":
                user_id_undo_borrow = last_action_data["user_id"]
                item_title_undo_borrow = last_action_data["item_title"]
                
                user_obj_undo = self.users.get(user_id_undo_borrow)
                book_obj_undo = self.books.search(item_title_undo_borrow)
                
                if user_obj_undo.return_book(item_title_undo_borrow):
                    next_borrower_after_undo = book_obj_undo.return_item()
                    print("Borrow action undone.")
                    if next_borrower_after_undo:
                        try:
                            next_user_obj_after_undo = self.users.get(next_borrower_after_undo)
                            next_user_obj_after_undo.borrow_book(item_title_undo_borrow)
                        except LibraryBaseException:
                            print("Error re-assigning book after undo.")
                            pass
                else:
                    print("Failed to undo borrow, user did not have item.")

            elif action_type_to_undo == "return":
                user_id_undo_return = last_action_data["user_id"]
                item_title_undo_return = last_action_data["item_title"]
                
                user_obj_undo_return = self.users.get(user_id_undo_return)
                book_obj_undo_return = self.books.search(item_title_undo_return)
                
                book_obj_undo_return.borrow_item()
                user_obj_undo_return.borrow_book(item_title_undo_return)
                print("Return action undone.")

        except LibraryBaseException as error_msg:
            print(f"An error occurred during undo: {error_msg}")

    def show_history(self):
        print("\n--- Operation History (Most Recent First) ---")
        if self.history_stack.item_count == 0:
            print("No operations recorded yet.")
            return
        
        temp_history_list = []
        temp_stack = Stack() 
        
        while self.history_stack.item_count > 0:
            action = self.history_stack.pop()
            temp_history_list.append(action)
            temp_stack.push(action) 
            
        while temp_stack.item_count > 0:
            self.history_stack.push(temp_stack.pop())

        for i, action_data in enumerate(reversed(temp_history_list)):
            print(f"{i+1}. Type: {action_data.get('action_type')}, Details: {action_data}")
        print("---------------------------------------------")

    def exit_system(self):
        print("Exiting system now.")
        print("Saving all current data to storage...")
        Storage.save_data(self.users, self.books)
        print("Data saved. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    app = LibSys()
    app.run()
