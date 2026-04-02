import unittest

from md_parser import split_nodes_delimiter
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
