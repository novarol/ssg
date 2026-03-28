from typing import Dict
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag: str, value: str, props: Dict[str, str] = None):
    super().__init__(tag, value, props=props)

  def to_html(self):
    if (not self.value):
      raise ValueError
    if (not self.tag):
      return self.value

    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"