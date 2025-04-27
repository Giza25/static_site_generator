from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method is not yet implemented within the class")
    
    """
    Converts 'props' attribute to a single string
    """
    def props_to_html(self):
        props = ""
        if self.props == None:
            return props
        for item in self.props:
            props = f"{props} {item}={self.props[item]}"
        return props[1:] # Deleting the first space in the output
    
    def __repr__(self):
        representation = (
f"""HTMLNode object:
tag = {self.tag}
value = {self.value}
children = {self.children}
properties = {self.props_to_html()}
"""
        )
        return representation
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError("LeafNode class object should have a value")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        result = (
            self.value
        ) if not self.tag else ((                                               # Condition to handle situation where Leaf has no tag
            f"<{self.tag}>{self.value}</{self.tag}>"
        ) if not self.props else (                                              # Condition to adress the space between the tag and the props
            f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        ))
        return result
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag == None:
            raise ValueError("ParentNode class object should have a tag")
        if children == None or children == []:
            raise ValueError("ParentNode class object should have at least 1 child object")
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        children_to_html = ""
        for child in self.children:
            children_to_html = f"{children_to_html}{child.to_html()}"
        result = (
            f"<{self.tag}>{children_to_html}</{self.tag}>"
        ) if not self.props else (
            f"<{self.tag} {self.props_to_html()}>{children_to_html}</{self.tag}>"
        )
        return result
        