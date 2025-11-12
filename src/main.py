import os
import shutil
from src import node_helper


def generate_public():
    public = "./public"
    if os.path.exists(public):
        print("PATH EXISTS... removing")
        shutil.rmtree(public)
    copy_static("./static", "./public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        from_file_content = from_file.read()
    with open(template_path, "r") as template_file:
        template_file_content = template_file.read()
    html_node = node_helper.markdown_to_html_node(from_file_content)
    print("PASSED MD > HTML node")
    html_string = html_node.to_html()
    print(f"HTMLSTR: {html_string}")
    page_title = extract_title(from_file_content)
    print(f"PAGE TITLE: {page_title}")
    template_file_content = (
        template_file_content.replace("{{ Title }}", page_title)
    ).replace("{{ Content }}", html_string)
    print(template_file_content)
    with open(f"{dest_path}", "w") as main_html_page:
        main_html_page.write(template_file_content)


def copy_static(path, destination):
    print(f"CURRENT PATH: {path}")
    print(f"CURRENT DESTINATION: {destination}")
    if os.path.exists(path):
        print(f"ON PATH: {path}")
        static_contents = os.listdir(path)
        print(static_contents)
    for item in static_contents:
        if str(item).startswith("."):
            continue
        new_path = os.path.join(path, item)
        new_destination = os.path.join(destination, item)
        print(f"NEW DESTINATION: {new_destination}")
        if os.path.isdir(new_path):
            os.makedirs(f"{new_destination}")
            copy_static(new_path, new_destination)
        if os.path.isfile(new_path):
            os.makedirs(os.path.dirname(new_destination), exist_ok=True)
            shutil.copy(new_path, new_destination)


def extract_title(markdown):
    lines = str(markdown).splitlines()
    for line in lines:
        if line.find("# ") == 0:
            line = (line.replace("#", "")).strip()
            return line
    raise Exception


def get_file_paths(base_path):
    paths = []
    content_folder = os.listdir(base_path)
    for item in content_folder:
        new_path = os.path.join(base_path, item)
        if os.path.isdir(new_path):
            result = get_file_paths(new_path)
            paths.extend(result)
    if os.path.isfile(new_path):
        paths.append(new_path)
    return paths


def main():
    generate_public()
    file_paths = get_file_paths("content")
    print(file_paths)
    for path in file_paths:
        left, right = str(path).split("/", 1)
        public_path = (os.path.join("public", right)).replace(".md", ".html")
        print(public_path)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        generate_page(path, "./template.html", public_path)


if __name__ == "__main__":
    main()
