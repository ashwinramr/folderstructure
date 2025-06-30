import streamlit as st
import re

st.set_page_config(page_title="Markdown Folder Tree Generator", layout="centered")

st.title("📁 Markdown Folder Structure Generator with Visual Preview")
st.write(
    "Enter your folder hierarchy manually and see it as a markdown tree and interactive visual tree."
)

# --- Folder structure input ---
st.subheader("Enter folder structure")
root_folder = st.text_input("Root folder name", value="project-root")

folder_list = st.text_area(
    "Subfolders & files (one per line, indent with spaces/tabs for hierarchy)",
    value="data/\n  raw/\n  processed/\nnotebooks/\nsrc/\n  utils/\n  main.py",
    height=200
)

if st.button("Generate Trees"):
    # --- Build Markdown tree ---
    def build_markdown_tree(lines, indent_size=2):
        markdown_lines = [f"{root_folder}/"]
        for line in lines:
            stripped = line.lstrip()
            indent_level = (len(line) - len(stripped)) // indent_size
            prefix = "│   " * indent_level + "├── " + stripped
            markdown_lines.append(prefix)
        return "\n".join(markdown_lines)

    lines = folder_list.strip().split("\n")
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

    # --- Visual interactive tree ---
    st.subheader("🌳 Interactive Folder Tree")
    try:
        from streamlit_tree import tree

        def render_tree(node):
            with tree(node["name"]):
                for child in node["children"]:
                    render_tree(child)

        render_tree(tree_data)
    except ModuleNotFoundError:
        st.warning(
            "To view the interactive folder tree, install the streamlit-tree component:\n\n"
            "```bash\npip install streamlit-tree\n```"
        )
        st.info("Fallback: interactive tree not shown because streamlit-tree is missing.")
    