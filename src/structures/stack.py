class StackNode:
    def __init__(self, action_data):
        self.action_data = action_data  # 记录操作内容，比如字典 {"action": "borrow", "user": "123", "book": "Python"}
        self.next = None

class Stack:
    """
    手动实现的后进先出 (LIFO) 栈。
    用于记录操作历史，实现撤销功能。
    """
    def __init__(self):
        self.top = None  # 栈顶指针
        self.size = 0

    def push(self, action_data):
        """
        TODO: 入栈 (记录了一次新操作)
        1. 创建新节点
        2. 新节点的 next 指向当前的 top
        3. top 更新为新节点
        """
        pass

    def pop(self):
        """
        TODO: 出栈 (执行撤销)
        1. 如果栈为空，返回 None
        2. 拿到 top 的 action_data
        3. top 更新为 top.next
        4. 返回 action_data，交由 main.py 去执行反向操作
        """
        pass