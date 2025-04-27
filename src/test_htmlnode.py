import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop1(self):
        node = HTMLNode("<a>", "This is an HTML node", None, None)
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
        node = HTMLNode("<a>", "This is an HTML node", None, props)
        test = (
f"""Testing class representation:
{node}\n"""
)
        print(test)


if __name__ == "__main__":
    unittest.main()