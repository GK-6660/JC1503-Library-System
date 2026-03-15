from utils.exceptions import ItemNotFoundError, DuplicateItemError


class HashNode:
    """哈希表中的节点（用于链地址法解决冲突）"""

    def __init__(self, key, value):
        self.key = key  # 存ID
        self.value = value  # 这里通常存 User 对象
        self.next = None  # 冲突时指向下一个人


class HashTable:
    """
    手动实现的哈希表。
    主要用于通过 user_id 快速查找 User 对象。
    """

    def __init__(self, capacity=100):
        self.capacity = capacity
        # Python中没有纯数组，这里用固定长度的list模拟底层连续内存，严禁调用 append 等动态方法！
        self.table = [None] * capacity
        self.size = 0

    def _hash_function(self, key: str) -> int:
        """
        哈希函数：把学号变成抽屉编号 (0 到 99)
        组员开发提示：
        1. 准备一个累加器：total = 0
        2. 遍历学号里的每一个字符：for char in key:
        3. 把字符转成数字加起来：total += ord(char)  # ord()可以把字母变成ASCII数字
        4. 对抽屉总数求余：return total % self.capacity
        """
        total = 0
        for char in key:
            total += ord(char)

        return total % self.capacity

    def insert(self, key: str, value):
        index = self._hash_function(key)
        current = self.table[index]

        # 如果这个位置是空的，直接放入
        if current is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
            return

        # 如果不为空，遍历链表
        prev = None
        while current is not None:
            if current.key == key:
                # 发现ID已经存在，抛出异常
                raise DuplicateItemError(f"用户 ID {key} 已存在，请勿重复添加")
            prev = current
            current = current.next

        # 挂在链表末尾
        prev.next = HashNode(key, value)
        self.size += 1

    def get(self, key: str):
        """
        找学生
        组员开发提示：
        1. 算抽屉号：index = self._hash_function(key)
        2. 拉开抽屉拿东西：current = self.table[index]
        3. 用 while 循环在这个抽屉的链表里找：
           while current is not None:
               if current.key == key:
                   return current.value  # 找到了，交出 User 对象
               current = current.next
        4. 找完了还没找到，抛出报错：
           raise ItemNotFoundError(f"找不到学号为 {key} 的用户")
        """
        index = self._hash_function(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        raise ItemNotFoundError(f"找不到学号为 {key} 的用户")

    def remove(self, key: str):
        """
        删除指定 key 的用户
        如果找不到就抛出 ItemNotFoundError
        """
        index = self._hash_function(key)
        current = self.table[index]
        prev = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    # 删除头节点
                    self.table[index] = current.next
                else:
                    # 删除中间或尾节点
                    prev.next = current.next
                self.size -= 1
                return
            prev = current
            current = current.next

        raise ItemNotFoundError(f"找不到学号为 {key} 的用户")

    def to_list(self):
        """Helper method to get all values (users) from the hash table."""
        all_items = []
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                all_items.append(current.value)
                current = current.next
        return all_items
