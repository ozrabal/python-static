import unittest
import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.textnode import TextNode, TextType
from src.main import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_empty_text(self):
        """Test handling empty text."""
        text = ""
        expected = [TextNode("", TextType.NORMAL)]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_only_bold(self):
        """Test text with only bold formatting."""
        text = "**Bold text**"
        expected = [TextNode("Bold text", TextType.BOLD)]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_only_italic(self):
        """Test text with only italic formatting."""
        text = "_Italic text_"
        expected = [TextNode("Italic text", TextType.ITALIC)]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_only_code(self):
        """Test text with only code formatting."""
        text = "`Code text`"
        expected = [TextNode("Code text", TextType.CODE)]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_only_image(self):
        """Test text with only an image."""
        text = "![Alt text](https://example.com/img.jpg)"
        expected = [TextNode("Alt text", TextType.IMAGE, "https://example.com/img.jpg")]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_only_link(self):
        """Test text with only a link."""
        text = "[Link text](https://example.com)"
        expected = [TextNode("Link text", TextType.LINK, "https://example.com")]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_nested_formatting(self):
        """Test text with nested formatting (which should be processed in order)."""
        text = "_This is **bold within italic** text_"
        # Since we process the bold first and then italic, the bold will be preserved
        # while the text around it is made italic
        expected = [
            TextNode("_This is ", TextType.NORMAL),
            TextNode("bold within italic", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
            TextNode("_", TextType.NORMAL),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)
    
    def test_multiple_formatting_types(self):
        """Test text with multiple formatting types in irregular order."""
        text = "Normal `code` **bold** _italic_ ![img](url) [link](url)"
        expected = [
            TextNode("Normal ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.NORMAL),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url"),
        ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()