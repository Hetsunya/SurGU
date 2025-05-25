import pytest
from test_data import *
from bst import BST, generate_trees
from tree_node import TreeNode
from tree_visualizer import *

# Тест инициализации пустого BST
@pytest.mark.bst
def test_tree_init_empty():
    t1 = BST()
    assert isinstance(t1, BST)
    assert t1.root is None
    t2 = BST(None)
    assert isinstance(t2, BST)
    assert t2.root is None

# Тест инициализации BST с одним узлом
@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_tree_init_nonempty(value):
    t = BST(value)
    assert isinstance(t, BST)
    assert isinstance(t.root, TreeNode)
    assert t.root.value == value
    assert t.root.left is None
    assert t.root.right is None

# Тест длины пустого дерева
@pytest.mark.bst
def test_tree_len_empty():
    t = BST()
    assert len(t) == 0

# Проверяет, является ли дерево BST
def is_bst(node, lower=float('-inf'), upper=float('inf')):
    if not node:
        return True
    val = node.value
    if val <= lower or val >= upper:
        return False
    if not is_bst(node.right, val, upper):
        return False
    if not is_bst(node.left, lower, val):
        return False
    return True

# Проверяет уникальность деревьев
def are_all_trees_unique(trees):
    seen = set()
    for tree in trees:
        structure = serialize_tree(tree)
        if structure in seen:
            return False
        seen.add(structure)
    return True

# Сериализует дерево в строку
def serialize_tree(node):
    if not node:
        return "None"
    return f"{node.value}({serialize_tree(node.left)},{serialize_tree(node.right)})"

# Тест генерации деревьев
@pytest.mark.parametrize("n, expected_count", [
    (0, 1), (1, 1), (2, 2), (3, 5), (4, 14), (5, 42)
])
def test_generate_trees(n, expected_count):
    trees = generate_trees(n)
    assert len(trees) == expected_count, f"Ожидалось {expected_count} деревьев для n={n}, получено {len(trees)}"
    assert all(is_bst(tree) for tree in trees), "Все деревья должны быть валидными BST"
    assert are_all_trees_unique(trees), "Все деревья должны быть структурно уникальными"