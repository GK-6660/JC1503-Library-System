import sys
import os
# 确保程序能正确导入 src 目录下的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from models.resource import Book
from structures.bst import BST
from structures.queue import Queue
from structures.stack import Stack
from utils.storage import StorageManager
from utils.exceptions import LibraryException

class LibrarySystem:
    def __init__(self):
        # 1. 初始化底层数据结构
        self.book_db = BST()            # 存储图书
        self.wait_queue = Queue()       # 借书排队
        self.action_stack = Stack()     # 操作日志/撤销
        self.storage = StorageManager() # 数据持久化
        
        self.current_user = None
        self.load_system_data()

    def load_system_data(self):
        """从 data 文件夹加载初始数据"""
        try:
            initial_books = self.storage.load_books()
            for b in initial_books:
                self.book_db.insert(b)
        except Exception:
            print("[系统提示] 未发现存档，将以空库启动。")

    def login(self):
        print("="*40)
        print("   JC1503 图书馆管理系统 - 登录")
        print("="*40)
        username = input("请输入用户名: ").strip()
        password = input("请输入密码: ").strip()
        
        # 简单逻辑：admin/123 为管理员，其余为读者
        if username == "admin" and password == "123":
            self.current_user = User(username, role="admin")
        else:
            self.current_user = User(username, role="reader")
        
        print(f"\n登录成功！身份确认：【{self.current_user.role.upper()}】")

    def show_menu(self):
        while True:
            role = self.current_user.role
            print(f"\n{'#'*10} 当前用户: {self.current_user.username} {'#'*10}")
            print("1. 搜索图书 (ID检索)")
            print("2. 浏览全库 (展示清单)")
            
            if role == "admin":
                print("3. [管理员] 新书入库 (Insert)")
                print("4. [管理员] 图书下架 (Delete)")
                print("5. [管理员] 查看借阅排队情况")
            else:
                print("3. [读者] 申请借书 (Borrow)")
                print("4. [读者] 归还图书 (Return)")
                print("5. [读者] 查看我的借阅历史")
            
            print("0. 保存并退出")
            print("-" * 30)
            
            choice = input("请选择操作序号: ")
            try:
                self.handle_choice(choice)
            except LibraryException as e:
                print(f"【操作失败】: {e}")
            except Exception as e:
                print(f"【系统错误】: {e}")

    def handle_choice(self, choice):
        role = self.current_user.role

        # --- 1. 搜索功能 (所有人) ---
        if choice == "1":
            bid = input("请输入图书ID: ")
            book = self.book_db.search(bid)
            if book:
                print(f"找到图书: 《{book.title}》 | 作者: {book.author} | 状态: {'在馆' if book.is_available else '已借出'}")
            else:
                print("抱歉，未找到该编号的图书。")

        # --- 2. 展示全库 (所有人) ---
        elif choice == "2":
            print("\n--- 图书馆馆藏清单 ---")
            # 调用 BST 的中序遍历方法
            all_books = self.book_db.get_all_in_order() 
            if not all_books:
                print("空空如也，请联系管理员上架。")
            for b in all_books:
                status = "√ 在馆" if b.is_available else "× 已借出"
                print(f"[{b.book_id}] 《{b.title}》 - {status}")

        # --- 3. 增加 (Admin) vs 借阅 (Reader) ---
        elif choice == "3":
            if role == "admin":
                bid = input("新书ID: ")
                title = input("书名: ")
                author = input("作者: ")
                self.book_db.insert(Book(bid, title, author))
                print("入库成功！")
            else:
                bid = input("请输入想借阅的书号: ")
                book = self.book_db.search(bid)
                if book and book.is_available:
                    book.is_available = False
                    self.current_user.add_history(f"借阅了《{book.title}》")
                    print("借书成功！请按时归还。")
                else:
                    print("该书目前不可借，已为您加入排队序列。")
                    self.wait_queue.enqueue(self.current_user.username)

        # --- 4. 删除 (Admin) vs 归还 (Reader) ---
        elif choice == "4":
            bid = input("请输入图书ID: ")
            if role == "admin":
                if self.book_db.delete(bid):
                    print("图书已成功从库中移除。")
                else:
                    print("删除失败：未找到该ID。")
            else:
                book = self.book_db.search(bid)
                if book and not book.is_available:
                    book.is_available = True
                    print(f"归还成功！《{book.title}》重新上架。")
                    # 联动：检查是否有排队者
                    next_user = self.wait_queue.dequeue()
                    if next_user:
                        print(f"【提醒】该书已自动分配给排队用户: {next_user}")
                        book.is_available = False
                else:
                    print("还书失败：该书不属于借出状态。")

        # --- 5. 排队 (Admin) vs 历史 (Reader) ---
        elif choice == "5":
            if role == "admin":
                print("\n--- 预约排队详情 ---")
                self.wait_queue.display()
            else:
                print("\n--- 我的借阅记录 ---")
                for record in self.current_user.get_history():
                    print(f"-> {record}")

        # --- 0. 退出 ---
        elif choice == "0":
            print("正在保存数据并退出...")
            all_books = self.book_db.get_all_in_order()
            self.storage.save_books(all_books)
            sys.exit()

if __name__ == "__main__":
    system = LibrarySystem()
    system.login()
    system.show_menu()