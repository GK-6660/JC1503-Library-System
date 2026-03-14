# 可以引入前面写的链表来存储子节点
# from structures.linked_list import DoublyLinkedList

from linked_list import DoublyLinkedList
from utils.exceptions import ItemNotFoundError, DuplicateItemError


class TreeNode:
    def __init__(self, category_name: str):
        self.category_name = category_name
        # 存放该分类下的具体图书 ID (可以使用普通单链表或直接简单处理)
        self.books = DoublyLinkedList()
        # self.books = DoublyLinkedList()
        # TODO: 存放子分类。
        self.children = DoublyLinkedList()
        # self.children = DoublyLinkedList()

    def __str__(self):
        """打印节点信息"""
        child_count = (
            self.children.size
            if hasattr(self.children, "size")
            else self._count_children()
        )
        return f"分类：{self.category_name} (子节点数：{child_count})"

    def _count_children(self):
        """遍历链表计算子节点数量"""
        count = 0
        current = self.children.head
        while current:
            count += 1
            current = current.next
        return count


class CategoryTree:
    """
    通用树（多叉树），用于构建：总类 -> 理科/文科 -> 物理/历史 的层级结构。
    """

    def __init__(self, root_name="Library"):
        self.root = TreeNode(root_name)

    def add_category(self, parent_name: str, new_category_name: str):
        parent_node = self._find_node(self.root, parent_name)

        if parent_node is None:
            raise ItemNotFoundError(f"找不到父分类 '{parent_name}'")

        if self._find_child_by_name(parent_node, new_category_name):
            raise DuplicateItemError(
                f"分类 '{new_category_name}' 已经存在于 '{parent_name}'"
            )

        new_node = TreeNode(new_category_name)
        parent_node.children.append(new_node)
        print(f"成功添加分类'{new_category_name}'到'{parent_name}'")
        return True

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

    def _find_node(self, current_node, target_name):
        if current_node.category_name == target_name:
            return current_node

        current = current_node.children.head
        while current is not None:
            result = self._find_node(current.data, target_name)
            if result is not None:
                return result
            current = current.next
        return None

        """
        TODO: 递归辅助函数，用于在树中查找特定名字的节点
        """

    def _find_child_by_name(self, parent_node, child_name):
        current = parent_node.children.head
        while current is not None:
            if current.data.category_name == child_name:
                return current.data
            current = current.next
        return None

    def display(self, node=None, level=0):
        if node is None:
            node = self.root
            print("目录")
            print("=" * 40)

        indent = "  " * level
        prefix = "└── " if level == 0 else "├── "
        print(f"{indent}{prefix}{node.category_name}")

        current = node.children.head
        while current is not None:
            self.display(current.data, level + 1)
            current = current.next

    def get_all_categories(self, node=None):
        if node is None:
            node = self.root
            categories = []
        else:
            categories = []

        categories.append(node.category_name)

        current = node.children.head
        while current is not None:
            categories.extend(self.get_all_categories(current.data))
            current = current.next

        return categories

    def find_category(self, category_name: str):
        """
        查找分类

        Args:
            category_name: 要查找的分类名称

        Returns:
            TreeNode: 找到的节点

        Raises:
            ItemNotFoundError: 找不到分类时抛出
        """
        node = self._find_node(self.root, category_name)
        if node is None:
            raise ItemNotFoundError(f"找不到分类 '{category_name}'")
        return node


if __name__ == "__main__":
    library = CategoryTree("图书馆")

    library.add_category("图书馆", "理科")
    library.add_category("图书馆", "文科")
    library.add_category("图书馆", "工科")

    library.add_category("理科", "数学")
    library.add_category("理科", "物理")
    library.add_category("理科", "化学")

    library.add_category("文科", "历史")
    library.add_category("文科", "哲学")

    library.add_category("工科", "计算机")
    library.add_category("工科", "电子工程")

    library.add_category("计算机", "编程语言")
    library.add_category("计算机", "数据结构")
    library.add_category("物理", "量子力学")

    library.display()

    print("\n" + "=" * 50)
    print("查找测试")
    print("=" * 50)
    test_names = ["量子力学", "哲学", "神在原后"]
    for name in test_names:
        try:
            node = library.find_category(name)
            print(f"找到{node}")
        except ItemNotFoundError as e:
            print(f"未找到{name} - {e}")

    all_cats = library.get_all_categories()
    print(f"所有分类（{len(all_cats)}个）")
    print(all_cats)

    print("\n" + "=" * 50)
    print("\n异常测试:")
    print("=" * 50)

    try:
        print("测试1: 尝试重复添加 '物理' 到 '理科'...")
        library.add_category("理科", "物理")
    except DuplicateItemError as e:
        print(f"✅ 正确捕获到重复添加异常: {e}")
    except Exception as e:
        print(f"❌ 捕获到意外异常: {e}")

    # 测试2: 找不到异常
    try:
        print("\n测试2: 尝试查找不存在的分类 '不存在的分类'...")
        library.find_category("不存在的分类")
    except ItemNotFoundError as e:
        print(f"✅ 正确捕获到找不到异常: {e}")
    except Exception as e:
        print(f"❌ 捕获到意外异常: {e}")

    # 测试3: 找不到父分类异常
    try:
        print("\n测试3: 尝试添加到不存在的父分类 '不存在'...")
        library.add_category("不存在", "新分类")
    except ItemNotFoundError as e:
        print(f"✅ 正确捕获到找不到父分类异常: {e}")
    except Exception as e:
        print(f"❌ 捕获到意外异常: {e}")
