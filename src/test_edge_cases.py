import unittest
import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from main import (
    extract_markdown_images, 
    extract_markdown_links,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestEdgeCases(unittest.TestCase):
    def test_malformed_markdown_links(self):
        """Test handling of malformed markdown links"""
        # Missing closing parenthesis
        text = "This is a [malformed link](https://example.com"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])  # Should not extract malformed links
        
        # Missing closing bracket
        text = "This is a [malformed link(https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        
        # Extra characters between brackets and parentheses
        text = "This is a [broken link] blah (https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    
    def test_malformed_markdown_images(self):
        """Test handling of malformed markdown images"""
        # Missing closing parenthesis
        text = "This is a ![malformed image](https://example.com/img.jpg"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        
        # Missing exclamation mark
        text = "[not an image](https://example.com/img.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_invalid_text_type(self):
        """Test error handling for invalid TextType"""
        # Create a custom class that mimics TextNode but with an invalid text_type
        class MockTextNode:
            def __init__(self):
                self.text = "test"
                self.text_type = "not_a_valid_type"  # Invalid type
        
        # Should raise an exception for invalid type
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(MockTextNode())
        self.assertTrue("Invalid TextType" in str(context.exception))
    
    def test_empty_nodes_list(self):
        """Test handling of empty node lists"""
        # Passing an empty list to the split functions should return an empty list
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])
        self.assertEqual(split_nodes_image([]), [])
        self.assertEqual(split_nodes_link([]), [])
    
    def test_consecutive_delimiters(self):
        """Test handling of consecutive delimiters"""
        # Text with consecutive bold delimiters
        text = "This has **consecutive** **delimiters**"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("consecutive", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("delimiters", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_delimiter_at_boundaries(self):
        """Test delimiters at the beginning and end of text"""
        # Delimiters at the beginning
        text = "**Bold at start** normal text"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("Bold at start", TextType.BOLD),
            TextNode(" normal text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)
        
        # Delimiters at the end
        text = "Normal text **bold at end**"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("Normal text ", TextType.NORMAL),
            TextNode("bold at end", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
    
    def test_odd_number_of_delimiters(self):
        """Test text with an odd number of delimiters"""
        # Odd number of delimiters should result in some unpaired ones
        text = "This **has an odd** number of ** delimiters"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # Based on the actual implementation, this is how unpaired delimiters are handled
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("has an odd", TextType.BOLD),
            TextNode(" number of ", TextType.NORMAL),
            TextNode("** delimiters", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)
    
    def test_special_characters_in_links(self):
        """Test links with special characters in URL and text"""
        text = "This is a [link with spaces & symbols!](https://example.com/path?query=value&more=stuff)"
        nodes = [TextNode(text, TextType.NORMAL)]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("link with spaces & symbols!", TextType.LINK, "https://example.com/path?query=value&more=stuff"),
        ]
        self.assertEqual(result, expected)
    
    def test_mixed_content_large_example(self):
        """Test a large example with mixed content types"""
        text = """# Markdown Example
        
        This is a paragraph with **bold text**, _italic text_, and `code blocks`.
        
        - Here's a list item with a [link](https://example.com)
        - And another with an ![image](https://example.com/img.jpg)
        
        ```
        def code_block():
            return "This is a multiline code block"
        ```
        
        > This is a blockquote with **formatting** inside it.
        """
        
        # We won't test the entire output since it's large, but we'll make sure it runs without errors
        nodes = text_to_textnodes(text)
        self.assertTrue(len(nodes) > 1)
        
        # Convert to HTML and check that it doesn't raise errors
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        parent = ParentNode("div", html_nodes)
        html = parent.to_html()
        self.assertTrue(len(html) > 0)


if __name__ == "__main__":
    unittest.main()