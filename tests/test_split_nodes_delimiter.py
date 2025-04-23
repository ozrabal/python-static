import unittest
import sys
import os

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.textnode import TextNode, TextType
from src.main import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter_single(self):
        """Test splitting a single backtick-delimited code block."""
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_delimiter_single(self):
        """Test splitting a single bold text marked with double asterisks."""
        node = TextNode("This text has **bold** formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This text has ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" formatting", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_delimiter_single(self):
        """Test splitting a single italic text marked with underscores."""
        node = TextNode("This text has _italic_ formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This text has ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" formatting", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters_same_type(self):
        """Test handling multiple instances of the same delimiter type."""
        node = TextNode("Text with `code one` and `code two` blocks", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("code one", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code two", TextType.CODE),
            TextNode(" blocks", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start(self):
        """Test handling when delimiter appears at the start of the text."""
        node = TextNode("`code block` at the beginning", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" at the beginning", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        """Test handling when delimiter appears at the end of the text."""
        node = TextNode("Code at the end `code block`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Code at the end ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_delimiter_content(self):
        """Test handling empty content between delimiters."""
        node = TextNode("Empty code block: ``", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Empty code block: ", TextType.NORMAL),
            TextNode("", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_missing_closing_delimiter(self):
        """Test handling when closing delimiter is missing."""
        node = TextNode("Unclosed `code block", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Our implementation splits at the delimiter
        expected = [
            TextNode("Unclosed ", TextType.NORMAL),
            TextNode("`code block", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_missing_opening_delimiter(self):
        """Test handling when there's a potential closing delimiter without an opening one."""
        node = TextNode("Just text with a single backtick at end`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Our implementation handles this by splitting at the backtick
        expected = [
            TextNode("Just text with a single backtick at end", TextType.NORMAL),
            TextNode("`", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_sequential_processing(self):
        """Test processing text with multiple types of formatting in sequence."""
        node = TextNode("Text with `code` and **bold** formatting", TextType.NORMAL)
        
        # Process code first
        code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Then process bold on the result
        final_nodes = split_nodes_delimiter(code_nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" formatting", TextType.NORMAL),
        ]
        self.assertEqual(final_nodes, expected)
    
    def test_skip_non_normal_nodes(self):
        """Test that only NORMAL text nodes get processed."""
        nodes = [
            TextNode("Normal text `with code`", TextType.NORMAL),
            TextNode("Already bold text `with code`", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("Normal text ", TextType.NORMAL),
            TextNode("with code", TextType.CODE),
            TextNode("Already bold text `with code`", TextType.BOLD)  # This node remains unchanged
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_mixed_node_list(self):
        """Test processing a list with mixed node types."""
        nodes = [
            TextNode("First `code` block", TextType.NORMAL),
            TextNode("Link", TextType.LINK, "https://example.com"),
            TextNode("Second `code` block", TextType.NORMAL)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("First ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.NORMAL),
            TextNode("Link", TextType.LINK, "https://example.com"),  # Unchanged
            TextNode("Second ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.NORMAL)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiter_types_in_sequence(self):
        """Test applying different delimiters in sequence."""
        text = "Text with `code`, **bold** and _italic_ formatting"
        node = TextNode(text, TextType.NORMAL)
        
        # Apply code formatting first
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Then apply bold formatting
        nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        
        # Finally apply italic formatting
        final_nodes = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)
        
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" formatting", TextType.NORMAL)
        ]
        self.assertEqual(final_nodes, expected)


if __name__ == "__main__":
    unittest.main()