from utils.exceptions import OutOfStockError
from structures.queue import Queue


class Resource:
    """所有图书馆资源的抽象基类"""

    def __init__(self, resource_id: str, title: str, total_copies: int):
        self.resource_id = resource_id  # 物品编号
        self.title = title  # 物品名称
        self.total_copies = total_copies  # 馆一共有多少这样的书
        self.available_copies = (
            total_copies  # 还剩多少这样的书（刚开始等于总数，后续更新）
        )

        # 初始化一个队列，用于存放预约这本书的用户ID
        self.waitlist = Queue()

    # 借书动作
    def borrow_item(self):
        """
        TODO: 借出资源的逻辑

        组员开发提示：
        1. 查库存：if self.available_copies > 0:
        2. 如果有库存，就把库存减 1 (self.available_copies -= 1)
        3. 如果没库存，抛出报错：raise OutOfStockError(f"{self.title} 没库存了")
        """
        if self.available_copies > 0:
            self.available_copies -= 1
            return True  # 成功借出
        else:
            raise OutOfStockError(f"{self.title} 没库存了")

    # 还书动作
    def return_item(self):
        """
        TODO: 归还资源的逻辑
        1. available_copies 加 1 (但不能超过 total_copies)
        2. 检查 waitlist 队列里有没有人在排队，如果有，自动把书借给队列里的第一个人
        """
        if self.available_copies < self.total_copies:
            self.available_copies += 1

        # 检查等待队列
        if not self.waitlist.is_empty():
            # 列表不为空，把书自动借给第一个人
            next_user_id = self.waitlist.dequeue()  # 从队列中取出下一个用户ID
            self.borrow_item()  # 借出一本书给这个用户
            print(f"已自动将 {self.title} 借给排队的用户 {next_user_id}")
            self.available_copies -= 1  # 更新库存，因为已经借出了一本书

            return next_user_id  # 返回被借走的用户ID，方便后续处理
        return None  # 没有用户排队，正常归还


class Book(Resource):
    """图书类，继承自 Resource"""

    def __init__(
        self, resource_id: str, title: str, total_copies: int, author: str, isbn: str
    ):
        # TODO: 调用父类的 __init__ 方法初始化公共属性
        # super().__init__(...)
        self.author = author  # 作者
        self.isbn = isbn  # 书号


class Magazine(Resource):
    """杂志类，继承自 Resource"""

    def __init__(
        self, resource_id: str, title: str, total_copies: int, issue_number: str
    ):
        # TODO: 调用父类初始化，并添加自己的 issue_number 属性
        super().__init__(resource_id, title, total_copies)
        self.issue_number = issue_number  # 期号
