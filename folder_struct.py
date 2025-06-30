import streamlit as st

st.set_page_config(page_title="Markdown Folder Tree Generator", layout="centered")

st.title("📁 Markdown Folder Structure Generator with Interactive Visual Tree")
st.write(
    "Define your folder hierarchy manually, generate a markdown tree, and preview it as an interactive expandable folder tree."
)

# --- Folder structure input ---
st.subheader("Enter Folder Structure")
root_folder = st.text_input("Root folder name", value="project-root")

folder_list = st.text_area(
    "Subfolders & files (one per line, indent with spaces/tabs for hierarchy)",
    value="data/\n  raw/\n  processed/\nnotebooks/\nsrc/\n  utils/\n  main.py",
    height=200
)

if st.button("Generate Trees"):
    # --- Parse folder lines ---
    lines = folder_list.strip().split("\n")

    # --- Generate markdown tree ---
    def build_markdown_tree(lines, indent_size=2):
        markdown_lines = [f"{root_folder}/"]
        for line in lines:
            stripped = line.lstrip()
            indent_level = (len(line) - len(stripped)) // indent_size
            prefix = "│   " * indent_level + "├── " + stripped
            markdown_lines.append(prefix)
        return "\n".join(markdown_lines)

    markdown_tree = build_markdown_tree(lines)

    st.subheader("📄 Generated Markdown Tree")
    st.code(markdown_tree, language="markdown")
    st.download_button(
        "💾 Download Markdown",
        markdown_tree,
        file_name="folder_structure.md",
        mime="text/markdown"
    )

    # --- Build hierarchical dict for interactive tree ---
    def build_tree_dict(lines, indent_size=2):
        root = {"name": root_folder, "children": []}
        stack = [(root, -1)]
        for line in lines:
            stripped = line.lstrip()
            indent_level = (len(line) - len(stripped)) // indent_size
            node = {"name": stripped, "children": []}
            while indent_level <= stack[-1][1]:
                stack.pop()
            stack[-1][0]["children"].append(node)
            stack.append((node, indent_level))
        return root

    tree_data = build_tree_dict(lines)

    # --- Render interactive folder tree with expanders ---
    st.subheader("🌳 Interactive Expandable Folder Tree")

    def render_tree_with_expanders(node):
        with st.expander(node["name"], expanded=True):
            for child in node["children"]:
                render_tree_with_expanders(child)

    render_tree_with_expanders(tree_data)