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
        Add a new value to the AVL tree.

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
            self._add_recursive(self._root, value)

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

        # Rebalance the tree after insertion.
        self._rebalance(node)

        return node

    def remove(self, value: object) -> bool:
        """
        Remove a value from the AVL tree. Returns True if the value is removed,
        otherwise returns False.

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
            # Case 2: Node has two children, use the BST method to handle it.
            self._remove_node_with_two_children(parent, current)
        else:
            # Case 3: Node has one child, replace it with the child.
            self._remove_node_with_one_child(parent, current)

        # Rebalance the tree starting from the parent.
        if parent is not None:
            self._rebalance(parent)

        return True

    def _remove_leaf(self, parent: AVLNode, node: AVLNode) -> None:
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

    def _remove_node_with_one_child(self, parent: AVLNode, node: AVLNode) -> None:
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

    def _remove_node_with_two_children(self, parent: AVLNode, node: AVLNode) -> None:
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

        # Rebalance the tree starting from the parent of the removed inorder successor.
        self._rebalance(successor_parent)

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate the balance factor of a given node.

        Parameters:
        - node: The AVL node.

        Returns:
        - int: The balance factor (height of left subtree - height of right subtree).
        """
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return left_height - right_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Get the height of a given node.

        Parameters:
        - node: The AVL node.

        Returns:
        - int: The height of the node.
        """
        return node.height if node else -1

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Perform a left rotation on a given node.

        Parameters:
        - node: The AVL node.

        Returns:
        - AVLNode: The new root of the subtree after the rotation.
        """
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.left = node
        node.parent = new_root

        # Update heights
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Perform a right rotation on a given node.

        Parameters:
        - node: The AVL node.

        Returns:
        - AVLNode: The new root of the subtree after the rotation.
        """
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.right = node
        node.parent = new_root

        # Update heights
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of a given node.

        Parameters:
        - node: The AVL node.

        Returns:
        - None
        """
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalance the AVL tree starting from the given node.

        Parameters:
        - node: The node to start the rebalancing process.

        Returns:
        - None
        """
        while node is not None:
            # Update the height of the current node.
            self._update_height(node)

            # Check the balance factor to determine the rotation needed.
            balance_factor = self._balance_factor(node)

            # Left heavy
            if balance_factor > 1:
                if self._balance_factor(node.left) < 0:
                    # Left-Right case (LR): Perform left rotation on left child,
                    # then right rotation on current node.
                    node.left = self._rotate_left(node.left)
                # Perform right rotation on current node.
                node = self._rotate_right(node)
            # Right heavy
            elif balance_factor < -1:
                if self._balance_factor(node.right) > 0:
                    # Right-Left case (RL): Perform right rotation on right child,
                    # then left rotation on current node.
                    node.right = self._rotate_right(node.right)
                # Perform left rotation on current node.
                node = self._rotate_left(node)

            # Move up the tree towards the root.
            node = node.parent