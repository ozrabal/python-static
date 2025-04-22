import unittest

from textnode import TextNode
from textnode import TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Text one", TextType.NORMAL)
        node2 = TextNode("Text two", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://a.com")
        node2 = TextNode("Link text", TextType.LINK, "https://b.com")
        self.assertNotEqual(node1, node2)

    def test_eq_none_url_defaults(self):
        node1 = TextNode("Plain text", TextType.NORMAL)
        node2 = TextNode("Plain text", TextType.NORMAL, None)
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()