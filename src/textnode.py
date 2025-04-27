from enum import Enum
from htmlnode import LeafNode

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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        match self.text_type:
            case MDTextType.NORMAL_TEXT:
                return LeafNode(None, self.text)
            case MDTextType.BOLD_TEXT:
                return LeafNode("b", self.text)
            case MDTextType.ITALIC_TEXT:
                return LeafNode("i", self.text)
            case MDTextType.CODE_TEXT:
                return LeafNode("code", self.text)
            case MDTextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case MDTextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise TypeError("Unsupported type!")