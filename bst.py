# Name: William Clements
# OSU Email: clemenwi@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: BST implementation
# Due Date: 11/20/2023
# Description: Binary Search tree implementation using stack and queue class


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None: #passes the prescribed tests
        """
            Add a new value to the tree. Duplicate values are allowed.
            If a node with that value is already in the tree, the new value
            is added to the right subtree of that node.

            O(N) runtime complexity.

            Parameters:
            - value: The value to be added to the tree.

            Returns:
            - None
        """
        if self._root is None:
            # If the tree is empty, create a new node as the root.
            self._root = BSTNode(value)
        else:
            # Call a helper function to recursively add the value to the tree.
            self._add_recursive(self._root, value)

    def _add_recursive(self, node: BSTNode, value: object) -> BSTNode:
        """
        Helper method for recursive addition of a value to the BST.

        Parameters:
        - node: The current node in the recursion.
        - value: The value to be added to the tree.

        Returns:
        - BSTNode: The root of the modified subtree.
        """
        # Perform standard BST insert
        if node is None:
            return BSTNode(value)
        elif value < node.value:
            node.left = self._add_recursive(node.left, value)
        else:
            node.right = self._add_recursive(node.right, value)

        return node

    def remove(self, value: object) -> bool: #passes the prescribed tests
        """
                Remove a value from the tree. Returns True if the value is removed,
                otherwise returns False.

                O(N) runtime complexity.

                Parameters:
                - value: The value to be removed from the tree.

                Returns:
                - bool: True if the value is removed, False otherwise.
                """
        # Initialize parent and current pointers.
        parent, current = None, self._root

        # Search for the node to be removed.
        while current and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        # If the value is not found, return False.
        if current is None:
            return False

        # Check the number of children of the node to be removed.
        if current.left is None and current.right is None:
            # Case 1: Node has no children, just remove it.
            self._remove_leaf(parent, current)
        elif current.left is not None and current.right is not None:
            # Case 2: Node has two children, find the inorder successor.
            self._remove_node_with_two_children(parent, current)
        else:
            # Case 3: Node has one child, replace it with the child.
            self._remove_node_with_one_child(parent, current)

        return True

    def _remove_leaf(self, parent: BSTNode, node: BSTNode) -> None:
        """
        Helper method to remove a leaf node.

        Parameters:
        - parent: The parent node of the leaf node.
        - node: The leaf node to be removed.

        Returns:
        - None
        """
        if parent is None:
            # If the node to be removed is the root, set the root to None.
            self._root = None
        elif parent.left == node:
            # If the node is the left child, set the left child of the parent to None.
            parent.left = None
        else:
            # If the node is the right child, set the right child of the parent to None.
            parent.right = None

    def _remove_node_with_one_child(self, parent: BSTNode, node: BSTNode) -> None:
        """
        Helper method to remove a node with one child.

        Parameters:
        - parent: The parent node of the node to be removed.
        - node: The node to be removed.

        Returns:
        - None
        """
        # Determine the non-empty child.
        child = node.left if node.left is not None else node.right

        if parent is None:
            # If the node to be removed is the root, set the root to the child.
            self._root = child
        elif parent.left == node:
            # If the node is the left child, set the left child of the parent to the child.
            parent.left = child
        else:
            # If the node is the right child, set the right child of the parent to the child.
            parent.right = child

    def _remove_node_with_two_children(self, parent: BSTNode, node: BSTNode) -> None:
        """
        Helper method to remove a node with two children.

        Parameters:
        - parent: The parent node of the node to be removed.
        - node: The node to be removed.

        Returns:
        - None
        """
        # Find the inorder successor (leftmost child of the right subtree).
        successor_parent, successor = node, node.right
        while successor.left:
            successor_parent, successor = successor, successor.left

        # Replace the node's value with the value of the inorder successor.
        node.value = successor.value

        # Remove the inorder successor (which has at most one child).
        self._remove_node_with_one_child(successor_parent, successor)

                               #

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has no subtrees (no left or right nodes)
        pass

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has a left or right subtree (only)
        pass

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)
        pass

    def contains(self, value: object) -> bool: #passes the prescribed tests
        """
                Returns True if the value is in the tree, otherwise returns False.
                If the tree is empty, the method returns False.

                O(N) runtime complexity.

                Parameters:
                - value: The value to check for in the tree.

                Returns:
                - bool: True if the value is in the tree, False otherwise.
                """
        return self._contains_recursive(self._root, value)

    def _contains_recursive(self, node: BSTNode, value: object) -> bool:
        """
        Helper method for recursive search in the tree.

        Parameters:
        - node: The current node in the recursion.
        - value: The value to check for in the tree.

        Returns:
        - bool: True if the value is in the tree, False otherwise.
        """
        if node is None:
            # If the current node is None, the value is not found.
            return False
        elif node.value == value:
            # If the value is equal to the current node's value, it is found.
            return True
        elif value < node.value:
            # If the value is less than the current node's value,
            # search in the left subtree.
            return self._contains_recursive(node.left, value)
        else:
            # If the value is greater than the current node's value,
            # search in the right subtree.
            return self._contains_recursive(node.right, value)

    def inorder_traversal(self) -> Queue: #passes the prescribed tests
        """
                Perform an inorder traversal of the tree and return a Queue object
                that contains the values of the visited nodes in the order they were visited.
                If the tree is empty, return an empty Queue.

                O(N) runtime complexity.

                Returns:
                - Queue: Queue object containing values of visited nodes.
                """
        result_queue = Queue()  # Queue to store the values of visited nodes.
        self._inorder_traversal_recursive(self._root, result_queue)
        return result_queue

    def _inorder_traversal_recursive(self, node: BSTNode, result_queue: Queue) -> None:
        """
        Helper method for recursive inorder traversal.

        Parameters:
        - node: The current node in the recursion.
        - result_queue: Queue to store the values of visited nodes.

        Returns:
        - None
        """
        if node is not None:
            # Traverse the left subtree.
            self._inorder_traversal_recursive(node.left, result_queue)
            # Enqueue the current node's value.
            result_queue.enqueue(node.value)
            # Traverse the right subtree.
            self._inorder_traversal_recursive(node.right, result_queue)

    def find_min(self) -> object: #passes the prescribed tests
        """
                Returns the lowest value in the tree. If the tree is empty, return None.

                O(N) runtime complexity.

                Returns:
                - object: The lowest value in the tree or None if the tree is empty.
                """
        if self._root is not None:
            return self._find_min_recursive(self._root)
        else:
            return None

    def _find_min_recursive(self, node: BSTNode) -> object:
        """
        Helper method for recursive search of the minimum value in the tree.

        Parameters:
        - node: The current node in the recursion.

        Returns:
        - object: The minimum value in the subtree rooted at the given node.
        """
        # The minimum value is the leftmost node in the BST.
        while node.left is not None:
            node = node.left
        return node.value

    def find_max(self) -> object: #passes the prescribed tests
        """
                Returns the highest value in the tree. If the tree is empty, return None.

                O(N) runtime complexity.

                Returns:
                - object: The highest value in the tree or None if the tree is empty.
                """
        if self._root is not None:
            return self._find_max_recursive(self._root)
        else:
            return None

    def _find_max_recursive(self, node: BSTNode) -> object:
        """
        Helper method for recursive search of the maximum value in the tree.

        Parameters:
        - node: The current node in the recursion.

        Returns:
        - object: The maximum value in the subtree rooted at the given node.
        """
        # The maximum value is the rightmost node in the BST.
        while node.right is not None:
            node = node.right
        return node.value

    def is_empty(self) -> bool: #passes the prescribed tests
        """
                Returns True if the tree is empty, otherwise returns False.

                O(1) runtime complexity.

                Returns:
                - bool: True if the tree is empty, False otherwise.
                """
        return self._root is None

    def make_empty(self) -> None: #passes the prescribed tests
        """
                Removes all the nodes from the tree.

                O(1) runtime complexity.

                Returns:
                - None
                """
        self._root = None
