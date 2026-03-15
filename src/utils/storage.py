import json
import os
from structures.hash_table import HashTable
from structures.bst import BST
from models.user import User
from models.resource import Book, Magazine

# 定义数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/library_data.json")


class Storage:
    @staticmethod
    def save_data(users_hash: HashTable, books_bst: BST):
        """
        TODO: 将内存中的对象序列化为 JSON 并保存
        1. 遍历 HashTable，把所有的 User 对象转成字典
        2. 遍历 BST，把所有的 Book/Magazine 转成字典
        3. 组装成一个大字典 data = {"users": [...], "books": [...]}
        4. 使用 json.dump 写入 DATA_FILE
        """
        data = {
            "users": [user.to_dict() for user in users_hash.to_list()],
            "books": [item.to_dict() for item in books_bst.to_list()]
        }
        
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_data() -> tuple:  # 注意返回的是元组
        """
        TODO: 系统启动时加载数据
        1. 检查 DATA_FILE 是否存在，不存在则返回空的 HashTable 和 BST
        2. 使用 json.load 读取数据
        3. 根据读取的字典，重新实例化 User 和 Book 对象，并放回 HashTable 和 BST 中
        4. return (恢复好的_users_hash, 恢复好的_books_bst)
        """
        users = HashTable()
        books = BST()

        if not os.path.exists(DATA_FILE):
            return users, books
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for user_data in data.get("users", []):
                user = User.from_dict(user_data)
                users.insert(user.user_id, user)
                
            for book_data in data.get("books", []):
                if book_data.get("type") == "Book":
                    item = Book.from_dict(book_data)
                elif book_data.get("type") == "Magazine":
                    item = Magazine.from_dict(book_data)
                else:
                    # Fallback or unknown type
                    continue
                books.insert(item.title, item)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or empty, return empty structures
            pass
            
        return users, books
