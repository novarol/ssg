from typing import Dict, Self

class HTMLNode:
  def __init__(self, tag: str = None, value: str = None, children: list[Self] = None, props: Dict[str, str] = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    attributes = ""

    if (not self.props):
      return attributes
    
    for prop in self.props:
      attributes += f" {prop}=\"{self.props[prop]}\""

    return attributes
  
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
