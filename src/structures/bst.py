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
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = BSTNode(key, value)
            else:
                self._insert_recursive(current_node.right, key, value)
        else:
            # key exists, update value or raise error?
            # Assuming update for now or just ignore
            current_node.value = value

    def search(self, key: str):
        """
        TODO: 根据书名搜索图书对象
        提示：调用 _search_recursive。如果最后返回 None，抛出 ItemNotFoundError。
        """
        result = self._search_recursive(self.root, key)
        if result is None:
            raise ItemNotFoundError(f"Book with title '{key}' not found.")
        return result

    def _search_recursive(self, current_node, key):
        """TODO: 递归搜索逻辑"""
        if current_node is None:
            return None
        if key == current_node.key:
            return current_node.value
        elif key < current_node.key:
            return self._search_recursive(current_node.left, key)
        else:
            return self._search_recursive(current_node.right, key)

    def remove(self, key: str):
        """Remove a node by key"""
        self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, current_node, key):
        if current_node is None:
            return None

        if key < current_node.key:
            current_node.left = self._remove_recursive(current_node.left, key)
        elif key > current_node.key:
            current_node.right = self._remove_recursive(current_node.right, key)
        else:
            # Node found
            # Case 1: No children (leaf)
            if current_node.left is None and current_node.right is None:
                return None
            
            # Case 2: One child
            if current_node.left is None:
                return current_node.right
            if current_node.right is None:
                return current_node.left
            
            # Case 3: Two children
            # Find in-order successor (smallest in right subtree)
            successor = self._find_min(current_node.right)
            current_node.key = successor.key
            current_node.value = successor.value
            current_node.right = self._remove_recursive(current_node.right, successor.key)
        
        return current_node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def to_list(self):
        """Helper method to convert BST to a list of values (books/resources)"""
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)
