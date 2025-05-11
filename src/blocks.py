import re
from sys import flags
from webbrowser import get
from textnode import MDTextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import split_markdown

from enum import Flag, auto

class BlockType(Flag):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def markdown_to_html(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_node = ParentNode("div", list(), None)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            process_heading(block, html_node)
            continue
        elif block_type == BlockType.PARAGRAPH:
            process_paragraph(block, html_node)
        block_text = get_block_text(block, block_type)
        
    return html_node
        
        

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    This finction gets a string and splits it into 'blocks'
    Each block is separated by at least 2 newlines
    The output of the function is a list of said 'blocks' i.e strings
    """
    result = re.split(r"\n{2,}", markdown)
    for i in range(len(result)):
        result[i] = result[i].strip()
        result[i] = result[i].strip('\n')
    return result

def block_to_block_type(block: str) -> BlockType:
    """
    This function checks the format of the input string and returns a type of it 
    """
    if re.match(r'#{1,6} ', block) and len(block.splitlines()) == 1:
        return BlockType.HEADING
    elif len(re.findall(r'^(```)|(```)$', block, flags=re.MULTILINE)) == 2:
        return BlockType.CODE
    elif re.fullmatch(r'(> (?:.+)\n?)+', block):
        return BlockType.QUOTE
    elif re.fullmatch(r'(- (?:.+)\n?)+', block):
        return BlockType.UNORDERED_LIST
    elif re.fullmatch(r'(\d+\. (?:.+)\n?)+', block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def get_block_text(block: str, block_type: BlockType) -> list[str]:
    result = list()
    match block_type:
        case BlockType.PARAGRAPH:
            result.append(block)
        case BlockType.QUOTE:
            lines = block.splitlines()
            for line in lines:
                result.append(line[2:])
        case BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            for line in lines:
                result.append(line[2:])
        case BlockType.ORDERED_LIST:
            lines = block.splitlines()
            for line in lines:
                result.append(re.match(r"([^\d+. ])(.*)", line))
        case BlockType.CODE:
            result.append(block.strip("```"))
    return result


def get_heading_text(text: str) -> str:
    if text[0] != "#" and text[0] != " ":
        return text
    return get_heading_text(text[1:])

def count_heading_hashes(text:str) -> int:
    if text[0] == "#":
        return count_heading_hashes(text[1:]) + 1
    return 0

def process_heading(block: str, parent_html: HTMLNode) -> None:
    heading_count = count_heading_hashes(block)
    html_tag = f"h{heading_count}"
    html_heading = ParentNode(html_tag, list(), None)
    parent_html.children.append(html_heading)
    heading_nodes = split_markdown(get_heading_text(block))
    for node in heading_nodes:
        html_heading.children.append(node.text_node_to_html_node())

def process_paragraph(block: str, parent_html: HTMLNode) -> None:
    html_paragraph = ParentNode("p", list(), None)
    parent_html.children.append(html_paragraph)
    paragraph_nodes = split_markdown(block)
    for node in paragraph_nodes:
        html_paragraph.children.append(node.text_node_to_html_node())