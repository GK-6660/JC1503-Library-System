from structures.linked_list import DoublyLinkedList

class User:
    def __init__(self, u_id, u_name):
        self.user_id = u_id
        self.name = u_name
        self.borrowed_items = DoublyLinkedList()
        self.is_active_user = True 

    def borrow_book(self, book_title_to_borrow):
        current_borrowed_list = self.borrowed_items
        current_borrowed_list.append(book_title_to_borrow)
        print(f"User {self.name} borrowed {book_title_to_borrow}.")

    def return_book(self, book_title_to_return):
        remove_success = self.borrowed_items.remove(book_title_to_return)
        if remove_success == False:
            print(f"Warning: {self.name} did not borrow {book_title_to_return}. Cannot return.")
            return False
        else:
            print(f"User {self.name} returned {book_title_to_return}.")
            return True

    def to_dict(self):
        user_data_dict = {}
        user_data_dict["user_id"] = self.user_id
        user_data_dict["name"] = self.name
        user_data_dict["borrowed_items"] = self.borrowed_items.to_list()
        user_data_dict["is_active"] = self.is_active_user 
        return user_data_dict

    @classmethod
    def from_dict(cls, data_dict):
        user_obj = cls(data_dict["user_id"], data_dict["name"])
        borrowed_list_from_data = data_dict["borrowed_items"]
        for item_title_str in borrowed_list_from_data:
            user_obj.borrowed_items.append(item_title_str)
        if "is_active" in data_dict:
            user_obj.is_active_user = data_dict["is_active"]
        return user_obj