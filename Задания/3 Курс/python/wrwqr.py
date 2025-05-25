def removeDuplicateFolders(paths):
    def dfs(node):
        # Serialize the current folder structure as a string
        serialized = []
        for child in node:
            serialized.append(child)
            serialized.extend(dfs(node[child]))
        serialized_str = ",".join(serialized)

        # Check if we have seen this folder structure before
        if serialized_str in seen:
            seen[serialized_str] += 1
        else:
            seen[serialized_str] = 1

        # If this structure was marked for deletion, return an empty dictionary
        if seen[serialized_str] > 1:
            return {}

        return {serialized_str: node}

    # Initialize the root folder as an empty dictionary
    root = {}
    seen = {}

    # Build the folder structure from the paths
    for path in paths:
        node = root
        for folder in path:
            node = node.setdefault(folder, {})

    # Perform depth-first search to identify duplicate folders
    dfs(root)

    # Extract remaining folder paths
    def extract_paths(node, current_path):
        paths = []
        for folder in node:
            new_path = current_path + [folder]
            child_paths = extract_paths(node[folder], new_path)
            if child_paths:
                paths.extend(child_paths)
            elif tuple(current_path) not in marked_for_deletion:
                paths.append(current_path)
        return paths

    marked_for_deletion = set()
    result = []
    for folder in root:
        result.extend(extract_paths(root[folder], [folder]))

    return result


# Example 1
paths1 = [["a"], ["c"], ["d"], ["a", "b"], ["c", "b"], ["d", "a"]]
print(removeDuplicateFolders(paths1))  # Output: [["a","b"],["c","b"],["d","a"]]
