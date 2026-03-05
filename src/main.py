from models.resource import Book
from structures.bst import BST
# ... 导入其他模块

class LibraryManager:
    def __init__(self):
        self.books_index = BST()  # 组合关系
        # 初始化其他数据结构

    def run(self):
        print("--- 欢迎进入 JC1503 图书馆管理系统 ---")
        # TODO: 主循环逻辑

if __name__ == "__main__":
    app = LibraryManager()
    app.run()