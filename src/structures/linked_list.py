class Node:
    """双向链表的节点"""

    def __init__(self, data):
        self.data = data  # 链表节点对应的数据
        self.prev = None  # 指向上一个节点
        self.next = None  # 指向下一个节点


# 总链表
class DoublyLinkedList:
    """
    手动实现的双向链表。
    组员任务：实现数据的增删改查。
    """

    def __init__(self):
        self.head = None  # 表头（第一本书）
        self.tail = None  # 表尾（最后一本书）
        self.size = 0  # 记录一共借了多少本书

    # 借书（在尾部加节点）
    def append(self, data):
        """
        TODO: 在链表尾部添加一个新节点
        提示：考虑链表为空和不为空两种情况，正确连接 prev 和 next 指针
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    # 还书（拿走某个节点）
    def remove(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                # 处理前驱节点或 head
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                # 处理后继节点或 tail
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self.size -= 1
                return True

            current = current.next

        print(f"Data {data} not found.")
        return False

    # 会返回列表
    def to_list(self):
        """辅助方法：将链表内容转为普通列表（仅用于最后的打印展示或保存JSON）"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
