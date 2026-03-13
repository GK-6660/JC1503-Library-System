from utils.exceptions import LibraryBaseException

"""排队借书"""


class QueueNode:
    """队列节点"""

    def __init__(self, user_id: str):
        self.user_id = user_id  # 存排队人的id
        self.next = None  # 指向后面排队的人


class Queue:
    """
    手动实现的先进先出 (FIFO) 队列。
    严禁使用 Python 的 list.append() 和 list.pop(0)！
    """

    def __init__(self):
        self.front = None  # 队头（准备出队的元素）
        self.rear = None  # 队尾（新加入的元素）
        self.size = 0  # 队伍总人数

    def enqueue(self, user_id: str):
        """
        入队：新来了一个人，排到队尾去。
        组员开发提示：
        1. 先造一个排队者：new_node = QueueNode(user_id)
        2. 如果队伍是空的 (if self.rear is None):
           - 队头和队尾都是这个人 (self.front = self.rear = new_node)
        3. 如果队伍里有人：
           - 让现在的队尾牵住新人的手 (self.rear.next = new_node)
           - 把“队尾”的称号交给新人 (self.rear = new_node)
        4. 队伍人数加一 (self.size += 1)
        """
        pass

    def dequeue(self) -> str:
        """
        出队：书还回来了，队头的人拿到书，离开队伍。
        组员开发提示：
        1. 如果队伍是空的 (if self.front is None):
           - 没人排队，直接 return None
        2. 拿到队头人的学号：borrower_id = self.front.user_id
        3. 把队头往后挪一位（原来排第二的人变成第一了）：
           self.front = self.front.next
        4. 边界情况：如果挪完之后，发现 self.front 变成 None 了（说明队伍走空了），
           那就必须把 self.rear 也变成 None！
        5. 队伍人数减一 (self.size -= 1)
        6. 返回拿到的学号：return borrower_id
        """
        pass

    def is_empty(self) -> bool:
        return self.size == 0
