import re
from textnode import MDTextType, TextNode

DELIMETERS = {
    '**': MDTextType.BOLD_TEXT,
    '_': MDTextType.ITALIC_TEXT,
    '`': MDTextType.CODE_TEXT,
    '': MDTextType.NORMAL_TEXT
}

def get_node(text: str, type: MDTextType, url=None):
    return TextNode(text, type, url)

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
            if old_node_text_splitted[i] != '':
                if i % 2 == 0:
                    new_node.append(get_node(old_node_text_splitted[i], DELIMETERS[current_delimiter]))
                else:
                    new_node.append(get_node(old_node_text_splitted[i], text_type))
    
    return new_node

def extract_md_images(text):
    images = re.findall(r"\!\[([^\[\]]*)\]\((https?:\/\/\w+(?:.\w+)+\/\w+.\w+)\)|!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_md_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\((https?:\/\/\w+(?:.\w+)+(?:))\/{0,1}\)|(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_link(*old_nodes: TextNode):
    new_node = list()

    for old_node in old_nodes:
        if old_node.text_type != MDTextType.NORMAL_TEXT:
            new_node.append(old_node)
            continue
        
        links = extract_md_links(old_node.text)

        old_node_text_splitted = [old_node.text]
        for link in links:
            link_list = [link[0], link[1]]
            if link[2] and link[3]:
                link_list = [link[2], link[3]]
            separator = f"[{link_list[0]}]({link_list[1]})"
            last = old_node_text_splitted.pop()
            old_node_text_splitted = old_node_text_splitted + last.split(separator, maxsplit=2)
        
        if old_node_text_splitted[0] != "":
            new_node.append(get_node(old_node_text_splitted[0], MDTextType.NORMAL_TEXT))
        for i in range(len(old_node_text_splitted) - 1):
            link_list = [links[i][0], links[i][1]]
            if links[i][2] and links[i][3]:
                link_list = [links[i][2], links[i][3]]
            new_node.append(get_node(link_list[0], MDTextType.LINK, link_list[1]))
            if old_node_text_splitted[i + 1] != "":
                new_node.append(get_node(old_node_text_splitted[i + 1], MDTextType.NORMAL_TEXT))
    
    return new_node

def split_nodes_image(*old_nodes: TextNode):
    new_node = list()

    for old_node in old_nodes:
        if old_node.text_type != MDTextType.NORMAL_TEXT:
            new_node.append(old_node)
            continue
        
        images = extract_md_images(old_node.text)

        old_node_text_splitted = [old_node.text]
        for image in images:
            image_list = [image[0], image[1]]
            if image[2] and image[3]:
                image_list = [image[2], image[3]]
            separator = f"![{image_list[0]}]({image_list[1]})"
            last = old_node_text_splitted.pop()
            old_node_text_splitted = old_node_text_splitted + last.split(separator, maxsplit=2)
        
        if old_node_text_splitted[0] != "":
            new_node.append(get_node(old_node_text_splitted[0], MDTextType.NORMAL_TEXT))
        for i in range(len(old_node_text_splitted) - 1):
            image_list = [images[i][0], images[i][1]]
            if images[i][2] and images[i][3]:
                image_list = [images[i][2], images[i][3]]
            new_node.append(get_node(image_list[0], MDTextType.IMAGE, image_list[1]))
            if old_node_text_splitted[i + 1] != "":
                new_node.append(get_node(old_node_text_splitted[i + 1], MDTextType.NORMAL_TEXT))
    
    return new_node

def split_markdown(text: str) -> list[TextNode]:
    nodes = [get_node(text, MDTextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(*nodes, delimiter='`', text_type=MDTextType.CODE_TEXT)
    nodes = split_nodes_image(*nodes)
    nodes = split_nodes_link(*nodes)
    nodes = split_nodes_delimiter(*nodes, delimiter="**", text_type=MDTextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(*nodes, delimiter="_", text_type=MDTextType.ITALIC_TEXT)
    return nodes
