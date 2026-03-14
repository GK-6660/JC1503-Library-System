import os
import sys
import unittest

# 获取当前文件所在目录 (tests/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根目录是当前目录的上一级 (JC1503-Library-System/)
project_dir = os.path.dirname(current_dir)

# 将项目根目录添加到路径
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

try:
    from src.structures.tree import CategoryTree
    from src.utils.exceptions import (
        ItemNotFoundError,
        DuplicateItemError,
    )

    Exception_available = True
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前文件: {__file__}")
    print(f"项目目录: {project_dir}")
    print(f"sys.path: {sys.path}")
    raise


class TestCategoryTree(unittest.TestCase):
    """测试分类树"""

    def setUp(self):
        self.tree = CategoryTree("图书馆")
        """每个测试前准备"""

    def test_add_root_category(self):
        """测试添加根分类"""
        result = self.tree.add_category("图书馆", "理科")
        self.assertTrue(result)
        self.assertIsNotNone(self.tree.root)
        self.assertEqual(self.tree.root.category_name, "理科")

    def test_add_child_category(self):
        """测试添加子分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")
        self.tree.add_category("理科", "物理")

        child_count = len(self.tree.root.children)  # 直接获取列表长度
        self.assertEqual(child_count, 2)

    def test_add_duplicate_category(self):
        """测试添加重复分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")

        with self.assertRaises(DuplicateItemError):
            self.tree.add_category("理科", "数学")

    def test_add_category_with_nonexistent_parent(self):
        """测试添加到不存在的父分类"""
        with self.assertRaises(ItemNotFoundError):
            self.tree.add_category("不存在的分类", "数学")

    def test_search_category(self):
        """测试搜索分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")
        self.tree.add_category("数学", "高等数学")

        node = self.tree.find_category("理科")
        self.assertEqual(node.category_name, "理科")

        node = self.tree.find_category("数学")
        self.assertEqual(node.category_name, "数学")

        node = self.tree.find_category("高等数学")
        self.assertEqual(node.category_name, "高等数学")

        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("化学")

    def test_get_path(self):
        """测试获取分类路径"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")
        self.tree.add_category("数学", "高等数学")
        self.tree.add_category("高等数学", "微积分")

        path = self.tree.get_path("微积分")
        self.assertEqual(path, ["图书馆", "理科", "数学", "高等数学", "微积分"])

        with self.assertRaises(ItemNotFoundError):
            self.tree.get_path("不存在的分类")

    def test_get_all_categories(self):
        """测试获取所有分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")
        self.tree.add_category("理科", "物理")
        self.tree.add_category("图书馆", "文科")
        self.tree.add_category("文科", "文学")
        self.tree.add_category("图书馆", "工科")

        all_cats = self.tree.get_all_categories()
        expected_cats = ["图书馆", "理科", "数学", "物理", "文科", "文学", "工科"]
        self.assertEqual(len(all_cats), 7)
        for cat in expected_cats:
            self.assertIn(cat, all_cats)

    def test_remove_category(self):
        """测试删除分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("理科", "数学")
        self.tree.add_category("数学", "高等数学")

        # 删除叶子节点
        result = self.tree.remove_category("高等数学")
        self.assertTrue(result)
        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("高等数学")

        # 删除非叶子节点
        result = self.tree.remove_category("数学")
        self.assertTrue(result)
        with self.assertRaises(ItemNotFoundError):
            self.tree.find_category("数学")

        # 删除不存在的分类
        result = self.tree.remove_category("不存在的")
        self.assertFalse(result)

    def test_move_category(self):
        """测试移动分类"""
        self.tree.add_category("图书馆", "理科")
        self.tree.add_category("图书馆", "文科")
        self.tree.add_category("理科", "数学")

        # 移动数学到文科下
        result = self.tree.move_category("数学", "文科")
        self.assertTrue(result)

        path = self.tree.get_path("数学")
        self.assertEqual(path, ["图书馆", "文科", "数学"])

        # 移动到不存在的父分类
        result = self.tree.move_category("数学", "不存在的")
        self.assertFalse(result)

    def test_nested_categories_depth(self):
        """测试深层嵌套分类"""
        self.tree.add_category("图书馆", "层级1")
        current = "层级1"
        for i in range(2, 7):
            name = f"层级{i}"
            self.tree.add_category(current, name)
            current = name

        # 验证最深层的路径
        path = self.tree.get_path("层级6")
        expected = ["图书馆", "层级1", "层级2", "层级3", "层级4", "层级5", "层级6"]
        self.assertEqual(path, expected)


class TestResourceModels(unittest.TestCase):
    """测试资源模型 - 等待组员1完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员1完成 Resource, Book, Magazine, User 类的实现")


class TestLinkedList(unittest.TestCase):
    """测试双向链表 - 等待组员2完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员2完成 DoublyLinkedList 的实现")


class TestStack(unittest.TestCase):
    """测试栈 - 等待组员2完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员2完成 Stack 的实现")


class TestHashTable(unittest.TestCase):
    """测试哈希表 - 等待组员3完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员3完成 HashTable 的实现")


class TestQueue(unittest.TestCase):
    """测试队列 - 等待组员3完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员3完成 Queue 的实现")


class TestBST(unittest.TestCase):
    """测试二叉搜索树 - 等待组员4完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待组员4完成 BST 的实现")


class TestIntegration(unittest.TestCase):
    """集成测试 - 等待所有模块完成"""

    def test_placeholder(self):
        """测试占位"""
        self.skipTest("等待所有模块完成后进行集成测试")


# 主测试入口
def create_test_suite():
    """创建测试套件"""
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()

    test_classes = [
        TestCategoryTree,
        TestResourceModels,
        TestLinkedList,
        TestStack,
        TestHashTable,
        TestQueue,
        TestBST,
        TestIntegration,
    ]

    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))
    return suite


def run_tests():
    """运行所有测试"""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'=' * 60}")
    print(" 测试报告")
    print(f"{'=' * 60}")
    print(f"测试总数: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    print(f"{'=' * 60}")

    if result.skipped:
        print("\n 跳过的测试（等待其他组员）：")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")

    return result


if __name__ == "__main__":
    run_tests()
