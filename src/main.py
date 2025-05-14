from genericpath import isdir
import os
import shutil

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

def main():
    copy_contents()

main()