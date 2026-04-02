import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
  new_nodes = []
  for node in old_nodes:
    if (node.text_type != TextType.PLAIN):
      new_nodes.append(node)
      continue

    if (node.text.count(delimiter) % 2 != 0):
      raise Exception(f"Invalid markdown text. Closing {delimiter} missing.")
    
    text_chunks = node.text.split(delimiter)
    for i, chunk in enumerate(text_chunks):
      if (chunk == ""):
        continue
      new_nodes.append(TextNode(chunk, TextType.PLAIN if i % 2 == 0 else text_type))

  return new_nodes

