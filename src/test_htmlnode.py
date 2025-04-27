import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_prop1(self):
        node = HTMLNode("a", "This is an HTML node", None, None)
        node_props = node.props_to_html()
        print(
f"""Testing 'props_to_html()' method. 
Expecting: ''. 
Actual: '{node_props}'\n"""
)
        self.assertEqual(node_props, "")
    
    def test_prop2(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        node_props = node.props_to_html()
        print(
f"""Testing 'props_to_html()' method. 
Expecting: 'href=https://www.google.com target=_blank'. 
Actual: '{node_props}'\n"""
)
        self.assertEqual(node_props, "href=https://www.google.com target=_blank")

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "This is an HTML node", None, props)
        test = (
f"""Testing class representation:
{node}\n"""
)
        print(test)



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p1(self):
        node = LeafNode("p", "Hello, world!")
        print(
f"""Testing LeafNode 'to_html()' method
Expecting: <p>Hello, World</p>
Actual: {node.to_html()}\n"""
        )
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "This is a link!", {"href": "https://github.com/Giza25/static_site_generator/tree/main"})
        print(
f"""Testing LeafNode 'to_html()' method
Expecting: <a href=https://github.com/Giza25/static_site_generator/tree/main>This is a link!</a>
Actual: {node.to_html()}\n"""
        )
        self.assertEqual(node.to_html(), "<a href=https://github.com/Giza25/static_site_generator/tree/main>This is a link!</a>")

    def test_leaf_to_html_p3(self):
        node = LeafNode(None, "This is just a plain text", {"prop": "A random prop"})
        print(
f"""Testing LeafNode 'to_html()' method
Expecting: This is just a plain text
Actual: {node.to_html()}\n"""
        )
        self.assertEqual(node.to_html(), "This is just a plain text")
    
    def test_leaf_value(self):
        print("Catching ValueError...")
        try:
            node = LeafNode()
        except Exception as e:
            print(
f"""Expected: LeafNode class object should have a value
Actual: {e}\n"""
            )

if __name__ == "__main__":
    unittest.main()