import sys
import os

structures_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(structures_dir, ".."))
sys.path.append(src_dir)

from utils.exceptions import ItemNotFoundError


class BSTNode:
    def __init__(self, key: str, value):
        self.key = key  # 通常是书名 (title)，用于字母排序比对
        self.value = value  # 存放 Resource/Book 对象
        self.left = None
        self.right = None


class BST:
    """
    二叉搜索树。用于按书名快速搜索图书。
    """

    def __init__(self):
        self.root = None

    def insert(self, key: str, value):
        """
        TODO: 插入新节点
        """
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, current_node, key, value):
        """
        TODO: 递归查找插入位置
        """
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = BSTNode(key, value)
            else:
                self._insert_recursive(current_node.left, key, value)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = BSTNode(key, value)
            else:
                self._insert_recursive(current_node.right, key, value)
        else:
            # 如果书名已经存在，更新对应的图书对象
            current_node.value = value

    def search(self, key: str):
        """
        TODO: 根据书名搜索图书对象
        """
        result = self._search_recursive(self.root, key)
        if result is None:
            raise ItemNotFoundError(f"Book with title '{key}' not found.")
        return result

    def _search_recursive(self, current_node, key):
        """TODO: 递归搜索逻辑"""
        if current_node is None:
            return None
        if key < current_node.key:
            return self._search_recursive(current_node.left, key)
        elif key > current_node.key:
            return self._search_recursive(current_node.right, key)
        else:
            return current_node.value

    def delete(self, key: str):
        """
        TODO: 删除节点
        """
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, current_node, key):
        """TODO: 递归删除逻辑"""
        if current_node is None:
            return None
        if key < current_node.key:
            current_node.left = self._delete_recursive(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._delete_recursive(current_node.right, key)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left

            temp = self._find_min(current_node.right)
            current_node.key = temp.key
            current_node.value = temp.value
            current_node.right = self._delete_recursive(current_node.right, temp.key)
        return current_node
