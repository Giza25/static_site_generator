import unittest
from blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html

class TestMDToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

  This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is a paragraph of text
With a new line
Several actually
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_code(self):
        md = """
```
print('hello world')
```
"""
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        md = """
> This is a quote
> This is a second quote
"""
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list(self):
        md = """
- First item of the list
- Second item of the list
- Third item of the list
"""
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        md = """
1. This is the first item of the list
2. This is the second item of the list
"""
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_heading_1_hash(self):
        md = "# This is a header"
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_heading_6_hashes(self):
        md = "###### This is a header"
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_heading_7_hashes(self):
        md = "####### This is a header"
        block = markdown_to_blocks(md)
        block_type = block_to_block_type(block[0])
        self.assertNotEqual(block_type, BlockType.HEADING)


class TestMarkdownToHtml(unittest.TestCase):
    def test_heading_base(self):
        md = """
### This is a header with a **bold** text and a `code` and an _italic_ texts as well
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(html)