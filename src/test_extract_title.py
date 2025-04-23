import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        """Test extracting a basic title."""
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_with_formatting(self):
        """Test extracting a title that contains markdown formatting."""
        markdown = "# **Bold** and _Italic_ Title"
        self.assertEqual(extract_title(markdown), "**Bold** and _Italic_ Title")
    
    def test_title_with_leading_trailing_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        markdown = "#    Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")
    
    def test_title_in_multiline_markdown(self):
        """Test extracting title from a multiline markdown document."""
        markdown = """
Some text before title

# My Document Title

## Subtitle

Content paragraph.
"""
        self.assertEqual(extract_title(markdown), "My Document Title")
    
    def test_no_title(self):
        """Test that an exception is raised when no title is found."""
        markdown = """
This is a document without a title.

## This is a subtitle
"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        
        self.assertTrue("No h1 header found" in str(context.exception))
    
    def test_not_a_title(self):
        """Test that only lines with a single # are recognized as titles."""
        markdown = """
## Not a title (h2)
### Also not a title (h3)
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_hash_without_space_not_title(self):
        """Test that a line with # but no space is not recognized as a title."""
        markdown = "#Not a proper title"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_second_title_ignored(self):
        """Test that only the first h1 header is extracted."""
        markdown = """
# First Title

Content

# Second Title
"""
        self.assertEqual(extract_title(markdown), "First Title")

if __name__ == "__main__":
    unittest.main()