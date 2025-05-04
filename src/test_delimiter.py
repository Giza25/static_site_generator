import unittest

import delimiter
from textnode import TextNode, MDTextType

class TestDelimiter(unittest.TestCase):

    def test_delimiter(self):
        old_nodes = [
            TextNode("This is text with a `code block` word", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = delimiter.split_nodes_delimiter(*old_nodes, delimiter='`', text_type=MDTextType.CODE_TEXT)
        print(
            f"""
Testing split_nodes_delimiters function:
Expected: [TextNode("This is text with a ", MDTextType.NORMAL_TEXT, None), TextNode("code block", MDTextType.CODE_TEXT, None), TextNode(" word", MDTextType.NORMAL_TEXT, None)]
Actual: {new_nodes}
"""
        )
        self.assertEqual(str(new_nodes), "[TextNode(\"This is text with a \", MDTextType.NORMAL_TEXT, None), TextNode(\"code block\", MDTextType.CODE_TEXT, None), TextNode(\" word\", MDTextType.NORMAL_TEXT, None)]")

    def test_delimiter_multiple_types(self):
        old_nodes = [
            TextNode("This is a text with **bold**, _italic_ and `code`", MDTextType.NORMAL_TEXT)
        ]
        print(f"Testing split_nodes_delimiters dunction:\n Input: {old_nodes}")
        new_nodes = delimiter.split_nodes_delimiter(*old_nodes, delimiter='`', text_type=MDTextType.CODE_TEXT)
        print(f"After code: {new_nodes}")
        new_nodes = delimiter.split_nodes_delimiter(*new_nodes, delimiter='_', text_type=MDTextType.ITALIC_TEXT)
        print(f"After italic: {new_nodes}")
        new_nodes = delimiter.split_nodes_delimiter(*new_nodes, delimiter='**', text_type=MDTextType.BOLD_TEXT)
        print(f"After bold: {new_nodes}")
        