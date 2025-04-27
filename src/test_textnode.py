import unittest

from textnode import TextNode, MDTextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", MDTextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", MDTextType.BOLD_TEXT)
        print(f"Testig equality of {node} and {node2}...")
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", MDTextType.ITALIC_TEXT, None)
        node2 = TextNode("This is a text node", MDTextType.ITALIC_TEXT)
        print(f"Testing equality of {node} and {node2} with url assigned to default value...")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", MDTextType.ITALIC_TEXT, None)
        node2 = TextNode("This is another text node", MDTextType.BOLD_TEXT)
        print(f"Testing unequality of {node} and {node2}...")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()