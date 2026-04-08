import unittest

from md_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestMDParser(unittest.TestCase):
  def test_split_bold(self):
    node = TextNode("This text has some **bold text** in it", TextType.PLAIN)
    self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
      TextNode("This text has some ", TextType.PLAIN),
      TextNode("bold text", TextType.BOLD),
      TextNode(" in it", TextType.PLAIN)
    ])

  def test_split_bold_start(self):
    node = TextNode("**Bold text** is at the start of this text", TextType.PLAIN)
    self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
      TextNode("Bold text", TextType.BOLD),
      TextNode(" is at the start of this text", TextType.PLAIN),
    ])

  def test_split_bold_end(self):
    node = TextNode("This text ends with **bold text**", TextType.PLAIN)
    self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
      TextNode("This text ends with ", TextType.PLAIN),
      TextNode("bold text", TextType.BOLD),
    ])

  def test_split_nodes_delimiter_missing_delimiter(self):
    node = TextNode("This text has some **bold text in it", TextType.PLAIN)
    with self.assertRaises(Exception) as cm:
      split_nodes_delimiter([node], "**", TextType.BOLD)

    self.assertTrue("Invalid markdown text. Closing ** missing." in str(cm.exception))
  
  def test_split_bold_multiple(self):
    node = TextNode("This **text has** multiple **bold text** in it", TextType.PLAIN)
    self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
      TextNode("This ", TextType.PLAIN),
      TextNode("text has", TextType.BOLD),
      TextNode(" multiple ", TextType.PLAIN),
      TextNode("bold text", TextType.BOLD),
      TextNode(" in it", TextType.PLAIN)
    ])

  def test_split_bold_italic(self):
    node = TextNode("This text has **bold text** and _italic text_ in it", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    self.assertEqual(new_nodes, [
      TextNode("This text has ", TextType.PLAIN),
      TextNode("bold text", TextType.BOLD),
      TextNode(" and ", TextType.PLAIN),
      TextNode("italic text", TextType.ITALIC),
      TextNode(" in it", TextType.PLAIN)
    ])

  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

  def test_extract_markdown_images_multiple(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://example.com/)"
    )
    self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://example.com/")])

  def test_extract_markdown_images_with_link(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com/)"
    )
    self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual(matches, [("link", "https://i.imgur.com/zjjcJKZ.png")])

  def test_extract_markdown_links_multiple(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and [another link](https://example.com/)"
    )
    self.assertListEqual(matches, [("link", "https://i.imgur.com/zjjcJKZ.png"), ("another link", "https://example.com/")])

  def test_extract_markdown_links_with_image(self):
    matches = extract_markdown_links(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com/)"
    )
    self.assertListEqual(matches, [("link", "https://example.com/")])

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://example.com/) and another ![second image](https://test.com/)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second image", TextType.IMAGE, "https://test.com/"),
        ],
        new_nodes,
    )

  def test_split_images_beginning_end(self):
    node = TextNode(
        "![This image](https://example.com/) and ![that image](https://test.com/)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This image", TextType.IMAGE, "https://example.com/"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("that image", TextType.IMAGE, "https://test.com/"),
        ],
        new_nodes,
    )

  def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://example.com/) and another [second link](https://test.com/)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com/"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second link", TextType.LINK, "https://test.com/"),
        ],
        new_nodes,
    )

  def test_split_links_beginning_end(self):
    node = TextNode(
        "[This link](https://example.com/) and [that link](https://test.com/)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This link", TextType.LINK, "https://example.com/"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("that link", TextType.LINK, "https://test.com/"),
        ],
        new_nodes,
    )
