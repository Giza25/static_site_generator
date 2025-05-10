import re
from textnode import MDTextType, TextNode

from enum import Flag, auto

class BlockType(Flag):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def markdown_to_blocks(markdown: str):
    result = re.split(r"\n{2,}", markdown)
    for i in range(len(result)):
        result[i] = result[i].strip()
        result[i] = result[i].strip('\n')
    return result

def block_to_block_type(block: str):
    if re.match(r'#{1,6} ', block) and len(block.splitlines()) == 1:
        return BlockType.HEADING
    elif len(re.findall(r'^(```)|(```)$', block)) == 2:
        return BlockType.CODE
    elif re.fullmatch(r'(> (?:.+)\n?)+', block):
        return BlockType.QUOTE
    elif re.fullmatch(r'(- (?:.+)\n?)+', block):
        return BlockType.UNORDERED_LIST
    elif re.fullmatch(r'(\d+\. (?:.+)\n?)+', block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH