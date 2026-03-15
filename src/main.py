import sys
from utils.storage import Storage
from structures.hash_table import HashTable
from structures.bst import BST
from structures.stack import Stack
from models.user import User
from models.resource import Book, Magazine
from utils.exceptions import DuplicateItemError, ItemNotFoundError, OutOfStockError


class LibrarySystem:
    def __init__(self):
        # 1. 系统启动，加载数据
        print("正在加载系统数据...")
        self.users, self.books = Storage.load_data()

        # 2. 初始化撤销栈
        self.history_stack = Stack()

    def run(self):
        """主循环，CLI 交互界面"""
        while True:
            self.print_menu()
            choice = input("请输入操作编号: ").strip()

            if choice == "1":
                self.handle_add_user()
            elif choice == "2":
                self.handle_add_book()
            elif choice == "3":
                self.handle_borrow()
            elif choice == "4":
                self.handle_return()
            elif choice == "5":
                self.handle_undo()
            elif choice == "0":
                self.exit_system()
            else:
                print("无效输入，请重新选择！")

    def print_menu(self):
        print("\n" + "=" * 30)
        print("  JC1503 图书管理系统  ")
        print("=" * 30)
        print("1. 添加用户")
        print("2. 录入新书")
        print("3. 借阅图书")
        print("4. 归还图书")
        print("5. 撤销上一步操作 (Undo)")
        print("0. 保存并退出")
        print("=" * 30)

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
        
        if not user_id or not name:
             print("ID 和姓名不能为空！")
             return

        try:
            user = User(user_id, name)
            self.users.insert(user_id, user)
            self.history_stack.push({"action": "add_user", "user_id": user_id})
            print(f"用户 {name} 添加成功！")
        except DuplicateItemError as e:
            print(f"错误: {e}")

    def handle_add_book(self):
        print("请选择资源类型: 1. 图书 (Book)  2. 杂志 (Magazine)")
        type_choice = input("请输入类型编号: ").strip()
        
        resource_id = input("请输入资源ID: ")
        title = input("请输入标题: ")
        try:
            total_copies = int(input("请输入总册数: "))
        except ValueError:
            print("册数必须是整数！")
            return
            
        if type_choice == "1":
            author = input("请输入作者: ")
            isbn = input("请输入ISBN: ")
            item = Book(resource_id, title, total_copies, author, isbn)
        elif type_choice == "2":
            issue_number = input("请输入刊号: ")
            item = Magazine(resource_id, title, total_copies, issue_number)
        else:
            print("无效的类型选择！")
            return

        self.books.insert(title, item)
        self.history_stack.push({"action": "add_book", "title": title})
        print(f"资源 '{title}' 添加成功！")

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
        user_id = input("请输入用户ID: ")
        book_title = input("请输入书名: ")
        
        try:
            user = self.users.get(user_id)
            book = self.books.search(book_title)
            
            book.borrow_item()
            user.borrow_book(book_title)
            
            self.history_stack.push({
                "action": "borrow", 
                "user_id": user_id, 
                "book_title": book_title
            })
            print(f"用户 {user.name} 成功借阅 '{book.title}'！")
            
        except ItemNotFoundError as e:
            print(f"错误: {e}")
        except OutOfStockError as e:
            print(f"错误: {e}")
            choice = input("库存不足，是否加入预约队列？(y/n): ").strip().lower()
            if choice == 'y':
                try:
                    # In case book wasn't assigned (unlikely given the flow)
                    if 'book' in locals():
                        book.waitlist.enqueue(user_id)
                        print("已加入预约队列。")
                except Exception as ex:
                    print(f"加入队列失败: {ex}")

    def handle_return(self):
        # TODO: 实现还书逻辑
        user_id = input("请输入用户ID: ")
        book_title = input("请输入书名: ")
        
        try:
            user = self.users.get(user_id)
            book = self.books.search(book_title)
            
            if user.return_book(book_title):
                next_user_id = book.return_item()
                print(f"用户 {user.name} 成功归还 '{book.title}'！")
                
                if next_user_id:
                    print(f"注意：书籍已自动借给预约队列中的用户 {next_user_id}！")
                    try:
                        next_user = self.users.get(next_user_id)
                        next_user.borrow_book(book_title)
                    except ItemNotFoundError:
                        print(f"警告: 预约用户 {next_user_id} 未找到，无法更新其借阅记录。")
                        
                self.history_stack.push({
                    "action": "return", 
                    "user_id": user_id, 
                    "book_title": book_title
                })
            else:
                print("归还失败，该用户未借阅此书。")

        except ItemNotFoundError as e:
            print(f"错误: {e}")

    def handle_undo(self):
        """
        TODO: self.history_stack.pop() 拿到上一步动作，然后反向执行
        """
        action_data = self.history_stack.pop()
        if not action_data:
            print("没有可以撤销的操作。")
            return
        
        action_type = action_data.get("action")
        print(f"正在撤销操作: {action_type}")
        
        try:
            if action_type == "add_user":
                user_id = action_data["user_id"]
                self.users.remove(user_id)
                print(f"撤销成功：用户 {user_id} 已删除。")
                
            elif action_type == "add_book":
                # Remove book - BST remove implemented
                title = action_data["title"]
                self.books.remove(title)
                print(f"撤销成功：书籍 '{title}' 已删除。")
                
            elif action_type == "borrow":
                # Undo borrow -> Return book
                user_id = action_data["user_id"]
                book_title = action_data["book_title"]
                
                user = self.users.get(user_id)
                book = self.books.search(book_title)
                
                # Logic similar to handle_return but without user input
                if user.return_book(book_title):
                    next_user_id = book.return_item()
                    print(f"撤销借阅成功：书 '{book_title}' 已归还。")
                    if next_user_id:
                        print(f"书籍自动流转给预约用户: {next_user_id}")
                        try:
                            next_user = self.users.get(next_user_id)
                            next_user.borrow_book(book_title)
                        except ItemNotFoundError:
                            pass
                else:
                    print("撤销失败：用户未借阅此书？数据可能不一致。")

            elif action_type == "return":
                # Undo return -> Borrow book
                user_id = action_data["user_id"]
                book_title = action_data["book_title"]
                
                user = self.users.get(user_id)
                book = self.books.search(book_title)
                
                # Check if book is available
                # If return triggered a lend to waitlist, book.available_copies might be 0
                # But we want to force borrow back to original user?
                # This is complex. We will try normal borrow.
                try:
                    book.borrow_item()
                    user.borrow_book(book_title)
                    print(f"撤销归还成功：书 '{book_title}' 已重新借给 {user.name}。")
                except OutOfStockError:
                    print("撤销失败：书籍库存不足（可能已借给预约者）。")

            else:
                print(f"未知操作类型: {action_type}")
                
        except Exception as e:
            print(f"撤销操作时发生错误: {e}")

    def exit_system(self):
        print("正在保存数据...")
        Storage.save_data(self.users, self.books)
        print("数据已保存，系统退出。再见！")
        sys.exit(0)


if __name__ == "__main__":
    system = LibrarySystem()
    system.run()
