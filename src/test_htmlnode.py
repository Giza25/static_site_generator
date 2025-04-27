import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
            self.assertEqual(str(e), 'LeafNode class object should have a value')



class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        print(
f"""Testing ParentNode 'to_html()' method
Expected: <div><span>child</span></div>
Actual: {parent_node.to_html()}\n"""
        )
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        print(
f"""Testing ParentNode 'to_html()' method
Expected: <div><span><b>grandchild</b></span></div>
Actual: {parent_node.to_html()}\n"""
        )
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_many_children(self):
        child_nodes = [
            LeafNode("a", "child_a", {"href": "https://www.boot.dev"}),
            LeafNode("b", "child_b"),
            LeafNode("c", "child_c", {"target": "None"})
        ]
        parent_node = ParentNode("div", child_nodes)
        print(
f"""Testing ParentNode 'to_html()' method
Expected: <div><a href=https://www.boot.dev>child_a</a><b>child_b</b><c target=None>child_c</c></div>
Actual: {parent_node.to_html()}\n"""
        )
        self.assertEqual(parent_node.to_html(), "<div><a href=https://www.boot.dev>child_a</a><b>child_b</b><c target=None>child_c</c></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"target": "None"})
        print(
f"""Testing ParentNode 'to_html()' method
Expected: <div target=None><span>child</span></div>
Actual: {parent_node.to_html()}\n"""
        )
        self.assertEqual(parent_node.to_html(), "<div target=None><span>child</span></div>")

    def test_Parent_value1(self):
        print("Catching ValueError...")
        try:
            node = ParentNode()
        except Exception as e:
            print(
f"""Expected: ParentNode class object should have a tag
Actual: {e}\n"""
            )
            self.assertEqual(str(e), 'ParentNode class object should have a tag')
    
    def test_Parent_value2(self):
        print("Catching ValueError...")
        try:
            node = ParentNode("a")
        except Exception as e:
            print(
f"""Expected: ParentNode class object should have at least 1 child object
Actual: {e}\n"""
            )
            self.assertEqual(str(e), 'ParentNode class object should have at least 1 child object')

    def test_Parent_value3(self):
        print("Catching ValueError...")
        try:
            node = ParentNode("a", [])
        except Exception as e:
            print(
f"""Expected: ParentNode class object should have at least 1 child object
Actual: {e}\n"""
            )
            self.assertEqual(str(e), 'ParentNode class object should have at least 1 child object')

if __name__ == "__main__":
    unittest.main()