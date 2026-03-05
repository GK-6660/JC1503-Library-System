class QueueNode:
    def __init__(self, user_id):
        self.user_id = user_id
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, user_id):
        """TODO: 成员 C 实现入队（用户开始排队）"""
        pass

    def dequeue(self):
        """TODO: 成员 C 实现出队（排到的人借书）"""
        pass