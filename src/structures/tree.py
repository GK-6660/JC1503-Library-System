import sys
import os
from utils.exceptions import ItemNotFoundError, DuplicateItemError

class Node:
    def __init__(self, d_val):
        self.data = d_val
        self.nxt = None
        self.prv = None
        self.node_type_str = "generic_node" 

class DList:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0
        self.list_id = "DL_" + str(id(self)) 

    def append(self, data_to_add):
        new_node_for_list = Node(data_to_add)
        
        is_list_empty_check = (self.size == 0)
        if is_list_empty_check == True:
            self.first = new_node_for_list
            self.last = new_node_for_list
            print(f"Added first item to DList: {data_to_add}")
        else:
            new_node_for_list.prv = self.last
            self.last.nxt = new_node_for_list
            self.last = new_node_for_list
            print(f"Appended item to DList: {data_to_add}")
        self.size = self.size + 1

    def remove(self, data_to_remove):
        current_node_in_list = self.first
        
        while current_node_in_list != None:
            node_value = current_node_in_list.data
            if node_value == data_to_remove:
                prev_node_ref = current_node_in_list.prv
                next_node_ref = current_node_in_list.nxt
                
                if prev_node_ref != None:
                    prev_node_ref.nxt = next_node_ref
                if next_node_ref != None:
                    next_node_ref.prv = prev_node_ref
                    
                if current_node_in_list == self.first:
                    self.first = next_node_ref
                if current_node_in_list == self.last:
                    self.last = prev_node_ref
                    
                self.size = self.size - 1
                print(f"Removed item '{data_to_remove}' from DList.")
                return True
            current_node_in_list = current_node_in_list.nxt
            
        print(f"Item '{data_to_remove}' not found in DList for removal.")
        return False

    def __len__(self):
        return self.size

class TNode:
    def __init__(self, node_name):
        self.name = node_name
        self.books = DList()
        self.children = DList()
        self.parent = None
        self.node_creation_timestamp = "some_time" 

class CTree:
    def __init__(self, root_name="Lib"):
        self.root = TNode(root_name)
        self.tree_depth_limit = 10 

    def add_c(self, parent_category_name, new_category_name):
        parent_node_obj = self._find(self.root, parent_category_name)

        if parent_node_obj == None:
            print("Error: Parent category not found for adding new category.")
            raise ItemNotFoundError("No parent")

        is_duplicate_category = False
        current_child_node_in_list = parent_node_obj.children.first
        
        while current_child_node_in_list != None:
            child_node_name = current_child_node_in_list.data.name
            if child_node_name == new_category_name:
                is_duplicate_category = True
            current_child_node_in_list = current_child_node_in_list.nxt
            
        if is_duplicate_category == True:
            print("Error: Duplicate category found. Cannot add.")
            raise DuplicateItemError("Dup")

        new_category_tnode = TNode(new_category_name)
        new_category_tnode.parent = parent_node_obj
        
        parent_node_obj.children.append(new_category_tnode)
        print("New category added successfully.")
        return True

    def _find(self, current_tree_node, target_node_name):
        current_node_name_val = current_tree_node.name
        if current_node_name_val == target_node_name:
            print(f"Found target node: {target_node_name}")
            return current_tree_node

        temp_child_node_ptr = current_tree_node.children.first
        while temp_child_node_ptr != None:
            recursive_result_node = self._find(temp_child_node_ptr.data, target_node_name)
            if recursive_result_node != None:
                return recursive_result_node
            temp_child_node_ptr = temp_child_node_ptr.nxt
            
        print(f"Target node '{target_node_name}' not found in this subtree.")
        return None

    def disp(self, node_to_display=None, current_level=0):
        if node_to_display == None:
            node_to_display = self.root
            print("Displaying Tree Structure:")

        indent_string = "  " * current_level
        print(indent_string + "-> " + node_to_display.name)

        child_pointer_for_display = node_to_display.children.first
        while child_pointer_for_display != None:
            self.disp(child_pointer_for_display.data, current_level + 1)
            child_pointer_for_display = child_pointer_for_display.nxt

    def get_all(self, start_node_for_get_all=None):
        if start_node_for_get_all == None:
            start_node_for_get_all = self.root
            all_categories_list = []
            print("Starting to collect all categories from root.")
        else:
            all_categories_list = []

        all_categories_list.append(start_node_for_get_all.name)

        current_child_for_get_all = start_node_for_get_all.children.first
        while current_child_for_get_all != None:
            all_categories_list.extend(self.get_all(current_child_for_get_all.data))
            current_child_for_get_all = current_child_for_get_all.nxt

        return all_categories_list

    def find_c(self, category_name_to_find):
        found_node = self._find(self.root, category_name_to_find)
        if found_node == None:
            print(f"Category '{category_name_to_find}' was not found.")
            raise ItemNotFoundError(f"Not found {category_name_to_find}")
        print(f"Category '{category_name_to_find}' found.")
        return found_node

    def get_p(self, category_name_for_path):
        node_for_path = self.find_c(category_name_for_path)
        path_elements_list = []
        current_path_node = node_for_path
        while current_path_node:
            path_elements_list.insert(0, current_path_node.name)
            current_path_node = current_path_node.parent
        print(f"Path for '{category_name_for_path}': {path_elements_list}")
        return path_elements_list

    def rm_c(self, category_to_remove_name):
        try:
            node_to_be_removed = self.find_c(category_to_remove_name)
        except ItemNotFoundError:
            print(f"Cannot remove '{category_to_remove_name}': Not found.")
            return False

        if node_to_be_removed.parent == None:
            print(f"Cannot remove root category '{category_to_remove_name}'.")
            return False

        removal_successful = node_to_be_removed.parent.children.remove(node_to_be_removed)
        if removal_successful == True:
            print(f"Category '{category_to_remove_name}' removed successfully.")
            return True
        else:
            print(f"Failed to remove category '{category_to_remove_name}'.")
            return False

    def mv_c(self, category_to_move_name, new_parent_category_name):
        try:
            node_to_move_obj = self.find_c(category_to_move_name)
            new_parent_node_obj = self.find_c(new_parent_category_name)
        except ItemNotFoundError:
            print("Error: Category to move or new parent not found.")
            return False

        if node_to_move_obj.parent == None:
            print(f"Cannot move root category '{category_to_move_name}'.")
            return False

        if not node_to_move_obj.parent.children.remove(node_to_move_obj):
            print(f"Failed to remove '{category_to_move_name}' from its current parent.")
            return False
            
        new_parent_node_obj.children.append(node_to_move_obj)
        node_to_move_obj.parent = new_parent_node_obj
        print(f"Category '{category_to_move_name}' moved to '{new_parent_category_name}'.")
        return True


if __name__ == "__main__":
    my_library_tree = CTree()

    my_library_tree.add_c("Lib", "Science")
    my_library_tree.add_c("Lib", "Art")
    my_library_tree.add_c("Science", "Physics")
    my_library_tree.add_c("Science", "Chemistry")
    
    print("\nInitial Tree Display:")
    my_library_tree.disp()

    print("\nAttempting to move Chemistry to Art:")
    move_result = my_library_tree.mv_c("Chemistry", "Art")
    if move_result == True:
        print("Move operation reported success.")
    else:
        print("Move operation reported failure.")
    
    print("\nTree Display After Move:")
    my_library_tree.disp()

    print("\nAttempting to remove Physics:")
    remove_result = my_library_tree.rm_c("Physics")
    if remove_result == True:
        print("Remove operation reported success.")
    else:
        print("Remove operation reported failure.")

    print("\nTree Display After Remove:")
    my_library_tree.disp()

    print("\nGetting path for Art:")
    art_path = my_library_tree.get_p("Art")
    print(f"Path: {art_path}")

    print("\nGetting all categories:")
    all_cats = my_library_tree.get_all()
    print(f"All categories: {all_cats}")