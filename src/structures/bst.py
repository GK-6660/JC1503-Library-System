from utils.exceptions import ItemNotFoundError

class Node:
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.left = None
        self.right = None
        self.node_level = 0 


class BST:
    def __init__(self):
        self.root = None

    def insert(self, k_val, v_val):
        if self.root == None:
            self.root = Node(k_val, v_val)
            self.root.node_level = 1 
        else:
            self._add_node(self.root, k_val, v_val, 1)

    def _add_node(self, current_node, k_val, v_val, current_level):
        next_level = current_level + 1
        if k_val < current_node.key:
            if current_node.left == None:
                current_node.left = Node(k_val, v_val)
                current_node.left.node_level = next_level
            else:
                self._add_node(current_node.left, k_val, v_val, next_level)
        elif k_val > current_node.key:
            if current_node.right == None:
                current_node.right = Node(k_val, v_val)
                current_node.right.node_level = next_level
            else:
                self._add_node(current_node.right, k_val, v_val, next_level)
        else:
            current_node.value = v_val
            print(f"Key {k_val} already exists, updating value.")

    def search(self, search_key):
        search_result = self._find_node(self.root, search_key)
        if search_result == None:
            print(f"Search failed for key: {search_key}")
            raise ItemNotFoundError("Not found")
        print(f"Key {search_key} found at level {search_result.node_level}.") 
        return search_result.value

    def _find_node(self, current_node_param, target_key):
        if current_node_param == None:
            print(f"Node not found for key {target_key} in this path.")
            return None
        
        node_key_here = current_node_param.key
        if target_key == node_key_here:
            print(f"Found node with key {target_key}.")
            return current_node_param 
        elif target_key < node_key_here:
            print(f"Moving left from {node_key_here} for {target_key}.")
            return self._find_node(current_node_param.left, target_key)
        else: 
            print(f"Moving right from {node_key_here} for {target_key}.")
            return self._find_node(current_node_param.right, target_key)

    def remove(self, key_to_remove):
        print(f"Attempting to remove key: {key_to_remove}")
        self.root = self._remove_node(self.root, key_to_remove)
        if self.root == None:
            print("Tree is now empty after removal.")
        else:
            print(f"Key {key_to_remove} removed (if it existed).")

    def _remove_node(self, current_node_for_remove, key_to_remove):
        if current_node_for_remove == None:
            print(f"Key {key_to_remove} not found in this subtree.")
            return None

        if key_to_remove < current_node_for_remove.key:
            current_node_for_remove.left = self._remove_node(current_node_for_remove.left, key_to_remove)
        elif key_to_remove > current_node_for_remove.key:
            current_node_for_remove.right = self._remove_node(current_node_for_remove.right, key_to_remove)
        else: 
            print(f"Node with key {key_to_remove} found for removal.")
            if current_node_for_remove.left == None and current_node_for_remove.right == None:
                print("Node is a leaf, simply removing.")
                return None
            
            if current_node_for_remove.left == None:
                print("Node has only right child, promoting right child.")
                return current_node_for_remove.right
            if current_node_for_remove.right == None:
                print("Node has only left child, promoting left child.")
                return current_node_for_remove.left
            
            print("Node has two children, finding successor.")
            successor_node = self._find_min_node(current_node_for_remove.right)
            current_node_for_remove.key = successor_node.key
            current_node_for_remove.value = successor_node.value
            current_node_for_remove.right = self._remove_node(current_node_for_remove.right, successor_node.key)
        
        return current_node_for_remove

    def _find_min_node(self, start_node):
        current_min_node = start_node
        while current_min_node.left != None:
            current_min_node = current_min_node.left
            print(f"Traversing left to find min. Current: {current_min_node.key}")
        print(f"Found minimum node with key: {current_min_node.key}")
        return current_min_node

    def to_list(self):
        all_items_list = []
        self._inorder_traversal(self.root, all_items_list)
        print(f"Converted BST to list with {len(all_items_list)} items.")
        return all_items_list

    def _inorder_traversal(self, current_node_traversal, result_array):
        if current_node_traversal:
            self._inorder_traversal(current_node_traversal.left, result_array)
            result_array.append(current_node_traversal.value)
            self._inorder_traversal(current_node_traversal.right, result_array)
        else:
            print("Reached end of a branch in traversal.")