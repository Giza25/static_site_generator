import os
import shutil
import re

from blocks import markdown_to_html

def copy_contents(path: str = ""):
    source_path = f"./static/{path}"
    target_path = f"./public/{path}"
    if os.path.exists(target_path) and os.path.isdir(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    content_list = os.listdir(source_path)
    for content in content_list:
        if os.path.isdir(os.path.join(source_path, content)):
            copy_contents(os.path.join(path, content))
        else:
            shutil.copy(os.path.join(source_path, content), os.path.join(target_path, content))

def extract_title(text: str):
    text = text.lstrip()
    if not re.match(r"^# ", text):
        raise Exception("No titles were found")
    title = text.splitlines()[0].rstrip().lstrip("# ")
    return title

def generate_page(from_path: str, dest_path: str, template_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file, open(template_path) as template_file, open(dest_path, "w") as destination_file:
        md = md_file.read()
        template_html = template_file.read()
        title = extract_title(md)
        contents_nodes = markdown_to_html(md)
        contents_html = contents_nodes.to_html()
        template_html = template_html.replace('{{ Title }}', title)
        template_html = template_html.replace('{{ Content }}', contents_html)
        destination_file.write(template_html)

def main():
    copy_contents()
    generate_page("./content/index.md", "./public/index.html", "./template.html")

main()