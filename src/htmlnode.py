from enum import Enum
from typing import List

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, 
                 children: List['HTMLNode'] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        s = ""
        for k,v in self.props.items():
            s += f' {k}="{v}"'
        return s
    
    def __repr__(self):
        return f"HMTLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if not self.value:
            return ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        
        #return f'<{self.tag}{self.props_to_html}>\n{self.children_to_html}\n</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>'

    def children_to_html(self):
        s = ""
        for node in self.children:
            s += node.to_html()
        return s