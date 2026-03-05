from structures.linked_list import DoublyLinkedList

class User:
    def __init__(self, user_id, name):
        # 封装：使用私有或受保护属性
        self._user_id = user_id  
        self.name = name
        
        # 组合 (Composition)：每个用户持有一个双向链表
        # 用于存储该用户当前借阅的 Book 对象
        self.borrowed_books = DoublyLinkedList()
        
        # 财务属性（体现系统逻辑）
        self.fines = 0.0

    def get_id(self):
        return self._user_id

    def __str__(self):
        return f"读者 ID: {self._user_id} | 姓名: {self.name} | 欠费: ￡{self.fines}"