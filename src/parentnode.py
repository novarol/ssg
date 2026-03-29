from typing import Dict, Self
from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: list[LeafNode], props: Dict[str, str] = None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if (not self.tag):
      raise ValueError
    if (not self.children):
      raise ValueError
    
    children_html = ""

    for child in self.children:
      children_html += child.to_html()

    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
  
  def __repr__(self):
    return f"ParentNode({self.tag}, {self.children}, {self.props})"