from abc import ABC, abstractmethod

class Resource(ABC):
    def __init__(self, item_id, title):
        self._item_id = item_id  
        self.title = title
        self.is_available = True

    @abstractmethod
    def display_info(self):
        """抽象方法：体现多态，子类必须实现"""
        pass

class Book(Resource):
    def __init__(self, item_id, title, author, isbn):
        super().__init__(item_id, title)
        self.author = author
        self.isbn = isbn

    def display_info(self):
        status = "在馆" if self.is_available else "已借出"
        return f"ID: {self._item_id} | 书名: {self.title} | 作者: {self.author} [{status}]"

class Magazine(Resource):
    def __init__(self, item_id, title, issue_number):
        super().__init__(item_id, title)
        self.issue_number = issue_number

    def display_info(self):
        status = "在馆" if self.is_available else "已借出"
        return f"ID: {self._item_id} | 期刊: {self.title} | 期号: {self.issue_number} [{status}]"