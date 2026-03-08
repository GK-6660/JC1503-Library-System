import sys
from utils.storage import Storage
from structures.hash_table import HashTable
from structures.bst import BST
from structures.stack import Stack
from models.user import User
from models.resource import Book

class LibrarySystem:
    def __init__(self):
        # 1. 系统启动，加载数据
        print("正在加载系统数据...")
        # TODO: self.users, self.books = Storage.load_data()
        
        # 暂时用空的代替（等 load_data 写好后替换）
        self.users = HashTable()
        self.books = BST()
        
        # 2. 初始化撤销栈
        self.history_stack = Stack()

    def run(self):
        """主循环，CLI 交互界面"""
        while True:
            self.print_menu()
            choice = input("请输入操作编号: ").strip()

            if choice == '1':
                self.handle_add_user()
            elif choice == '2':
                self.handle_add_book()
            elif choice == '3':
                self.handle_borrow()
            elif choice == '4':
                self.handle_return()
            elif choice == '5':
                self.handle_undo()
            elif choice == '0':
                self.exit_system()
            else:
                print("无效输入，请重新选择！")

    def print_menu(self):
        print("\n" + "="*30)
        print("  JC1503 图书管理系统  ")
        print("="*30)
        print("1. 添加用户")
        print("2. 录入新书")
        print("3. 借阅图书")
        print("4. 归还图书")
        print("5. 撤销上一步操作 (Undo)")
        print("0. 保存并退出")
        print("="*30)

    def handle_add_user(self):
        """
        TODO: 处理添加用户逻辑
        1. input() 获取用户 ID 和姓名
        2. 创建 User 对象
        3. self.users.insert(user_id, user_obj)
        4. 记录这次操作到 self.history_stack.push(...)
        """
        user_id = input("请输入新用户学号/ID: ")
        name = input("请输入用户姓名: ")
        # 完善后面的逻辑...
        print(f"用户 {name} 添加成功！")

    def handle_borrow(self):
        """
        TODO: 借书核心逻辑
        1. input() 获取 user_id 和 book_title
        2. 从 self.users (哈希表) 里 get 用户对象
        3. 从 self.books (BST) 里 search 书籍对象
        4. 调用书的 book.borrow_item()
        5. 调用用户的 user.borrow_book()
        6. 注意使用 try...except 捕获他们抛出的异常并打印友好提示！
        """
        pass
        
    def handle_return(self):
        # TODO: 实现还书逻辑
        pass
        
    def handle_undo(self):
        # TODO: self.history_stack.pop() 拿到上一步动作，然后反向执行
        pass

    def exit_system(self):
        print("正在保存数据...")
        # TODO: Storage.save_data(self.users, self.books)
        print("数据已保存，系统退出。再见！")
        sys.exit(0)

if __name__ == "__main__":
    system = LibrarySystem()
    system.run()