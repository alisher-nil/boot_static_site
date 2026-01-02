import os
import shutil

from src.constants import CONTENT_DIR, PUBLIC_DIR, STATIC_DIR
from src.convert import markdown_to_html_node
from src.markdown import extract_title


def main():
    reset_public_directory()
    generate_pages()


def generate_pages():
    files = find_files_with_extension(CONTENT_DIR, ".md")
    for file_path in files:
        dirname = os.path.dirname(file_path)
        relative_dir = (
            os.path.relpath(dirname, CONTENT_DIR) if dirname != CONTENT_DIR else ""
        )
        dest_dir = os.path.join(PUBLIC_DIR, relative_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        dest_path = os.path.join(dest_dir, f"{filename}.html")
        generate_page(file_path, "template.html", dest_path)


def find_files_with_extension(directory: str, extension: str) -> list[str]:
    """Find all files with given extension in directory and subdirectories."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace(r"{{ Title }}", title)
    template_content = template_content.replace(r"{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(template_content)
    pass  # Implementation of page generation goes here


def reset_public_directory():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.mkdir(PUBLIC_DIR)
    copy_files(STATIC_DIR, PUBLIC_DIR)


def copy_files(src, dst):
    for item in os.listdir(src):
        if os.path.isfile(os.path.join(src, item)):
            shutil.copy(os.path.join(src, item), dst)
        else:
            os.mkdir(os.path.join(dst, item))
            copy_files(os.path.join(src, item), os.path.join(dst, item))


if __name__ == "__main__":
    main()
