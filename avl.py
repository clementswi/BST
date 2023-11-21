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

    def add(self, value: object) -> None: #passes the first two prescribed tests
        """
                Add a new value to the AVL tree while maintaining its AVL property.

                Parameters:
                - value: The value to be added to the tree.

                Returns:
                - None
                """
        if not self.contains(value):
            self._root = self._add_recursive(self._root, value)
    def _add_recursive(self, node: AVLNode, value: object) -> AVLNode:
        # Perform standard BST insert
        node = super()._add_recursive(node, value)

        # Update the height of the current node.
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check and perform rotations if needed.
        balance = self._get_balance(node)

        # Left-Left case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)

        # Right-Right case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)

        # Left-Right case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right-Left case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _remove_node_with_one_child(self, parent: AVLNode, node: AVLNode) -> None:
        # Override the method to update heights before returning.
        super()._remove_node_with_one_child(parent, node)

        # Update height of the parent.
        if parent:
            parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))

        # Check and perform rotations if needed.
        self._balance_after_removal(parent)

    def _remove_node_with_two_children(self, parent: AVLNode, node: AVLNode) -> None:
        # Override the method to update heights before returning.
        super()._remove_node_with_two_children(parent, node)

        # Update height of the parent.
        if parent:
            parent.height = 1 + max(self._get_height(parent.left), self._get_height(parent.right))

        # Check and perform rotations if needed.
        self._balance_after_removal(parent)

    def _balance_after_removal(self, node: AVLNode) -> None:
        # Check and perform rotations if needed.
        while node:
            balance = self._get_balance(node)

            # Left-Left case
            if balance > 1 and self._get_balance(node.left) >= 0:
                node = self._right_rotate(node)

            # Right-Right case
            elif balance < -1 and self._get_balance(node.right) <= 0:
                node = self._left_rotate(node)

            # Left-Right case
            elif balance > 1 and self._get_balance(node.left) < 0:
                node.left = self._left_rotate(node.left)
                node = self._right_rotate(node)

            # Right-Left case
            elif balance < -1 and self._get_balance(node.right) > 0:
                node.right = self._right_rotate(node.right)
                node = self._left_rotate(node)

            node = node.parent

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _get_balance(self, node: AVLNode) -> int:
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_height(self, node: AVLNode) -> int:
        if node is None:
            return 0
        return node.height