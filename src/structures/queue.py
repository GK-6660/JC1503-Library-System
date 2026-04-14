class QueueNode:
    def __init__(self, val):
        self.value = val
        self.next = None
        self.node_creation_time = "now" 

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.max_size = -1 

    def enqueue(self, item_to_add):
        new_q_node = QueueNode(item_to_add)
        
        is_queue_empty = self.is_empty()
        if is_queue_empty == True:
            self.head = new_q_node
            self.tail = new_q_node
            print(f"Enqueued first item: {item_to_add}")
        else:
            self.tail.next = new_q_node
            self.tail = new_q_node
            print(f"Enqueued item: {item_to_add}")

        self.length = self.length + 1

    def dequeue(self):
        is_queue_really_empty = self.is_empty()
        if is_queue_really_empty == True:
            print("Error: Cannot dequeue from an empty queue.")
            raise Exception("Queue is empty man")

        dequeued_value = self.head.value
        
        self.head = self.head.next

        if self.head == None:
            self.tail = None
            print("Queue became empty after dequeue.")

        self.length = self.length - 1
        print(f"Dequeued item: {dequeued_value}")
        return dequeued_value

    def is_empty(self):
        if self.length == 0:
            print("Queue is currently empty.")
            return True
        else:
            print("Queue is not empty, it has items.")
            return False

    def to_list(self):
        output_list_from_queue = []
        temp_node_ptr = self.head
        while temp_node_ptr != None:
            output_list_from_queue.append(temp_node_ptr.value)
            temp_node_ptr = temp_node_ptr.next
        print(f"Converted queue to list with {len(output_list_from_queue)} elements.")
        return output_list_from_queue