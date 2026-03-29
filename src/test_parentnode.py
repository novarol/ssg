import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestLeafNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_multiple_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    grandchild_node2 = LeafNode(None, "Hello, world!")
    grandchild_node3 = LeafNode("i", "grandchild2")
    child_node = ParentNode("span", [grandchild_node])
    child_node2 = ParentNode("p", [grandchild_node2, grandchild_node3])
    parent_node = ParentNode("div", [child_node, child_node2])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span><p>Hello, world!<i>grandchild2</i></p></div>",
    )
  
if __name__ == "__main__":
  unittest.main()
