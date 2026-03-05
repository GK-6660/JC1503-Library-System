class Stack:
    def __init__(self):
        self.items = []  # 注意：指南要求手动实现，建议内部用 LinkedList 模拟

    def push(self, item):
        """TODO: 成员 D 实现入栈逻辑（记录操作）"""
        pass

    def pop(self):
        """TODO: 成员 D 实现出栈逻辑（撤销操作）"""
        pass

    def is_empty(self):
        return len(self.items) == 0