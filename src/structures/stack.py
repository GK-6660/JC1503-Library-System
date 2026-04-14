class StackNode:
    def __init__(self, val_data):
        self.value = val_data
        self.next = None
        self.node_type = "stack_element" 

class Stack:
    def __init__(self):
        self.top_node = None
        self.item_count = 0
        self.stack_capacity = 1000 

    def push(self, item_to_push):
        new_stack_element = StackNode(item_to_push)
        
        is_stack_empty_now = (self.item_count == 0)
        if is_stack_empty_now == True:
            self.top_node = new_stack_element
            print(f"Pushed first item: {item_to_push}")
        else:
            new_stack_element.next = self.top_node
            self.top_node = new_stack_element
            print(f"Pushed item: {item_to_push}")
            
        self.item_count = self.item_count + 1

    def pop(self):
        if self.item_count == 0:
            print("Stack is empty, nothing to pop.")
            return None
            
        old_top_node_ref = self.top_node
        value_to_return = old_top_node_ref.value
        
        self.top_node = old_top_node_ref.next
        
        self.item_count = self.item_count - 1
        print(f"Popped item: {value_to_return}")
        return value_to_return