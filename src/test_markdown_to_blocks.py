import unittest
import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_empty_markdown(self):
        """Test that empty markdown returns an empty list."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_only_whitespace(self):
        """Test that markdown containing only whitespace returns an empty list."""
        md = "   \n\n   \t\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_single_block(self):
        """Test markdown with a single block."""
        md = "This is a single paragraph block."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph block."])
    
    def test_multiple_newlines(self):
        """Test markdown with excessive newlines between blocks."""
        md = """First paragraph


Second paragraph



Third paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph"
            ],
        )
    
    def test_headings_and_lists(self):
        """Test markdown with headings and lists."""
        md = """# Heading 1

## Heading 2

- List item 1
- List item 2
  - Nested item

Paragraph after list."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "- List item 1\n- List item 2\n  - Nested item",
                "Paragraph after list."
            ],
        )
    
    def test_code_blocks(self):
        """Test markdown with fenced code blocks."""
        md = """Regular paragraph

```python
def hello_world():
    print("Hello, world!")
```

Another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph",
                "```python\ndef hello_world():\n    print(\"Hello, world!\")\n```",
                "Another paragraph"
            ],
        )
    
    def test_block_quotes(self):
        """Test markdown with block quotes."""
        md = """This is a paragraph

> This is a block quote
> It spans multiple lines
> Within the same block

This is another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "> This is a block quote\n> It spans multiple lines\n> Within the same block",
                "This is another paragraph"
            ],
        )
    
    def test_whitespace_between_blocks(self):
        """Test markdown with whitespace around blocks that should be stripped."""
        md = """   First paragraph with leading spaces   

   Second paragraph with leading spaces and trailing spaces   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with leading spaces",
                "Second paragraph with leading spaces and trailing spaces"
            ],
        )
    
    def test_tables(self):
        """Test markdown with tables."""
        md = """This is a paragraph

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |

Another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n| Cell 3   | Cell 4   |",
                "Another paragraph"
            ],
        )


if __name__ == "__main__":
    unittest.main()