"""
自定义异常类
组员注意：当你的代码遇到错误（比如找不到书、库存不够）时，
不要直接 print，而是 raise 这里的异常！
"""

# 定义总基类
class LibraryBaseException(Exception):
    """所有图书馆系统异常的基类"""
    pass

# 找不到东西
class ItemNotFoundError(LibraryBaseException):
    """当在 BST 或哈希表中找不到指定资源或用户时抛出"""
    pass

# 库存不足
class OutOfStockError(LibraryBaseException):
    """当图书库存为 0，无法借阅时抛出"""
    pass

# 重复添加
class DuplicateItemError(LibraryBaseException):
    """当试图添加已经存在的用户或书籍时抛出"""
    pass