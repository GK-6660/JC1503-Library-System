class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)] # 使用拉链法解决冲突

    def _hash(self, key):
        """TODO: 实现哈希函数"""
        return hash(key) % self.size

    def insert_user(self, user_id, user_obj):
        """TODO: 实现插入用户信息"""
        pass

    def get_user(self, user_id):
        """TODO: 实现快速获取用户信息"""
        pass