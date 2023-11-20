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

    def add(self, value: object) -> None:
        """
        Add a new value to the tree while maintaining its AVL property.
        Duplicate values are not allowed. If the value is already in the tree,
        the method should not change the tree.

        O(log N) runtime complexity.

        Parameters:
        - value: The value to be added to the tree.

        Returns:
        - None
        """

        # Insert the new value using the standard BST insertion algorithm.
        new_node = AVLNode(value)
        new_node.parent = None

        if self._root is None:
            # If the tree is empty, the new node becomes the root.
            self._root = new_node
        else:
            # Find the parent node of the new node.
            parent, current = None, self._root

            while current:
                parent = current

                if value < current.value:
                    current = current.left
                else:
                    current = current.right

            # Insert the new node as the child of the parent.
            if value < parent.value:
                parent.left = new_node
            else:
                parent.right = new_node

            # Update heights of ancestors of the new node.
            while parent:
                parent.height += 1
                parent = parent.parent

            # Check for and fix any AVL property violations
            self._balance_insert(new_node)

    def _balance_insert(self, node: AVLNode) -> None:
        """
        Balance the tree after inserting a new node.

        Parameters:
        - node: The node to start balancing from.

        Returns:
        - None
        """

        while node:
            balance_factor = self._get_balance_factor(node)

            # Left-left case
            if balance_factor > 1 and node.left.value > node.right.value:
                self._rotate_right(node)
            # Right-right case
            elif balance_factor < -1 and node.right.value < node.left.value:
                self._rotate_left(node)
            # Left-right case
            elif balance_factor > 1 and node.left.value < node.right.value:
                self._rotate_left(node.left)
                self._rotate_right(node)
            # Right-left case
            elif balance_factor < -1 and node.right.value > node.left.value:
                self._rotate_right(node.right)
                self._rotate_left(node)

            node = node.parent

    def _rotate_left(self, node: AVLNode):
        """
        Perform a left rotation on the given node.

        Parameters:
        - node: The node to rotate left.

        Returns:
        - None
        """

        right_child = node.right
        right_child_left = right_child.left

        # Update parent links
        if node.parent:
            if node == node.parent.left:
                node.parent.left = right_child
            else:
                node.parent.right = right_child
        else:
            self._root = right_child

        right_child.parent = node.parent
        node.parent = right_child

        # Update child links
        right_child.left = node
        node.right = right_child_left

        if right_child_left:
            right_child_left.parent = node

        # Update heights
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        right_child.height = max(self._get_height(right_child.left), node.value) + 1

    def _rotate_right(self, node: AVLNode):
        """
        Perform a right rotation on the given node.

        Parameters:
        - node: The node to rotate right.

        Returns:
        - None
        """

        left_child = node.left
        left_child_right = left_child.right

        # Update parent links
        if node.parent:
            if node == node.parent.left:
                node.parent.left = left_child
            else:
                node.parent.right = left_child
        else:
            self._root = left_child

        left_child.parent = node.parent
        node.parent = left_child

        # Update child links
        left_child.right = node
        node.left = left_child_right

        if left_child_right:
            left_child_right.parent = node

        # Update heights
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        left_child.height = max(self._get_height(left_child.right), node.value) + 1

    def _get_height(self, node: AVLNode) -> int:
        """
        Calculate the height of the subtree rooted at the given node.

        Parameters:
        - node: The node for which to calculate the height.

        Returns:
        - int: The height of the subtree rooted at the given node.
        """

        if node is None:
            return -1
        else:
            return node.height

    def _get_balance_factor(self, node: AVLNode) -> int:
        """
        Calculate the balance factor of the given node.

        Parameters:
        - node: The node for which to calculate the balance factor.

        Returns:
        - int: The balance factor of the given node.
        """

        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        return left_height - right_height



