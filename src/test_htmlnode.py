import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
  def test_no_props(self):
    node = HTMLNode(value="This is a text node")
    self.assertEqual(node.props_to_html(), "")

  def test_single_prop(self):
    node = HTMLNode(tag="a", value="This is a text node", props={"href": "https://example.com/"})
    self.assertEqual(node.props_to_html(), ' href="https://example.com/"')

  def test_multiple_props(self):
    node = HTMLNode(tag="img", props={"src": "https://example.com/", "alt": "This is an image"})
    self.assertEqual(node.props_to_html(), ' src="https://example.com/" alt="This is an image"')

if __name__ == "__main__":
  unittest.main()
