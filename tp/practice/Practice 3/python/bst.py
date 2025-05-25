from tree_visualizer import TreeVisualizer
from tree_node import TreeNode

class BST:
    # Визуализирует дерево через TreeVisualizer
    def visualize(self):
        TreeVisualizer.visualize(self.root)
    
    # Создает BST, корень None или узел с заданным значением
    def __init__(self, value=None):
        self.root = None if value is None else TreeNode(value)
        self.size = 0 if value is None else 1
    
    # Возвращает строковое представление дерева
    def __str__(self):
        return "None" if self.root is None else str(self.root)

    # Вставляет значение в дерево
    def insert_node(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            self.size += 1
            return
        self._insert_recursive(self.root, value)
        self.size += 1

    # Рекурсивно вставляет значение
    def _insert_recursive(self, current, value):
        if current is None:
            return TreeNode(value)
        if value == current.value:
            current.count += 1
            return current
        if value < current.value:
            current.left = self._insert_recursive(current.left, value)
        else:
            current.right = self._insert_recursive(current.right, value)
        return current

    # Удаляет узел с заданным значением
    def delete_node(self, value):
        if self.root is None:
            raise ValueError("Tree is empty")
        self.root = self._delete_recursive(self.root, value)

    # Рекурсивно удаляет узел
    def _delete_recursive(self, node, value):
        if node is None:
            raise ValueError("Value not found in the tree")
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                self.size -= 1
                return node.right
            if node.right is None:
                self.size -= 1
                return node.left
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
        return node

    # Находит узел с минимальным значением
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # Проверяет наличие значения в дереве
    def __contains__(self, value):
        current = self.root
        while current:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

    # Возвращает количество узлов
    def __len__(self):
        return self.size

    # Очищает дерево
    def clear(self):
        self.root = None
        self.size = 0

    # Создает копию дерева
    def copy(self):
        new_tree = BST()
        self._copy_recursive(self.root, new_tree)
        return new_tree

    # Рекурсивно копирует узлы
    def _copy_recursive(self, node, tree):
        if node:
            tree.insert_node(node.value)
            self._copy_recursive(node.left, tree)
            self._copy_recursive(node.right, tree)

    # Подсчитывает узлы с заданным значением
    def count(self, value):
        return self._count_recursive(self.root, value)
    
    # Рекурсивно подсчитывает узлы
    def _count_recursive(self, current, value):
        if current is None:
            return 0
        if value == current.value:
            return current.count
        return self._count_recursive(current.left if value < current.value else current.right, value)
    
    # Строковое представление для отладки
    def __repr__(self):
        return str(self)
    
    # Сравнивает два дерева на равенство
    def __eq__(self, other):
        if not isinstance(other, BST):
            return False
        return self._trees_are_equal(self.root, other.root)

    # Рекурсивно сравнивает деревья
    def _trees_are_equal(self, node1, node2):
        if node1 is None and node2 is None:
            return True
        if node1 and node2:
            return (node1.value == node2.value and
                    self._trees_are_equal(node1.left, node2.left) and
                    self._trees_are_equal(node1.right, node2.right))
        return False

    # Вставляет список значений
    def insert_list(self, values):
        for value in values:
            self.insert_node(value)

    # Рекурсивный прямой обход
    def recursive_preorder_traverse(self):
        return self._preorder_traverse(self.root)
    
    # Вспомогательный метод для прямого обхода
    def _preorder_traverse(self, node):
        if node is None:
            return []
        return [node.value] + self._preorder_traverse(node.left) + self._preorder_traverse(node.right)
    
    # Итеративный прямой обход
    def iterative_preorder_traverse(self):
        if self.root is None:
            return []
        stack, result = [self.root], []
        while stack:
            node = stack.pop()
            if node:
                result.append(node.value)
                stack.append(node.right)
                stack.append(node.left)
        return result
    
    # Рекурсивный центрированный обход
    def recursive_inorder_traverse(self):
        return self._inorder_traverse(self.root)
    
    # Вспомогательный метод для центрированного обхода
    def _inorder_traverse(self, node):
        if node is None:
            return []
        return self._inorder_traverse(node.left) + [node.value] + self._inorder_traverse(node.right)
    
    # Итеративный центрированный обход
    def iterative_inorder_traverse(self):
        result, stack, current = [], [], self.root
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.value)
            current = current.right
        return result
    
    # Рекурсивный обратный обход
    def recursive_postorder_traverse(self):
        return self._postorder_traverse(self.root)
    
    # Вспомогательный метод для обратного обхода
    def _postorder_traverse(self, node):
        if node is None:
            return []
        return self._postorder_traverse(node.left) + self._postorder_traverse(node.right) + [node.value]
    
    # Итеративный обратный обход
    def iterative_postorder_traverse(self):
        if self.root is None:
            return []
        stack, result = [self.root], []
        while stack:
            node = stack.pop()
            if node:
                result.append(node.value)
                stack.append(node.left)
                stack.append(node.right)
        return result[::-1]
    
    # Поуровневый обход
    def level_order_traverse(self):
        if not self.root:
            return []
        queue, result = [self.root], []
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.value)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result

# Генерирует все уникальные BST для n узлов
def generate_trees(n):
    if n == 0:
        return [None]
    return generate_trees_recursive(1, n)

# Рекурсивно генерирует BST
def generate_trees_recursive(start, end):
    if start > end:
        return [None]
    all_trees = []
    for i in range(start, end + 1):
        left_trees = generate_trees_recursive(start, i - 1)
        right_trees = generate_trees_recursive(i + 1, end)
        for l in left_trees:
            for r in right_trees:
                current_tree = TreeNode(i)
                current_tree.left = l
                current_tree.right = r
                all_trees.append(current_tree)
    return all_trees