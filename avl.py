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

    def _add_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method for recursive addition of a value to the AVL tree.
        """
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self._add_recursive(node.left, value)
            node.left.parent = node  # Update parent attribute
        else:
            node.right = self._add_recursive(node.right, value)
            node.right.parent = node  # Update parent attribute

        # Update height and balance factor
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Perform rotations if needed
        if balance > 1:
            if value < node.left.value:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if value > node.right.value:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def add(self, value: object) -> None:
        """
        Add a new value to the AVL tree. Duplicate values are allowed.

        O(log N) runtime complexity.

        Parameters:
        - value: The value to be added to the tree.

        Returns:
        - None
        """
        self._root = self._add_recursive(self._root, value)

    def _remove_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method for recursive removal of a value from the AVL tree.
        """
        if node is None:
            return node

        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children, get the inorder successor
            successor_parent, successor = node, node.right
            while successor.left:
                successor_parent, successor = successor, successor.left

            # Copy the inorder successor's value to this node
            node.value = successor.value

            # Remove the inorder successor
            node.right = self._remove_recursive(node.right, successor.value)

        # Update height and balance factor
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Perform rotations if needed
        if balance > 1:
            if self._get_balance(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def remove(self, value: object) -> bool:
        """
        Remove a value from the AVL tree. Returns True if the value is removed,
        otherwise returns False.

        O(log N) runtime complexity.

        Parameters:
        - value: The value to be removed from the tree.

        Returns:
        - bool: True if the value is removed, False otherwise.
        """
        if self._root is None:
            return False

        self._root = self._remove_recursive(self._root, value)

        # Update height of the root after removal
        if self._root:
            self._root.height = 1 + max(self._get_height(self._root.left), self._get_height(self._root.right))

        return True

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Left rotate a subtree rooted with z.
        """
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotate a subtree rooted with y.
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _get_height(self, node: AVLNode) -> int:
        """
        Get the height of a node. If the node is None, return -1.
        """
        if node is None:
            return -1
        return node.height

    def _get_balance(self, node: AVLNode) -> int:
        """
        Get the balance factor of a node.
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)