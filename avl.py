# Name: William Clements
# OSU Email: clemenw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: AVL Tree
# Due Date: 11/20/2023
# Description: Using a stack and queue classes, as well as a BST class, to implement an AVL tree


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value):
        """
        Add a new value to the AVL tree. Duplicate values are allowed.
        If a node with that value is already in the tree, the new value
        is added to the right subtree of that node.

        Overrides the add() method in the BST class to ensure AVL balance.

        O(log N) runtime complexity.

        Parameters:
        - value: The value to be added to the tree.

        Returns:
        - None
        """
        if self._root is None:
            # If the tree is empty, create a new node as the root.
            self._root = AVLNode(value)
        else:
            # Call a helper function to recursively add the value to the tree.
            self._root = self._add_recursive(self._root, value)

        # Update the height of the root node.
        self._root.height = 1 + max(self._get_height(self._root.left), self._get_height(self._root.right))

    def _add_recursive(self, node, value):
        """
        Helper method for recursive addition of a value to the AVL tree.

        Parameters:
        - node: The current node in the recursion.
        - value: The value to be added to the tree.

        Returns:
        - AVLNode: The root of the modified subtree.
        """
        # Perform standard BST insert
        if node is None:
            return AVLNode(value)
        elif value < node.value:
            node.left = self._add_recursive(node.left, value)
            node.left.parent = node  # Update parent pointer
        else:
            node.right = self._add_recursive(node.right, value)
            node.right.parent = node  # Update parent pointer

        # Update height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Rebalance the AVL tree
        return self._balance_recursive(node)

    def remove(self, value):
        """
        Remove a value from the AVL tree. Returns True if the value is removed,
        otherwise returns False.

        Overrides the remove() method in the BST class to ensure AVL balance.

        O(log N) runtime complexity.

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

        # Rebalance the AVL tree
        self._balance_tree()

        return True

    def _remove_leaf(self, parent, node):
        """
        Helper method to remove a leaf node.

        Parameters:
        - parent: The parent node of the leaf node.
        - node: The leaf node to be removed.

        Returns:
        - None
        """
        super()._remove_leaf(parent, node)
        # Update height of the parent node
        if parent:
            parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))

    def _remove_node_with_one_child(self, parent, node):
        """
        Helper method to remove a node with one child.

        Parameters:
        - parent: The parent node of the node to be removed.
        - node: The node to be removed.

        Returns:
        - None
        """
        super()._remove_node_with_one_child(parent, node)
        # Update height of the parent node
        if parent:
            parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))

    def _remove_node_with_two_children(self, parent, node):
        """
        Helper method to remove a node with two children.

        Parameters:
        - parent: The parent node of the node to be removed.
        - node: The node to be removed.

        Returns:
        - None
        """
        super()._remove_node_with_two_children(parent, node)
        # Update height of the parent node
        if parent:
            parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))

    def _balance_tree(self):
        """
        Rebalance the AVL tree after an insertion or removal.
        """
        if self._root:
            self._root = self._balance_recursive(self._root)

    def _balance_recursive(self, node):
        """
        Recursively balance the AVL tree.
        """
        # Update height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check balance factor
        balance = self._get_balance(node)

        # Left Heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                # Left-Right Rotation
                node.left = self._left_rotate(node.left)
            # Left-Left Rotation
            return self._right_rotate(node)

        # Right Heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                # Right-Left Rotation
                node.right = self._right_rotate(node.right)
            # Right-Right Rotation
            return self._left_rotate(node)

        return node

    def _get_height(self, node):
        """
        Get the height of a node.
        """
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        """
        Get the balance factor of a node.
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        """
        Left rotation on the AVL tree.
        """
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        # Update height of the rotated nodes
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, y):
        """
        Right rotation on the AVL tree.
        """
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        # Update height of the rotated nodes
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x