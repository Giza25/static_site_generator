from enum import Enum
from typing import Type

class MDTextType(Enum):
    NORMAL_TEXT = "Normal Text"
    BOLD_TEXT = "Bold Text"
    ITALIC_TEXT = "Italic Text"
    CODE_TEXT = "Code Text"
    LINK = "Link"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text: str, text_type: MDTextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: 'TextNode'):
        return (self.text == other.text and 
            self.text_type == other.text_type and
            self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"