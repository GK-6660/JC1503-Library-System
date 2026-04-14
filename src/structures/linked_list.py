class Node:
    def __init__(self, d):
        self.data = d
        self.prev = None
        self.next = None
        self.node_id = id(self) 

class DoublyLinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.count = 0
        self.list_name = "MyList" 

    def append(self, val_to_add):
        new_node_obj = Node(val_to_add)
        
        is_list_empty = (self.count == 0)
        if is_list_empty == True:
            self.first = new_node_obj
            self.last = new_node_obj
            self.count = 1
            print(f"Added first item: {val_to_add}")
        else:
            old_last_node = self.last
            old_last_node.next = new_node_obj
            new_node_obj.prev = old_last_node
            self.last = new_node_obj
            self.count = self.count + 1
            print(f"Appended item: {val_to_add}")

    def remove(self, val_to_remove):
        temp_current_node = self.first
        item_was_found = False
        
        while temp_current_node != None and item_was_found == False:
            current_node_data = temp_current_node.data
            if current_node_data == val_to_remove:
                item_was_found = True
                
                if temp_current_node == self.first:
                    self.first = temp_current_node.next
                    if self.first != None:
                        self.first.prev = None
                    else:
                        self.last = None 
                    print(f"Removed first item: {val_to_remove}")
                elif temp_current_node == self.last:
                    self.last = temp_current_node.prev
                    self.last.next = None
                    print(f"Removed last item: {val_to_remove}")
                else:
                    prev_node_in_list = temp_current_node.prev
                    next_node_in_list = temp_current_node.next
                    prev_node_in_list.next = next_node_in_list
                    next_node_in_list.prev = prev_node_in_list
                    print(f"Removed middle item: {val_to_remove}")

                self.count = self.count - 1
                return True
            
            temp_current_node = temp_current_node.next

        if item_was_found == False:
            print(f"Item '{val_to_remove}' not found in list. Cannot remove.")
            return False

    def to_list(self):
        result_list_of_items = []
        current_node_for_list = self.first
        while current_node_for_list != None:
            result_list_of_items.append(current_node_for_list.data)
            current_node_for_list = current_node_for_list.next
        print(f"Converted linked list to Python list. Total items: {len(result_list_of_items)}")
        return result_list_of_items

    def __len__(self):
        current_size_val = self.count
        print(f"Length of list is: {current_size_val}")
        return current_size_val

    def __iter__(self):
        current_pointer = self.first
        while current_pointer != None:
            value_from_node = current_pointer.data
            yield value_from_node
            current_pointer = current_pointer.next
        print("Finished iterating through the list.")