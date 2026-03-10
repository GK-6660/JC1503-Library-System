from utils.exceptions import ItemNotFoundError

class BSTNode:
    def __init__(self, key: str, value):
        self.key = key      # 通常是书名 (title)，用于字母排序比对
        self.value = value  # 存放 Resource/Book 对象
        self.left = None
        self.right = None

class BST:
    """
    二叉搜索树。用于按书名快速搜索图书。
    组员任务：重点搞懂递归逻辑！
    """
    def __init__(self):
        self.root = None

    def insert(self, key: str, value):
        """
        TODO: 插入新节点
        提示：如果 root 为空，直接赋值。如果不为空，调用内部的递归辅助方法 _insert_recursive
        """
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, current_node, key, value):
        """
        TODO: 递归查找插入位置
        如果 key < current_node.key，往左走；如果大于，往右走。
        """
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = BSTNode(key, value)
            else:
                self._insert_recursive(current_node.left, key, value)
        else:
            if current_node.right is None:
                current_node.right = BSTNode(key, value)
            else:
                self._insert_recursive(current_node.right, key, value)

    def search(self, key: str):
        """
        TODO: 根据书名搜索图书对象
        提示：调用 _search_recursive。如果最后返回 None，抛出 ItemNotFoundError。
        """
        if self.root.key == key:
            return self.root
        else:
            return self._search_recursive(self.root, key)

    def _search_recursive(self, current_node, key):
        """TODO: 递归搜索逻辑"""
        if current_node.key > key:
            if current_node.left.key == key:
                return current_node.left
            else:
                return self._search_recursive(current_node.left, key)
        else:
            if current_node.right.key == key:
                return current_node.right
            else:
                return self._search_recursive(current_node.right, key)

