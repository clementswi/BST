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

    def _height(self, node):
        """Helper method to get the height of a node."""
        if node is None:
            return -1
        return node.height

    def _add_recursive(self, node: AVLNode, value: object) -> AVLNode:
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
        else:
            node.right = self._add_recursive(node.right, value)

        # Update height of the current node
        node.height = 1 + max(self._height(node.left), self._height(node.right))

        # Get the balance factor and perform rotations if needed
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node  # Return the new root after rotations

    def _get_balance(self, node: AVLNode) -> int:
        """
        Get the balance factor of a node.

        Parameters:
        - node: The AVL node.

        Returns:
        - int: The balance factor.
        """
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Perform a right rotation.

        Parameters:
        - z: The node at which the rotation is performed.

        Returns:
        - AVLNode: The new root after rotation.
        """
        y = z.left
        T2 = y.right

        # Perform rotation
        y.right = z
        z.left = T2

        # Update heights
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def _rotate_left(self, y: AVLNode) -> AVLNode:
        """
        Perform a left rotation.

        Parameters:
        - y: The node at which the rotation is performed.

        Returns:
        - AVLNode: The new root after rotation.
        """
        x = y.right
        T2 = x.left

        # Perform rotation
        x.left = y
        y.right = T2

        # Update heights
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def remove(self, value: object) -> bool:
        """
                Remove the value from the AVL tree.

                Parameters:
                - value: The value to be removed.

                Returns:
                - bool: True if the value is removed, False otherwise.
                """
        if not self.contains(value):
            return False

        self._root = self._remove_recursive(self._root, value)
        return True

    def _remove_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method for recursive removal of a value from the AVL tree.

        Parameters:
        - node: The current node in the recursion.
        - value: The value to be removed.

        Returns:
        - AVLNode: The root of the modified subtree.
        """
        if node is None:
            return None

        # Perform standard BST delete
        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the inorder successor (smallest
            # in the right subtree)
            successor = self._get_min_value_node(node.right)

            # Copy the inorder successor's value to this node
            node.value = successor.value

            # Delete the inorder successor
            node.right = self._remove_recursive(node.right, successor.value)

        # Update height of the current node
        node.height = 1 + max(self._height(node.left), self._height(node.right))

        # Get the balance factor and perform rotations if needed
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_min_value_node(self, node: AVLNode) -> AVLNode:
        """
        Helper method to find the node with the minimum value in a subtree.

        Parameters:
        - node: The root of the subtree.

        Returns:
        - AVLNode: The node with the minimum value.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current