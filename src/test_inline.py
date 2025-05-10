import unittest
from inline import split_markdown, split_nodes_delimiter, extract_md_images, extract_md_links, split_nodes_image, split_nodes_link
from textnode import TextNode, MDTextType

class TestDelimiter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diffs in test output

    def test_delimiter(self):
        print("\n=== Testing delimiter splitting ===")
        old_nodes = [
            TextNode("This is text with a `code block` word", MDTextType.NORMAL_TEXT)
        ]
        print(f"Input: {old_nodes}")
        expected = [
            TextNode("This is text with a ", MDTextType.NORMAL_TEXT),
            TextNode("code block", MDTextType.CODE_TEXT),
            TextNode(" word", MDTextType.NORMAL_TEXT)
        ]
        print(f"Expected: {expected}")
        new_nodes = split_nodes_delimiter(*old_nodes, delimiter='`', text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {new_nodes}")
        self.assertEqual(str(new_nodes), "[TextNode(\"This is text with a \", MDTextType.NORMAL_TEXT, None), TextNode(\"code block\", MDTextType.CODE_TEXT, None), TextNode(\" word\", MDTextType.NORMAL_TEXT, None)]")

    def test_delimiter_multiple_types(self):
        print("\n=== Testing delimiter splitting with multiple types ===")
        old_nodes = [
            TextNode("This is a text with **bold**, _italic_ and `code`", MDTextType.NORMAL_TEXT)
        ]
        print(f"Input: {old_nodes}")
        new_nodes = split_nodes_delimiter(*old_nodes, delimiter='`', text_type=MDTextType.CODE_TEXT)
        print(f"After code: {new_nodes}")
        new_nodes = split_nodes_delimiter(*new_nodes, delimiter='_', text_type=MDTextType.ITALIC_TEXT)
        print(f"After italic: {new_nodes}")
        new_nodes = split_nodes_delimiter(*new_nodes, delimiter='**', text_type=MDTextType.BOLD_TEXT)
        print(f"After bold: {new_nodes}")

    def test_delimiter_nested(self):
        print("\n=== Testing nested delimiter splitting ===")
        old_nodes = [
            TextNode("This node **has a _nested_ text**", MDTextType.NORMAL_TEXT)
        ]
        print(f"Input: {old_nodes}")
        new_nodes = split_nodes_delimiter(*old_nodes, delimiter='**', text_type=MDTextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(*new_nodes, delimiter='_', text_type=MDTextType.ITALIC_TEXT)
        print(f"Output: {new_nodes}")

    def test_split_delimiter_basic(self):
        print("\n=== Testing basic code delimiter splitting ===")
        node = TextNode("This is `code` text", MDTextType.NORMAL_TEXT)
        print(f"Input: {node}")
        expected = [
            TextNode("This is ", MDTextType.NORMAL_TEXT),
            TextNode("code", MDTextType.CODE_TEXT),
            TextNode(" text", MDTextType.NORMAL_TEXT)
        ]
        print(f"Expected: {expected}")
        nodes = split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {nodes}")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, MDTextType.CODE_TEXT)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, MDTextType.NORMAL_TEXT)

    def test_split_delimiter_multiple_occurrences(self):
        print("\n=== Testing multiple code delimiter occurrences ===")
        node = TextNode("Text with `code` and more `code`", MDTextType.NORMAL_TEXT)
        print(f"Input: {node}")
        expected = [
            TextNode("Text with ", MDTextType.NORMAL_TEXT),
            TextNode("code", MDTextType.CODE_TEXT),
            TextNode(" and more ", MDTextType.NORMAL_TEXT),
            TextNode("code", MDTextType.CODE_TEXT),
            TextNode("", MDTextType.NORMAL_TEXT)
        ]
        print(f"Expected: {expected}")
        nodes = split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {nodes}")
        self.assertEqual(len(nodes), 4)
        self.assertTrue(all(n.text_type == MDTextType.CODE_TEXT for n in [nodes[1], nodes[3]]))
        self.assertTrue(all(n.text_type == MDTextType.NORMAL_TEXT for n in [nodes[0], nodes[2]]))

    def test_split_delimiter_no_delimiters(self):
        print("\n=== Testing text with no delimiters ===")
        node = TextNode("Plain text without delimiters", MDTextType.NORMAL_TEXT)
        print(f"Input: {node}")
        expected = [TextNode("Plain text without delimiters", MDTextType.NORMAL_TEXT)]
        print(f"Expected: {expected}")
        nodes = split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {nodes}")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Plain text without delimiters")
        self.assertEqual(nodes[0].text_type, MDTextType.NORMAL_TEXT)

    def test_split_delimiter_odd_delimiters(self):
        print("\n=== Testing text with odd number of delimiters ===")
        node = TextNode("Text with `odd number` of delimiters`", MDTextType.NORMAL_TEXT)
        print(f"Input: {node}")
        print("Expected: Exception for odd number of delimiters")
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {str(context.exception)}")

    def test_split_delimiter_empty_content(self):
        print("\n=== Testing empty content between delimiters ===")
        node = TextNode("Text with `` empty delimiters", MDTextType.NORMAL_TEXT)
        print(f"Input: {node}")
        expected = [
            TextNode("Text with ", MDTextType.NORMAL_TEXT),
            TextNode("", MDTextType.CODE_TEXT),
            TextNode(" empty delimiters", MDTextType.NORMAL_TEXT)
        ]
        print(f"Expected: {expected}")
        nodes = split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {nodes}")
        self.assertEqual(len(nodes), 2)

    def test_non_normal_text_node(self):
        print("\n=== Testing already formatted text node ===")
        node = TextNode("Already formatted text", MDTextType.BOLD_TEXT)
        print(f"Input: {node}")
        expected = [TextNode("Already formatted text", MDTextType.BOLD_TEXT)]
        print(f"Expected: {expected}")
        nodes = split_nodes_delimiter(node, delimiter="`", text_type=MDTextType.CODE_TEXT)
        print(f"Actual: {nodes}")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, MDTextType.BOLD_TEXT)

class testImagesLinks(unittest.TestCase):
    def test_image1(self):
        matches = extract_md_images(
            "This is an image ![image](https://i.redd.it/v8gm7jc4uyye1.png)"
        )
        print(
f"""
Testing extract_md_images function - basic case
Input: This is an image ![image](https://i.redd.it/v8gm7jc4uyye1.png)
Expected: [('image', 'https://i.redd.it/v8gm7jc4uyye1.png')]
Output: {matches}
"""
        )
        self.assertListEqual(matches, [('image', 'https://i.redd.it/v8gm7jc4uyye1.png')])

    def test_multiple_images(self):
        text = "Multiple images: ![img1](https://example.com/img1.jpg) and ![img2](https://example.com/img2.png)"
        matches = extract_md_images(text)
        print(
f"""
Testing extract_md_images function - multiple images
Input: {text}
Expected: [('img1', 'https://example.com/img1.jpg'), ('img2', 'https://example.com/img2.png')]
Output: {matches}
"""
        )
        self.assertListEqual(matches, [('img1', 'https://example.com/img1.jpg'), ('img2', 'https://example.com/img2.png')])

    def test_no_images(self):
        text = "This is a text without any images"
        matches = extract_md_images(text)
        print(
f"""
Testing extract_md_images function - no images
Input: {text}
Expected: []
Output: {matches}
"""
        )
        self.assertListEqual(matches, [])

    def test_invalid_image_syntax(self):
        text = "Invalid image syntax: ![image(https://example.com/img.jpg) and [image](https://example.com/img.jpg)"
        matches = extract_md_images(text)
        print(
f"""
Testing extract_md_images function - invalid syntax
Input: {text}
Expected: []
Output: {matches}
"""
        )
        self.assertListEqual(matches, [])

    def test_link1(self):
        matches = extract_md_links(
            "This is a link [link](https://regexr.com)"
        )
        print(
f"""
Testing extract_md_links function - basic case
Input: This is a link [link](https://regexr.com)
Expected: [('link', 'https://regexr.com')]
Output: {matches}
"""
        )
        self.assertListEqual(matches, [('link', 'https://regexr.com')])

    def test_multiple_links(self):
        text = "Multiple links: [link1](https://example.com) and [link2](https://example.org)"
        matches = extract_md_links(text)
        print(
f"""
Testing extract_md_links function - multiple links
Input: {text}
Expected: [('link1', 'https://example.com'), ('link2', 'https://example.org')]
Output: {matches}
"""
        )
        self.assertListEqual(matches, [('link1', 'https://example.com'), ('link2', 'https://example.org')])

    def test_no_links(self):
        text = "This is a text without any links"
        matches = extract_md_links(text)
        print(
f"""
Testing extract_md_links function - no links
Input: {text}
Expected: []
Output: {matches}
"""
        )
        self.assertListEqual(matches, [])

    def test_invalid_link_syntax(self):
        text = "Invalid link syntax: [link(https://example.com) and ![link](https://example.com)"
        matches = extract_md_links(text)
        print(
f"""
Testing extract_md_links function - invalid syntax
Input: {text}
Expected: []
Output: {matches}
"""
        )
        self.assertListEqual(matches, [])

class testDelimiterImagesLinks(unittest.TestCase):
    def test_node_with_link(self):
        print("\n=== Testing basic link splitting ===")
        old_nodes = [
            TextNode("This is a text with a [link](https://www.boot.dev)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_link(*old_nodes)
        print(
f"""
Testing split_nodes_link function
Expected: [TextNode("This is a text with a ", MDTextType.NORMAL_TEXT, None), TextNode("link", MDTextType.LINK, "https://www.boot.dev")]
Actual: {new_nodes}
"""
)
        self.assertEqual(str(new_nodes), "[TextNode(\"This is a text with a \", MDTextType.NORMAL_TEXT, None), TextNode(\"link\", MDTextType.LINK, https://www.boot.dev)]")

    def test_multiple_links(self):
        print("\n=== Testing multiple links splitting ===")
        old_nodes = [
            TextNode("Text with [link1](https://example.com) and [link2](https://example.org)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_link(*old_nodes)
        print(f"Input: {old_nodes}")
        print("Expected: Multiple nodes with two links and surrounding text")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 4)  # Text + link1 + text + link2
        self.assertEqual(new_nodes[1].text, "link1")
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[3].text, "link2")
        self.assertEqual(new_nodes[3].url, "https://example.org")

    def test_no_links(self):
        print("\n=== Testing text with no links ===")
        old_nodes = [
            TextNode("This is a text without any links", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_link(*old_nodes)
        print(f"Input: {old_nodes}")
        print(f"Expected: [TextNode(\"This is a text without any links\", MDTextType.NORMAL_TEXT, None)]")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a text without any links")
        self.assertEqual(new_nodes[0].text_type, MDTextType.NORMAL_TEXT)

    def test_non_normal_text_node(self):
        print("\n=== Testing already formatted text node ===")
        old_nodes = [
            TextNode("[link](https://example.com)", MDTextType.BOLD_TEXT)
        ]
        new_nodes = split_nodes_link(*old_nodes)
        print(f"Input: {old_nodes}")
        print(f"Expected: [TextNode(\"[link](https://example.com)\", MDTextType.BOLD_TEXT, None)]")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, MDTextType.BOLD_TEXT)

    def test_empty_text_between_links(self):
        print("\n=== Testing empty text between links ===")
        old_nodes = [
            TextNode("[link1](https://example.com)[link2](https://example.org)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_link(*old_nodes)
        print(f"Input: {old_nodes}")
        print("Expected: Two link nodes with empty text node between")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "link1")
        self.assertEqual(new_nodes[0].url, "https://example.com")
        self.assertEqual(new_nodes[1].text, "link2")
        self.assertEqual(new_nodes[1].url, "https://example.org")

    def test_node_with_image(self):
        print("\n=== Testing basic image splitting ===")
        old_nodes = [
            TextNode("This is a text with an ![image](https://i.redd.it/v8gm7jc4uyye1.png)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_image(*old_nodes)
        print(
f"""
Testing split_nodes_link function
Expected: [TextNode("This is a text with an ", MDTextType.NORMAL_TEXT, None), TextNode("image", MDTextType.IMAGE, "https://i.redd.it/v8gm7jc4uyye1.png")]
Actual: {new_nodes}
"""
)
        self.assertEqual(str(new_nodes), "[TextNode(\"This is a text with an \", MDTextType.NORMAL_TEXT, None), TextNode(\"image\", MDTextType.IMAGE, https://i.redd.it/v8gm7jc4uyye1.png)]")

    def test_multiple_images(self):
        print("\n=== Testing multiple images splitting ===")
        old_nodes = [
            TextNode("Images: ![img1](https://example.com/img1.jpg) and ![img2](https://example.com/img2.png)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_image(*old_nodes)
        print(f"Input: {old_nodes}")
        print("Expected: Multiple nodes with two images and surrounding text")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 4)  # Text + img1 + text + img2
        self.assertEqual(new_nodes[1].text, "img1")
        self.assertEqual(new_nodes[1].url, "https://example.com/img1.jpg")
        self.assertEqual(new_nodes[3].text, "img2")
        self.assertEqual(new_nodes[3].url, "https://example.com/img2.png")

    def test_no_images(self):
        print("\n=== Testing text with no images ===")
        old_nodes = [
            TextNode("This is a text without any images", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_image(*old_nodes)
        print(f"Input: {old_nodes}")
        print(f"Expected: [TextNode(\"This is a text without any images\", MDTextType.NORMAL_TEXT, None)]")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is a text without any images")
        self.assertEqual(new_nodes[0].text_type, MDTextType.NORMAL_TEXT)

    def test_non_normal_text_node_image(self):
        print("\n=== Testing already formatted text node with image ===")
        old_nodes = [
            TextNode("![image](https://example.com/img.jpg)", MDTextType.BOLD_TEXT)
        ]
        new_nodes = split_nodes_image(*old_nodes)
        print(f"Input: {old_nodes}")
        print(f"Expected: [TextNode(\"![image](https://example.com/img.jpg)\", MDTextType.BOLD_TEXT, None)]")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, MDTextType.BOLD_TEXT)

    def test_empty_text_between_images(self):
        print("\n=== Testing empty text between images ===")
        old_nodes = [
            TextNode("![img1](https://example.com/img1.jpg)![img2](https://example.com/img2.png)", MDTextType.NORMAL_TEXT)
        ]
        new_nodes = split_nodes_image(*old_nodes)
        print(f"Input: {old_nodes}")
        print("Expected: Two image nodes with no text between")
        print(f"Actual: {new_nodes}")
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "img1")
        self.assertEqual(new_nodes[0].url, "https://example.com/img1.jpg")
        self.assertEqual(new_nodes[1].text, "img2")
        self.assertEqual(new_nodes[1].url, "https://example.com/img2.png")

class testSplitMarkdown(unittest.TestCase):
    def test_split_markdown(self):
        print("\n=== Testing split_markdown basic functionality ===")
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = split_markdown(text)
        print(f"Input: {text}")
        print(f"Output: {nodes}")
        
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, MDTextType.BOLD_TEXT)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, MDTextType.ITALIC_TEXT)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, MDTextType.CODE_TEXT)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, MDTextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, MDTextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_split_markdown_nested(self):
        print("\n=== Testing split_markdown with nested formatting ===")
        text = "This is **bold with _italic_ inside** text"
        nodes = split_markdown(text)
        print(f"Input: {text}")
        print(f"Output: {nodes}")
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[1].text, "bold with _italic_ inside")
        self.assertEqual(nodes[1].text_type, MDTextType.BOLD_TEXT)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, MDTextType.NORMAL_TEXT)

    def test_split_markdown_empty(self):
        print("\n=== Testing split_markdown with empty text ===")
        text = ""
        nodes = split_markdown(text)
        print(f"Input: empty string")
        print(f"Output: {nodes}")
        
        self.assertEqual(len(nodes), 0)

    def test_split_markdown_no_formatting(self):
        print("\n=== Testing split_markdown with no markdown formatting ===")
        text = "This is just plain text without any formatting"
        nodes = split_markdown(text)
        print(f"Input: {text}")
        print(f"Output: {nodes}")
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, MDTextType.NORMAL_TEXT)

    def test_split_markdown_multiple_same_format(self):
        print("\n=== Testing split_markdown with multiple instances of same formatting ===")
        text = "**Bold** normal **bold again** and _italic_ then _more italic_"
        nodes = split_markdown(text)
        print(f"Input: {text}")
        print(f"Output: {nodes}")
        
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "Bold")
        self.assertEqual(nodes[0].text_type, MDTextType.BOLD_TEXT)
        self.assertEqual(nodes[1].text, " normal ")
        self.assertEqual(nodes[1].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[2].text, "bold again")
        self.assertEqual(nodes[2].text_type, MDTextType.BOLD_TEXT)
        self.assertEqual(nodes[3].text, " and ")
        self.assertEqual(nodes[3].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[4].text, "italic")
        self.assertEqual(nodes[4].text_type, MDTextType.ITALIC_TEXT)
        self.assertEqual(nodes[5].text, " then ")
        self.assertEqual(nodes[5].text_type, MDTextType.NORMAL_TEXT)
        self.assertEqual(nodes[6].text, "more italic")
        self.assertEqual(nodes[6].text_type, MDTextType.ITALIC_TEXT)

if __name__ == "__main__":
    unittest.main()
