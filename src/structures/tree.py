# 可以引入前面写的链表来存储子节点
# from structures.linked_list import DoublyLinkedList

class TreeNode:
    def __init__(self, category_name: str):
        self.category_name = category_name
        # 存放该分类下的具体图书 ID (可以使用普通单链表或直接简单处理)
        # self.books = DoublyLinkedList() 
        # TODO: 存放子分类。
        # self.children = DoublyLinkedList() 

class CategoryTree:
    """
    通用树（多叉树），用于构建：总类 -> 理科/文科 -> 物理/历史 的层级结构。
    """
    def __init__(self, root_name="Library"):
        self.root = TreeNode(root_name)

    def add_category(self, parent_name: str, new_category_name: str):
        """
        组员开发提示：往指定的“父分类”下，挂载一个“新子分类”
        例如：add_category("理科", "物理")
        
        1. 我们需要先写一个内部方法 _find_node，在树里找到名字叫 parent_name 的那个节点
        2. parent_node = self._find_node(self.root, parent_name)
        3. 如果没找到，可以 print 提示 "找不到父分类"
        4. 如果找到了：
           - 造一个新节点：new_node = TreeNode(new_category_name)
           - 把它塞进父节点的 children 链表里：
             parent_node.children.append(new_node)
        """
        parent_node = self._find_node(self.root, parent_name)
        if parent_node is None:
            return "找不到父类"
        else:
            new_node = TreeNode(new_category_name)
            parent_node.children.append(new_node)
            return "finish"


    def _find_node(self, current_node, target_name):
        """
        TODO: 递归辅助函数，用于在树中查找特定名字的节点
        """
        if current_node.name == target_name:
            return current_node
        else:
            for child in current_node.children:
                return self._find_node(child, target_name)
