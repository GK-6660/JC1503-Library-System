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
        self.borrowed_items.append(book_title)  # 将书名加入到借阅链表中
        print(f"{self.name} 已借阅 {book_title}")

    def return_book(self, book_title: str):
        """
        TODO: 将书名从借阅链表中移除
        调用 self.borrowed_items.remove(...)
        """
        # 从借阅链表中移除书名
        result = self.borrowed_items.remove(book_title)
        if result:
            print(f"{self.name} 已归还 {book_title}")
        else:
            print(f"{self.name} 没有借阅 {book_title}")
        return result  # 返回是否成功归还

    def get_borrowed_list(self):
        """获取用户借阅的所有书籍列表"""
        return self.borrowed_items.to_list()

    def __str__(self):
        borrowed_titles = self.borrowed_items.to_list()
        if borrowed_titles:
            books_str = "、".join(borrowed_titles)
            return f"用户: {self.name}({self.user_id}) - 已借书籍: {books_str}"
        else:
            return f"用户: {self.name}({self.user_id}) - 暂无借阅"
