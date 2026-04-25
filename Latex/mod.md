### **Project Report: Library Management System**
**Course:** JC1503: Object-Oriented Programming
**Team:** CS Group 5
**Date:** April 24, 2026

### **1. System Architecture & Domain**
Manual library tracking scales poorly. We built a digitized management system handling books, magazines, and user transaction histories. The platform provides simple operational nodes for adding, searching, and moving inventory while logging all transactions.

Instead of fragmented scripts, a Controller pattern drives the application. `LibSys` resides in `main.py`. It bridges the command-line interface and the underlying data models. Users execute actions via the CLI. Memory handles operational states directly. We keep users in a Hash Table and inventory in a Binary Search Tree. State persistence falls to a dedicated `Storage` module. JSON handles the I/O. The system triggers `to_dict()` and `to_list()` during teardown and rebuilds objects on startup.

### **2. Object-Oriented Implementation**
We structured the domain models around strict OOP paradigms.

* **Inheritance**: `Resource` acts as the base class. It dictates shared states like `resource_id` and implements the `borrow_item` function. `Book` and `Magazine` inherit this foundation. They append specific metadata, such as issue numbers or authors.
* **Composition**: Python lists were bypassed. Custom structures live directly inside the models. The `User` class instantiates our `DoublyLinkedList` for borrowing history. Waitlists rely on a custom `Queue` nested inside `Resource`.
* **Encapsulation & Polymorphism**: State mutations require specific method calls. Illegal operations throw custom exceptions like `OutOfStockError`. Serialization required polymorphic behavior. Child classes override `to_dict()`. Rebuilding memory states relies on the `@classmethod from_dict(cls)` implementation.

### **3. Custom Data Structures**
Standard libraries were ignored to meet project constraints. We built the following primitives:

* **Stack (LIFO)**: Injected into `main.py` for global undo functionality. It pushes system states. Users can reverse mistakes easily.
* **Queue (FIFO)**: Attached to `Resource`. Returned high-demand items trigger `dequeue()`, reallocating the resource automatically to the next waiting user.
* **Binary Search Tree**: Organizes books by title string comparison. Insert and search are recursive. 
* **Hash Table**: Fixed array size of 100. Maps `User` objects via ID. Chaining resolves collisions.

### **4. Efficiency & Complexity Trade-offs**
Our data structures face specific Big-O trade-offs. The Hash Table computes ASCII sums modulo 100. Average lookup hits $O(1)$. Anagrams guarantee collision. This forces worst-case $O(n)$ traversal along the chain. 

The BST averages $O(\log n)$ for search. No auto-balancing exists. Alphabetical data dumps degrade the tree into a linked line. Search complexity plummets to $O(n)$.

### **5. Development Lifecycle & Bug Resolution**
We followed iterative integration. Base OOP constructs came first. We then swapped Python lists for custom nodes. Testing needed initial states. Booting creates 30 users, 40 books, and 20 magazines inside `library_data.json` automatically via `generate_initial_data()`.

Integration surfaced several blocks. 
The borrowing module threw an `AttributeError`. The `search` routine returned the structural `Node` wrapper, not the payload. Invoking `node.value.borrow_item()` fixed the pointer issue. 

Passing custom objects to `json.dump()` threw `TypeError`s. Complex memory representations had to be flattened. Implementing `to_dict()` and `to_list()` stripped objects down to base Python dictionaries. 

Merging into `main.py` broke execution. The "Menu Logic" and "Persistence" branches collided. Manual diff resolution patched the sequence. We forced `load_data()` to execute synchronously before the CLI loop started.

### **6. Testing & Reflection**
Basic structures underwent unit checks first to ensure chaining worked. CLI end-to-end testing followed. Repeatedly borrowing items and triggering the stack's "undo" validated memory state rollbacks.

The architecture separates structural nodes from manager logic. This maintained readable code boundaries. Core requirements are functional. 

Technical debt is evident. The naive hashing algorithm and hardcoded capacity of 100 guarantee chain degradation. $O(1)$ efficiency will vanish at scale. Pre-sorted JSON loading skews the unbalanced BST instantly, creating $O(n)$ bottlenecks.

Future iterations require refactoring the Hash Table to use DJB2 with dynamic resizing. The BST needs upgrading to an AVL Tree to enforce $O(\log n)$ constraints. A graphical interface should replace the CLI.

Writing low-level structures clarified memory management. Tracing `next`, `left`, and `right` pointers forces an understanding of boundaries. Interface contracts matter deeply in team environments. Returning a wrapper instead of a domain object breaks downstream dependencies.