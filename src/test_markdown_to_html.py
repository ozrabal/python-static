import unittest
import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from main import text_to_textnodes, text_node_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_full_conversion_pipeline(self):
        """Test the full process from markdown text to HTML nodes"""
        # Start with markdown text
        markdown_text = "This is **bold** and _italic_ text with a `code block` and an ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        
        # Convert to text nodes
        text_nodes = text_to_textnodes(markdown_text)
        
        # Convert text nodes to HTML nodes
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        
        # Wrap in a parent node
        parent = ParentNode("div", html_nodes)
        
        # Generate HTML
        html = parent.to_html()
        
        # Expected HTML output
        expected_html = '<div>This is <b>bold</b> and <i>italic</i> text with a <code>code block</code> and an <img src="https://example.com/img.jpg" alt="image"></img> and a <a href="https://example.com">link</a></div>'
        
        self.assertEqual(html, expected_html)
    
    def test_headings_conversion(self):
        """Test converting markdown heading syntax (not implemented yet, but could be added)"""
        # This test is a placeholder for future functionality
        markdown_text = "# Heading 1\n## Heading 2"
        text_nodes = text_to_textnodes(markdown_text)
        
        # Since heading processing isn't implemented yet, this should just be normal text
        expected_nodes = [TextNode("# Heading 1\n## Heading 2", TextType.NORMAL)]
        self.assertEqual(text_nodes, expected_nodes)
    
    def test_complex_nested_content(self):
        """Test a complex example with multiple nested elements"""
        markdown_text = "Start **bold _italic bold_ still bold** end"
        
        # With the current implementation, the formatting won't be properly nested
        # This test documents the current behavior
        text_nodes = text_to_textnodes(markdown_text)
        
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        parent = ParentNode("p", html_nodes)
        html = parent.to_html()
        
        # Current expected behavior (not ideal, but documents how it currently works)
        expected_html = '<p>Start <b>bold _italic bold_ still bold</b> end</p>'
        self.assertEqual(html, expected_html)
    
    def test_empty_input(self):
        """Test converting an empty string"""
        markdown_text = ""
        text_nodes = text_to_textnodes(markdown_text)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        parent = ParentNode("div", html_nodes)
        html = parent.to_html()
        
        expected_html = '<div></div>'
        self.assertEqual(html, expected_html)


if __name__ == "__main__":
    unittest.main()