import os
import shutil
import re
import sys

from blocks import markdown_to_html

def copy_contents(target: str = "public", path: str = ""):
    source_path = f"./static/{path}"
    target_path = f"./{target}/{path}"
    if os.path.exists(target_path) and os.path.isdir(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    content_list = os.listdir(source_path)
    for content in content_list:
        if os.path.isdir(os.path.join(source_path, content)):
            copy_contents(path=os.path.join(path, content))
        else:
            shutil.copy(os.path.join(source_path, content), os.path.join(target_path, content))

def extract_title(text: str):
    text = text.lstrip()
    if not re.match(r"^# ", text):
        raise Exception("No titles were found")
    title = text.splitlines()[0].rstrip().lstrip("# ")
    return title

def generate_page_recursively(dir_path_content: str, dir_path_destination: str, template_path: str, base_path: str):
    contents = os.listdir(dir_path_content)
    for content in contents:
        if os.path.isfile(os.path.join(dir_path_content, content)):
            content_name = os.path.splitext(content)
            generate_page(os.path.join(dir_path_content, content), os.path.join(dir_path_destination, content_name[0] + ".html"), template_path, base_path)
        else:
            os.mkdir(os.path.join(dir_path_destination, content))
            generate_page_recursively(os.path.join(dir_path_content, content), os.path.join(dir_path_destination, content), template_path, base_path)

def generate_page(from_path: str, dest_path: str, template_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file, open(template_path) as template_file, open(dest_path, "w") as destination_file:
        md = md_file.read()
        template_html = template_file.read()
        title = extract_title(md)
        contents_nodes = markdown_to_html(md)
        contents_html = contents_nodes.to_html()
        template_html = template_html.replace('{{ Title }}', title)
        template_html = template_html.replace('{{ Content }}', contents_html)
        template_html = template_html.replace('href=\"/', f"href=\"{base_path}")
        template_html = template_html.replace('src=\"/', f"src=\"{base_path}")
        destination_file.write(template_html)

def main():
    base_path = "/"
    content_path = "./content"
    destination_path = "./public"
    template_file_path = "./template.html"
    if len(sys.argv) > 1: 
        base_path = sys.argv[1]
        destination_path = "./docs"
        copy_contents("docs")
    else:
        copy_contents()
    generate_page_recursively(content_path, destination_path, template_file_path, base_path)

main()