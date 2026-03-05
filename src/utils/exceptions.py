class LibraryError(Exception):
    """图书馆系统所有自定义异常的基类"""
    def __init__(self, message="图书馆系统发生错误"):
        self.message = message
        super().__init__(self.message)

class ItemNotFoundError(LibraryError):
    """当在 BST 或 链表中找不到书籍时触发"""
    def __init__(self, item_name):
        super().__init__(f"未找到资源: 《{item_name}》")

class UserNotFoundError(LibraryError):
    """当 Hash Table 中找不到该用户 ID 时触发"""
    def __init__(self, user_id):
        super().__init__(f"未找到用户 ID: {user_id}")

class OutOfStockError(LibraryError):
    """当书籍已借出且预约队列已满时触发"""
    def __init__(self, title):
        super().__init__(f"《{title}》目前不可借阅且预约人数已达上限")

class FileDataError(LibraryError):
    """当 JSON 文件损坏或无法读取时触发 (成员 E 负责)"""
    def __init__(self):
        super().__init__("系统数据文件损坏或格式错误")