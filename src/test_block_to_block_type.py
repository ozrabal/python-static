import unittest
from main import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        # Simple paragraph
        self.assertEqual(
            block_to_block_type("This is a simple paragraph."),
            BlockType.PARAGRAPH
        )
        
        # Multi-line paragraph
        self.assertEqual(
            block_to_block_type("This is a multi-line\nparagraph with content."),
            BlockType.PARAGRAPH
        )
        
        # Paragraph with markdown formatting
        self.assertEqual(
            block_to_block_type("Paragraph with **bold** and _italic_ text."),
            BlockType.PARAGRAPH
        )
        
        # Paragraph with links and images
        self.assertEqual(
            block_to_block_type("Paragraph with [link](https://example.com) and ![image](image.jpg)."),
            BlockType.PARAGRAPH
        )

    def test_headings(self):
        # H1 heading
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING
        )
        
        # H2 heading
        self.assertEqual(
            block_to_block_type("## Heading 2"),
            BlockType.HEADING
        )
        
        # H3 heading
        self.assertEqual(
            block_to_block_type("### Heading 3"),
            BlockType.HEADING
        )
        
        # H4 heading
        self.assertEqual(
            block_to_block_type("#### Heading 4"),
            BlockType.HEADING
        )
        
        # H5 heading
        self.assertEqual(
            block_to_block_type("##### Heading 5"),
            BlockType.HEADING
        )
        
        # H6 heading
        self.assertEqual(
            block_to_block_type("###### Heading 6"),
            BlockType.HEADING
        )
        
        # Heading with formatting
        self.assertEqual(
            block_to_block_type("## Heading with **bold** text"),
            BlockType.HEADING
        )
        
        # Invalid heading (7 #'s should be a paragraph)
        self.assertEqual(
            block_to_block_type("####### Not a heading"),
            BlockType.PARAGRAPH
        )
        
        # Invalid heading (no space after #)
        self.assertEqual(
            block_to_block_type("#Not a heading"),
            BlockType.PARAGRAPH
        )

    def test_code_blocks(self):
        # Simple code block
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE
        )
        
        # Code block with language specifier
        self.assertEqual(
            block_to_block_type("```python\ndef hello():\n    print('Hello world!')\n```"),
            BlockType.CODE
        )
        
        # Empty code block
        self.assertEqual(
            block_to_block_type("```\n```"),
            BlockType.CODE
        )
        
        # Code block with backticks in content
        self.assertEqual(
            block_to_block_type("```\nInline `code` within a block\n```"),
            BlockType.CODE
        )
        
        # Invalid code block (only starting backticks)
        self.assertEqual(
            block_to_block_type("```\nCode without closing backticks"),
            BlockType.PARAGRAPH
        )
        
        # Invalid code block (only ending backticks)
        self.assertEqual(
            block_to_block_type("Code without opening backticks\n```"),
            BlockType.PARAGRAPH
        )

    def test_quote_blocks(self):
        # Simple quote
        self.assertEqual(
            block_to_block_type("> This is a quote"),
            BlockType.QUOTE
        )
        
        # Multi-line quote
        self.assertEqual(
            block_to_block_type("> Line 1 of the quote\n> Line 2 of the quote"),
            BlockType.QUOTE
        )
        
        # Quote with formatting
        self.assertEqual(
            block_to_block_type("> Quote with **bold** and _italic_"),
            BlockType.QUOTE
        )
        
        # Invalid quote (mixed lines)
        self.assertEqual(
            block_to_block_type("> Quote line\nNot a quote line"),
            BlockType.PARAGRAPH
        )
        
        # Invalid quote (space before >)
        self.assertEqual(
            block_to_block_type(" > Not a valid quote block"),
            BlockType.PARAGRAPH
        )
        
        # Quote with links and images
        self.assertEqual(
            block_to_block_type("> Quote with [link](https://example.com)"),
            BlockType.QUOTE
        )

    def test_unordered_lists(self):
        # Simple unordered list
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2\n- Item 3"),
            BlockType.UNORDERED_LIST
        )
        
        # Unordered list with single item
        self.assertEqual(
            block_to_block_type("- Single item"),
            BlockType.UNORDERED_LIST
        )
        
        # Unordered list with formatting
        self.assertEqual(
            block_to_block_type("- Item with **bold**\n- Item with _italic_"),
            BlockType.UNORDERED_LIST
        )
        
        # Invalid unordered list (missing space after -)
        self.assertEqual(
            block_to_block_type("-Item without space"),
            BlockType.PARAGRAPH
        )
        
        # Invalid unordered list (mixed with other content)
        self.assertEqual(
            block_to_block_type("- Item 1\nNot a list item"),
            BlockType.PARAGRAPH
        )
        
        # Unordered list with nested content (should still be identified as list)
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item with [link](https://example.com)"),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_lists(self):
        # Simple ordered list
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"),
            BlockType.ORDERED_LIST
        )
        
        # Ordered list with single item
        self.assertEqual(
            block_to_block_type("1. Single item"),
            BlockType.ORDERED_LIST
        )
        
        # Ordered list with formatting
        self.assertEqual(
            block_to_block_type("1. Item with **bold**\n2. Item with _italic_"),
            BlockType.ORDERED_LIST
        )
        
        # Invalid ordered list (wrong numbering)
        self.assertEqual(
            block_to_block_type("1. Item 1\n3. Item 3"),
            BlockType.PARAGRAPH
        )
        
        # Invalid ordered list (not starting from 1)
        self.assertEqual(
            block_to_block_type("2. Item 2\n3. Item 3"),
            BlockType.PARAGRAPH
        )
        
        # Invalid ordered list (missing space after period)
        self.assertEqual(
            block_to_block_type("1.Item without space"),
            BlockType.PARAGRAPH
        )
        
        # Invalid ordered list (mixed with other content)
        self.assertEqual(
            block_to_block_type("1. Item 1\nNot a list item"),
            BlockType.PARAGRAPH
        )
        
        # Valid ordered list with multiple digits
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4\n5. Item 5\n6. Item 6\n7. Item 7\n8. Item 8\n9. Item 9\n10. Item 10"),
            BlockType.ORDERED_LIST
        )

    def test_edge_cases(self):
        # Empty string defaults to paragraph
        self.assertEqual(
            block_to_block_type(""),
            BlockType.PARAGRAPH
        )
        
        # Special characters
        self.assertEqual(
            block_to_block_type("!@#$%^&*()"),
            BlockType.PARAGRAPH
        )
        
        # Numeric content
        self.assertEqual(
            block_to_block_type("12345"),
            BlockType.PARAGRAPH
        )
        
        # Only whitespace (though this should be stripped before calling the function)
        self.assertEqual(
            block_to_block_type("   "),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()