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

## This is another heading
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")
        
    def test_paragraph_base(self):
        md = """
This is a paragraph of text with **bold**, _italic_
and
`code` texts
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")
        
    def test_code_base(self):
        md = """
```
```# This is a block of random `code` with **mixed** _markdown_ that should be unprocessed```
print("Hello World")
```
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")
        
    def test_quote_base(self):
        md = """
> This is a quote
> With several lines
> And a text with **some** _markdown_
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")
        
    def test_unordered_list_base(self):
        md = """
- This is an **unordered** list
- With some elements
- with _mixed_ `markdown`
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")
        
    def test_ordered_list_base(self):
        md = """
3. This is an **ordered** list
228. With some elements
1. with _mixed_ `markdown`
"""
        node = markdown_to_html(md)
        html = node.to_html()
        print(f"""
Input: {md}
Output: {html}
""")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )