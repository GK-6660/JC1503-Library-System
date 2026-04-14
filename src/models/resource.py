from structures.queue import Queue
from utils.exceptions import OutOfStockError

class Resource:
    def __init__(self, res_id, item_title, total_count):
        self.resource_id = res_id  
        self.title = item_title  
        self.total_copies = total_count  
        self.available_copies = total_count  
        self.waitlist = Queue()
        self.is_available_flag = True if total_count > 0 else False 

    def borrow_item(self):
        current_available_count = self.available_copies
        if current_available_count > 0:
            self.available_copies = current_available_count - 1
            print(f"Item '{self.title}' borrowed. Available: {self.available_copies}")
            if self.available_copies == 0:
                self.is_available_flag = False
        else:
            print(f"Error: '{self.title}' is out of stock. Cannot borrow.")
            raise OutOfStockError("no stock")

    def return_item(self):
        if self.available_copies < self.total_copies:
            self.available_copies = self.available_copies + 1
            print(f"Item '{self.title}' returned. Available: {self.available_copies}")
            if self.available_copies > 0 and self.is_available_flag == False:
                self.is_available_flag = True
            
            if self.waitlist.is_empty() == False:
                next_user_from_waitlist = self.waitlist.dequeue()
                self.available_copies = self.available_copies - 1 
                print(f"Item '{self.title}' immediately borrowed by {next_user_from_waitlist} from waitlist.")
                return next_user_from_waitlist  
        else:
            print(f"Warning: '{self.title}' already at max copies. No return needed.")
        return None

    def to_dict(self):
        resource_data = {}
        resource_data["resource_id"] = self.resource_id
        resource_data["title"] = self.title
        resource_data["total_copies"] = self.total_copies
        resource_data["available_copies"] = self.available_copies
        resource_data["waitlist"] = self.waitlist.to_list()
        resource_data["type"] = self.__class__.__name__
        resource_data["is_available_status"] = self.is_available_flag 
        return resource_data

    @classmethod
    def from_dict(cls, data_dict):
        print("Warning: Calling base Resource from_dict. This might not be correct.")
        return None

class Book(Resource):
    def __init__(self, res_id, item_title, total_count, book_author, book_isbn):
        super().__init__(res_id, item_title, total_count)
        self.author = book_author  
        self.isbn = book_isbn  
        self.is_fiction = True 

    def to_dict(self):
        book_data = super().to_dict()
        book_data["author"] = self.author
        book_data["isbn"] = self.isbn
        book_data["is_fiction_book"] = self.is_fiction 
        return book_data

    @classmethod
    def from_dict(cls, data_from_dict):
        book_obj = cls(
            res_id=data_from_dict["resource_id"],
            item_title=data_from_dict["title"],
            total_count=data_from_dict["total_copies"],
            book_author=data_from_dict["author"],
            book_isbn=data_from_dict["isbn"]
        )
        book_obj.available_copies = data_from_dict["available_copies"]
        waitlist_items_list = data_from_dict.get("waitlist", [])
        for user_id_in_waitlist in waitlist_items_list:
            book_obj.waitlist.enqueue(user_id_in_waitlist)
        if "is_fiction_book" in data_from_dict:
            book_obj.is_fiction = data_from_dict["is_fiction_book"]
        return book_obj

class Magazine(Resource):
    def __init__(self, res_id, item_title, total_count, issue_num):
        super().__init__(res_id, item_title, total_count)
        self.issue_number = issue_num
        self.is_monthly = True 

    def to_dict(self):
        magazine_data = super().to_dict()
        magazine_data["issue_number"] = self.issue_number
        magazine_data["is_monthly_mag"] = self.is_monthly 
        return magazine_data

    @classmethod
    def from_dict(cls, data_from_dict):
        magazine_obj = cls(
            res_id=data_from_dict["resource_id"],
            item_title=data_from_dict["title"],
            total_count=data_from_dict["total_copies"],
            issue_num=data_from_dict["issue_number"]
        )
        magazine_obj.available_copies = data_from_dict["available_copies"]
        queue_list_from_data = data_from_dict.get("waitlist", [])
        for user_id_in_queue in queue_list_from_data:
            magazine_obj.waitlist.enqueue(user_id_in_queue)
        if "is_monthly_mag" in data_from_dict:
            magazine_obj.is_monthly = data_from_dict["is_monthly_mag"]
        return magazine_obj