import unittest

from textnode import TextNode, MDTextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", MDTextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", MDTextType.BOLD_TEXT)
        print(f"Testig equality of {node} and {node2}...\n")
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", MDTextType.ITALIC_TEXT, None)
        node2 = TextNode("This is a text node", MDTextType.ITALIC_TEXT)
        print(f"Testing equality of {node} and {node2} with url assigned to default value...\n")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", MDTextType.ITALIC_TEXT, None)
        node2 = TextNode("This is another text node", MDTextType.BOLD_TEXT)
        print(f"Testing unequality of {node} and {node2}...\n")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", MDTextType.NORMAL_TEXT)
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: This is a text node
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", MDTextType.BOLD_TEXT)
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <b>This is a bold text</b>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_italic(self):
        node = TextNode("This is in italic", MDTextType.ITALIC_TEXT)
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <i>This is in italic</i>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is in italic")

    def test_bold_and_italic(self):
        node = TextNode("This is both bold and italic", (MDTextType.ITALIC_TEXT, MDTextType.BOLD_TEXT))
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <b><i>This is both bold and italic</i></b>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "<i>This is both bold and italic</i>")

    def test_code(self):
        node = TextNode("This is a code", MDTextType.CODE_TEXT)
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <code>This is a code</code>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code")

    def test_link(self):
        node = TextNode("This is a link", MDTextType.LINK, "https://www.youtube.com")
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <a href=https://www.youtube.com>This is a link</a>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.youtube.com"})

    def test_image(self):
        node = TextNode("This is an image", MDTextType.IMAGE, "https://i.imgur.com/EzebBCP.jpeg")
        html_node = node.text_node_to_html_node()
        print(
f"""Testing TextNode 'text_node_to_html_node()' method
Expected: <img src=https://i.imgur.com/EzebBCP.jpeg alt="This is an image"></img>
Actual: {html_node.to_html()}\n"""
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://i.imgur.com/EzebBCP.jpeg", "alt": "This is an image"})


if __name__ == "__main__":
    unittest.main()