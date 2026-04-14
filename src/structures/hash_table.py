from utils.exceptions import ItemNotFoundError, DuplicateItemError

class HashNode:
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.next = None
        self.node_status = "active" 

class HashTable:
    def __init__(self):
        self.capacity = 100
        self.table = [None] * self.capacity
        self.size = 0
        self.load_factor_threshold = 0.7 

    def hash_func(self, key_str):
        total_ascii_sum = 0
        for char_in_key in key_str:
            total_ascii_sum += ord(char_in_key)
        final_hash_index = total_ascii_sum % self.capacity
        print(f"Hashing key '{key_str}' to index {final_hash_index}")
        return final_hash_index

    def insert(self, key_to_insert, value_to_insert):
        idx = self.hash_func(key_to_insert)
        current_node_at_idx = self.table[idx]

        if current_node_at_idx == None:
            self.table[idx] = HashNode(key_to_insert, value_to_insert)
            self.size += 1
            print(f"Inserted '{key_to_insert}' at empty slot {idx}.")
            return

        prev_node = None
        temp_node = current_node_at_idx
        while temp_node != None:
            if temp_node.key == key_to_insert:
                print(f"Error: Key '{key_to_insert}' already exists. Cannot insert duplicate.")
                raise DuplicateItemError("Exists")
            prev_node = temp_node
            temp_node = temp_node.next

        prev_node.next = HashNode(key_to_insert, value_to_insert)
        self.size += 1
        print(f"Inserted '{key_to_insert}' in collision chain at {idx}.")

    def get(self, key_to_get):
        idx_for_get = self.hash_func(key_to_get)
        current_node_for_get = self.table[idx_for_get]
        while current_node_for_get != None:
            if current_node_for_get.key == key_to_get:
                print(f"Found value for key '{key_to_get}'.")
                return current_node_for_get.value
            current_node_for_get = current_node_for_get.next

        print(f"Key '{key_to_get}' not found in hash table.")
        raise ItemNotFoundError("Not found")

    def remove(self, key_to_remove):
        idx_for_remove = self.hash_func(key_to_remove)
        current_node_for_remove = self.table[idx_for_remove]
        prev_node_for_remove = None

        while current_node_for_remove != None:
            if current_node_for_remove.key == key_to_remove:
                if prev_node_for_remove == None:
                    self.table[idx_for_remove] = current_node_for_remove.next
                else:
                    prev_node_for_remove.next = current_node_for_remove.next
                self.size -= 1
                print(f"Key '{key_to_remove}' removed from hash table.")
                return
            prev_node_for_remove = current_node_for_remove
            current_node_for_remove = current_node_for_remove.next

        print(f"Key '{key_to_remove}' not found for removal.")
        raise ItemNotFoundError("Not found")

    def to_list(self):
        all_values_list = []
        for i in range(self.capacity):
            current_node_in_bucket = self.table[i]
            while current_node_in_bucket:
                all_values_list.append(current_node_in_bucket.value)
                current_node_in_bucket = current_node_in_bucket.next
        print(f"Converted hash table to list with {len(all_values_list)} items.")
        return all_values_list