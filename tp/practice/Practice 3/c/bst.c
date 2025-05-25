#include "bst.h"

// Рекурсивно выводит узлы в DOT-файл для визуализации
static void output_nodes_to_dotfile(tree_node_t *node, FILE *file, print_datatype_func print_data) {
    if (!node) return;
    fprintf(file, "%zu [label=<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\"><TR>\n", (size_t)node);
    if (node->left) fprintf(file, "<TD port=\"left\"><SUB><i>l</i></SUB></TD>\n");
    fprintf(file, "<TD CELLPADDING=\"7\"><b>");
    print_data(file, node->data);
    fprintf(file, "</b></TD>\n");
    if (node->right) fprintf(file, "<TD port=\"right\"><SUB><i>r</i></SUB></TD>\n");
    fprintf(file, "</TR></TABLE>>]\n");
    if (node->left) fprintf(file, "%zu:left -> %zu\n", (size_t)node, (size_t)node->left);
    if (node->right) fprintf(file, "%zu:right -> %zu\n", (size_t)node, (size_t)node->right);
    output_nodes_to_dotfile(node->left, file, print_data);
    output_nodes_to_dotfile(node->right, file, print_data);
}

// Создает PNG-изображение дерева
void bst_render(bst_t *bst, print_datatype_func print_data, bool open) {
    struct stat st = {0};
    const char *pics_folder = "./pics";
    if (stat(pics_folder, &st) == -1)
        if (mkdir(pics_folder, 0777) == -1) {
            printf("Ошибка: не удалось создать папку '%s'\n", pics_folder);
            exit(EXIT_FAILURE);
        }

    char *filename = calloc(64, 1);
    sprintf(filename, "%s/bst_%zu", pics_folder, (size_t)bst);
    FILE *file = fopen(filename, "w");
    if (!file) {
        printf("Ошибка: не удалось открыть файл '%s'\n", filename);
        free(filename);
        exit(EXIT_FAILURE);
    }
    fprintf(file, "digraph bst_%zu {\nnode [shape=ellipse]\n", (size_t)bst);
    output_nodes_to_dotfile(bst->root, file, print_data);
    fprintf(file, "}\n");
    fclose(file);
    char *command = calloc(64, 1);
    sprintf(command, "dot -Tpng %s -o %s.png", filename, filename);
    system(command);
    remove(filename);
    free(command);
    if (open) {
        command = calloc(64, 1);
        sprintf(command, "xdg-open %s.png", filename);
        system(command);
        free(command);
    }
    free(filename);
}

// Создает новое дерево
bst_t *bst_create(size_t data_size) {
    bst_t *tree = malloc(sizeof(bst_t));
    if (!tree) return NULL;
    tree->root = NULL;
    tree->data_size = data_size;
    return tree;
}

// Проверяет, пустое ли дерево
bool bst_empty(bst_t *tree) {
    return tree->root == NULL;
}

// Проверяет наличие данных в дереве
bool bst_contains(bst_t *tree, void *data, comparator_func comp) {
    tree_node_t *current = tree->root;
    while (current) {
        int compare_result = comp(data, current->data);
        if (compare_result < 0) current = current->left;
        else if (compare_result > 0) current = current->right;
        else return true;
    }
    return false;
}

// Подсчитывает узлы рекурсивно
static size_t count_nodes(tree_node_t *node) {
    if (!node) return 0;
    return 1 + count_nodes(node->left) + count_nodes(node->right);
}

// Возвращает количество узлов
size_t bst_length(bst_t *tree) {
    return count_nodes(tree->root);
}

// Рекурсивно вставляет узел
static tree_node_t *insert_node_recursive(tree_node_t *node, void *data, size_t data_size, comparator_func comp) {
    if (!node) {
        tree_node_t *new_node = malloc(sizeof(tree_node_t));
        new_node->data = malloc(data_size);
        memcpy(new_node->data, data, data_size);
        new_node->left = NULL;
        new_node->right = NULL;
        return new_node;
    }
    if (comp(data, node->data) < 0)
        node->left = insert_node_recursive(node->left, data, data_size, comp);
    else
        node->right = insert_node_recursive(node->right, data, data_size, comp);
    return node;
}

// Вставляет узел в дерево
void bst_insert_node(bst_t *tree, void *data, comparator_func comp) {
    tree->root = insert_node_recursive(tree->root, data, tree->data_size, comp);
}

// Находит узел с минимальным значением
static tree_node_t *find_min(tree_node_t *node) {
    tree_node_t *current = node;
    while (current && current->left) current = current->left;
    return current;
}

// Рекурсивно удаляет узел
static tree_node_t *delete_node_recursive(tree_node_t *node, void *data, size_t data_size, comparator_func comp) {
    if (!node) return NULL;
    int compare_result = comp(data, node->data);
    if (compare_result < 0)
        node->left = delete_node_recursive(node->left, data, data_size, comp);
    else if (compare_result > 0)
        node->right = delete_node_recursive(node->right, data, data_size, comp);
    else {
        if (!node->left) {
            tree_node_t *temp = node->right;
            free(node->data);
            free(node);
            return temp;
        } else if (!node->right) {
            tree_node_t *temp = node->left;
            free(node->data);
            free(node);
            return temp;
        }
        tree_node_t *temp = find_min(node->right);
        memcpy(node->data, temp->data, data_size);
        node->right = delete_node_recursive(node->right, temp->data, data_size, comp);
    }
    return node;
}

// Удаляет узел из дерева
void bst_delete_node(bst_t *tree, void *data, comparator_func comp) {
    tree->root = delete_node_recursive(tree->root, data, tree->data_size, comp);
}

// Прямой обход рекурсивно
static void preorder_traversal(tree_node_t *node, int *array, int *index) {
    if (!node) return;
    array[(*index)++] = *(int *)node->data;
    preorder_traversal(node->left, array, index);
    preorder_traversal(node->right, array, index);
}

// Прямой обход дерева
void *bst_preorder_traversal(bst_t *tree) {
    if (!tree || !tree->root) return NULL;
    size_t num_nodes = bst_length(tree);
    if (!num_nodes) return NULL;
    int *result = malloc(num_nodes * sizeof(int));
    if (!result) return NULL;
    int index = 0;
    preorder_traversal(tree->root, result, &index);
    return result;
}

// Центрированный обход рекурсивно
static void inorder_traversal(tree_node_t *node, int *array, int *index) {
    if (!node) return;
    inorder_traversal(node->left, array, index);
    array[(*index)++] = *(int *)node->data;
    inorder_traversal(node->right, array, index);
}

// Центрированный обход дерева
void *bst_inorder_traversal(bst_t *tree) {
    if (!tree || !tree->root) return NULL;
    size_t num_nodes = bst_length(tree);
    if (!num_nodes) return NULL;
    int *result = malloc(num_nodes * sizeof(int));
    if (!result) return NULL;
    int index = 0;
    inorder_traversal(tree->root, result, &index);
    return result;
}

// Обратный обход рекурсивно
static void postorder_traversal(tree_node_t *node, int *array, int *index) {
    if (!node) return;
    postorder_traversal(node->left, array, index);
    postorder_traversal(node->right, array, index);
    array[(*index)++] = *(int *)node->data;
}

// Обратный обход дерева
void *bst_postorder_traversal(bst_t *tree) {
    if (!tree || !tree->root) return NULL;
    size_t num_nodes = bst_length(tree);
    if (!num_nodes) return NULL;
    int *result = malloc(num_nodes * sizeof(int));
    if (!result) return NULL;
    int index = 0;
    postorder_traversal(tree->root, result, &index);
    return result;
}

// Вычисляет высоту дерева
static int tree_height(tree_node_t *node) {
    if (!node) return 0;
    int leftHeight = tree_height(node->left);
    int rightHeight = tree_height(node->right);
    return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
}

// Собирает данные узлов на заданном уровне
static void collect_level_data(tree_node_t *node, int level, void *array, int *index, size_t data_size) {
    if (!node) return;
    if (level == 0) {
        memcpy((char *)array + (size_t)(*index) * data_size, node->data, data_size);
        (*index)++;
    } else {
        collect_level_data(node->left, level - 1, array, index, data_size);
        collect_level_data(node->right, level - 1, array, index, data_size);
    }
}

// Поуровневый обход дерева
void *bst_level_order_traversal(bst_t *tree) {
    if (!tree || !tree->root) return NULL;
    int height = tree_height(tree->root);
    size_t total_nodes = bst_length(tree);
    void *results = malloc(total_nodes * tree->data_size);
    if (!results) return NULL;
    int index = 0;
    for (int i = 0; i < height; i++)
        collect_level_data(tree->root, i, results, &index, tree->data_size);
    return results;
}

// Вставляет массив в дерево
void bst_insert_array(bst_t *tree, size_t size, void *a, comparator_func cmp) {
    char *array = (char *)a;
    for (size_t i = 0; i < size; i++)
        bst_insert_node(tree, array + i * tree->data_size, cmp);
}

// Печатает узел рекурсивно
static void print_node(FILE *f, tree_node_t *node) {
    if (!node) {
        fprintf(f, "()");
        return;
    }
    fprintf(f, "(%d", *((int*)node->data));
    if (node->left || node->right) {
        if (node->left) {
            fprintf(f, ", l -> ");
            print_node(f, node->left);
        }
        if (node->right) {
            fprintf(f, ", r -> ");
            print_node(f, node->right);
        }
    }
    fprintf(f, ")");
}

// Печатает дерево
void bst_print_int(bst_t *tree, FILE *f) {
    if (!tree || !tree->root) fprintf(f, "()");
    else print_node(f, tree->root);
}

// Рекурсивно освобождает узлы
static void destroy_nodes(tree_node_t *node) {
    if (!node) return;
    destroy_nodes(node->left);
    destroy_nodes(node->right);
    free(node->data);
    free(node);
}

// Уничтожает дерево
void bst_destroy(bst_t *tree) {
    if (tree) {
        destroy_nodes(tree->root);
        free(tree);
    }
}