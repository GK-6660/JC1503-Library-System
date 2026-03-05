class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []  # 存储子分类节点

class GeneralTree:
    def __init__(self, root_name="Library"):
        self.root = TreeNode(root_name)

    def add_category(self, parent_name, new_category):
        """TODO: 实现添加分类"""
        pass

    def count_total_items(self, node):
        """
        TODO: 实现递归遍历
        功能：统计该分类及其所有子分类下的图书总数
        """
        pass