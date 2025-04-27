from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method is not yet implemented within the class")
    
    def props_to_html(self):
        props = ""
        if self.props == None:
            return props
        for item in self.props:
            props = f"{props} {item}={self.props[item]}"
        return props[1:]
    
    def __repr__(self):
        representation = f"""HTMLNode object:
tag = {self.tag}
value = {self.value}
children = {self.children}
properties = {self.props_to_html()}
"""
        return representation