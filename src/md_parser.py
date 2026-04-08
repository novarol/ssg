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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
  return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
  return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
  new_nodes = []
  for node in old_nodes:
    if (node.text_type != TextType.PLAIN):
      new_nodes.append(node)
      continue

    extracted_images = extract_markdown_images(node.text)

    if (not extracted_images):
      new_nodes.append(node)
      continue

    text_chunks = re.split("|".join(r"!\[" + text + r"\]\(" + url + r"\)" for text, url in extracted_images), node.text)

    for i, chunk in enumerate(text_chunks):
      if (chunk != ""):
        new_nodes.append(TextNode(chunk, TextType.PLAIN))

      if (i < len(extracted_images)):
        text, url = extracted_images[i]
        new_nodes.append(TextNode(text, TextType.IMAGE, url))

  return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
  new_nodes = []
  for node in old_nodes:
    if (node.text_type != TextType.PLAIN):
      new_nodes.append(node)
      continue

    extracted_links = extract_markdown_links(node.text)

    if (not extracted_links):
      new_nodes.append(node)
      continue

    text_chunks = re.split("|".join(r"\[" + text + r"\]\(" + url + r"\)" for text, url in extracted_links), node.text)

    for i, chunk in enumerate(text_chunks):
      if (chunk != ""):
        new_nodes.append(TextNode(chunk, TextType.PLAIN))

      if (i < len(extracted_links)):
        text, url = extracted_links[i]
        new_nodes.append(TextNode(text, TextType.LINK, url))

  return new_nodes
