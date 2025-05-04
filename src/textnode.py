from enum import Flag, auto
from htmlnode import LeafNode

class MDTextType(Flag):
    NORMAL_TEXT = auto()
    BOLD_TEXT = auto()
    ITALIC_TEXT = auto()
    CODE_TEXT = auto()
    LINK = auto()
    IMAGE = auto()

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
        return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        if MDTextType.BOLD_TEXT in self.text_type and MDTextType.ITALIC_TEXT in self.text_type:
            return LeafNode("b", LeafNode("i", self.text).to_html())
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