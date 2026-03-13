import json
import os
from structures.hash_table import HashTable
from structures.bst import BST

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
        pass

    @staticmethod
    def load_data() -> tuple:  # 注意返回的是元组
        """
        TODO: 系统启动时加载数据
        1. 检查 DATA_FILE 是否存在，不存在则返回空的 HashTable 和 BST
        2. 使用 json.load 读取数据
        3. 根据读取的字典，重新实例化 User 和 Book 对象，并放回 HashTable 和 BST 中
        4. return (恢复好的_users_hash, 恢复好的_books_bst)
        """
        pass
