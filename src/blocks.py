import re
from textnode import MDTextType, TextNode

def markdown_to_blocks(markdown: str):
    result = re.split(r"\n{2,}", markdown)
    for i in range(len(result)):
        result[i] = result[i].strip()
        result[i] = result[i].strip('\n')
    return result
