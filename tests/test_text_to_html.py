import unittest

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode
from src.main import text_node_to_html_node


class TestTextToHtml(unittest.TestCase):
    def test_normal_text(self):
        # Test converting normal text (equivalent to the provided TextType.TEXT)
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})
        
    def test_bold_text(self):
        # Test converting bold text
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})
        
    def test_italic_text(self):
        # Test converting italic text
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})
        
    def test_code_text(self):
        # Test converting code text
        node = TextNode("const x = 5;", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "const x = 5;")
        self.assertEqual(html_node.props, {})
        
    def test_link(self):
        # Test converting link
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        
    def test_image(self):
        # Test converting image
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.png",
            "alt": "Alt text for image"
        })
        
    def test_invalid_type(self):
        # Test handling invalid TextType
        # Create a mock TextNode with an invalid type for testing
        class MockTextNode:
            def __init__(self):
                self.text = "test"
                self.text_type = "invalid"
                
        with self.assertRaises(Exception):
            text_node_to_html_node(MockTextNode())
            
    def test_html_rendering(self):
        # Test that the HTML nodes can be rendered correctly
        test_cases = [
            (TextNode("Normal text", TextType.NORMAL), "Normal text"),
            (TextNode("Bold text", TextType.BOLD), "<b>Bold text</b>"),
            (TextNode("Italic text", TextType.ITALIC), "<i>Italic text</i>"),
            (TextNode("Code snippet", TextType.CODE), "<code>Code snippet</code>"),
            (TextNode("Link text", TextType.LINK, "https://example.com"), 
             '<a href="https://example.com">Link text</a>'),
            (TextNode("Image description", TextType.IMAGE, "https://example.com/img.jpg"),
             '<img src="https://example.com/img.jpg" alt="Image description"></img>'),
        ]
        
        for text_node, expected_html in test_cases:
            html_node = text_node_to_html_node(text_node)
            self.assertEqual(html_node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()