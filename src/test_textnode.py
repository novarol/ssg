import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_eq_url(self):
    node = TextNode("This is a link text node", TextType.LINK, "https://example.com/")
    node2 = TextNode("This is a link text node", TextType.LINK, "https://example.com/")
    self.assertEqual(node, node2)

  def test_eq_url_none(self):
    node = TextNode("This is a text node", TextType.ITALIC)
    node2 = TextNode("This is a text node", TextType.ITALIC, None)
    self.assertEqual(node, node2)

  def test_not_eq_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    node2 = TextNode("This is another text node", TextType.PLAIN)
    self.assertNotEqual(node, node2)

  def test_not_eq_url(self):
    node = TextNode("This is a link text node", TextType.IMAGE, "https://test.com/")
    node2 = TextNode("This is a link text node", TextType.IMAGE, "https://example.com/")
    self.assertNotEqual(node, node2)

  def test_not_eq_type(self):
    node = TextNode("This is a text node", TextType.CODE)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertNotEqual(node, node2)

  def test_to_html_node_plain_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_to_html_node_bold_text(self):
    node = TextNode("This is a text node", TextType.BOLD)
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a text node")

  def test_to_html_node_italic_text(self):
    node = TextNode("This is a text node", TextType.ITALIC)
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is a text node")

  def test_to_html_node_code_text(self):
    node = TextNode("This is a text node", TextType.CODE)
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a text node")

  def test_to_html_node_link_text(self):
    node = TextNode("This is a text node", TextType.LINK, "https://example.com/")
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a text node")
    self.assertEqual(html_node.props, { "href": "https://example.com/"})

  def test_to_html_node_image_text(self):
    node = TextNode("This is an image node", TextType.IMAGE, "https://example.com/")
    html_node = node.to_html_node()
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, { "src": "https://example.com/", "alt": "This is an image node" })

if __name__ == "__main__":
  unittest.main()
