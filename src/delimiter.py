import re
from textnode import MDTextType, TextNode

DELIMETERS = {
    '**': MDTextType.BOLD_TEXT,
    '_': MDTextType.ITALIC_TEXT,
    '`': MDTextType.CODE_TEXT,
    '': MDTextType.NORMAL_TEXT
}

def get_node(text: str, type: MDTextType):
    return TextNode(text, type)

def split_nodes_delimiter(*old_nodes: TextNode, delimiter, text_type: MDTextType, current_delimiter=''):
    new_node = list()

    for old_node in old_nodes:
        if old_node.text_type != MDTextType.NORMAL_TEXT:
            new_node.append(old_node)
            continue
        
        # Counting amount of delimiters found to check the legitimacy of the text
        delimiter_count = 0
        for char in old_node.text:
            if delimiter == char:
                delimiter_count += 1
        
        if delimiter_count % 2 == 1:
            raise Exception("There is an odd amount of delimiters!")
        
        old_node_text_splitted = old_node.text.split(delimiter)

        # assigning node type to every splitted bit of text
        for i in range(len(old_node_text_splitted)):
            if i % 2 == 0:
                new_node.append(get_node(old_node_text_splitted[i], DELIMETERS[current_delimiter]))
            else:
                new_node.append(get_node(old_node_text_splitted[i], text_type))
    
    return new_node

def extract_md_images(text):
    images = re.findall(r"\!\[(\w+)\]\((https?:\/\/\w+(?:.\w+)+\/\w+.\w+)\)", text)
    return images

def extract_md_links(text):
    links = re.findall(r"(?<!!)\[(\w+)\]\((https?:\/\/\w+(?:.\w+)+(?:))\/{0,1}\)", text)
    return links

