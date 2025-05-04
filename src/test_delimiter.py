import unittest
from delimiter import split_nodes_delimiter
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
        self.assertEqual(len(nodes), 5)
        self.assertTrue(all(n.text_type == MDTextType.CODE_TEXT for n in [nodes[1], nodes[3]]))
        self.assertTrue(all(n.text_type == MDTextType.NORMAL_TEXT for n in [nodes[0], nodes[2], nodes[4]]))

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
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[1].text_type, MDTextType.CODE_TEXT)

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

if __name__ == "__main__":
    unittest.main()
