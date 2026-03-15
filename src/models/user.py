from structures.linked_list import DoublyLinkedList


class User:
    """图书馆的借阅者"""

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id  # 用户ID
        self.name = name  # 用户姓名
        # 实例化手写的双向链表，用于存借的书
        self.borrowed_items = DoublyLinkedList()

    def borrow_book(self, book_title: str):
        """
        TODO: 将书名(或书的ID)加入到借阅链表中
        调用 self.borrowed_items.append(...)
        """
        self.borrowed_items.append(book_title)

    def return_book(self, book_title: str):
        """
        TODO: 将书名从借阅链表中移除
        调用 self.borrowed_items.remove(...)
        """
        success = self.borrowed_items.remove(book_title)
        if not success:
            print(f"User {self.name} does not have book '{book_title}' borrowed.")
        return success

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "borrowed_items": self.borrowed_items.to_list()
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["user_id"], data["name"])
        for item in data["borrowed_items"]:
            user.borrowed_items.append(item)
        return user
