import unittest
import sys
import os

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        """Test converting heading markdown to HTML nodes."""
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )
    
    def test_headings_with_formatting(self):
        """Test headings with inline formatting."""
        md = """
# Heading with **bold** text

## Heading with _italic_ text

### Heading with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <b>bold</b> text</h1><h2>Heading with <i>italic</i> text</h2><h3>Heading with <code>code</code> text</h3></div>",
        )
    
    def test_unordered_lists(self):
        """Test converting unordered lists to HTML nodes."""
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )
    
    def test_ordered_lists(self):
        """Test converting ordered lists to HTML nodes."""
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )
    
    def test_lists_with_formatting(self):
        """Test lists with inline formatting."""
        md = """
- Item with **bold** text
- Item with _italic_ text
- Item with `code` text

1. Ordered item with **bold**
2. Ordered item with _italic_
3. Ordered item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b> text</li><li>Item with <i>italic</i> text</li><li>Item with <code>code</code> text</li></ul><ol><li>Ordered item with <b>bold</b></li><li>Ordered item with <i>italic</i></li><li>Ordered item with <code>code</code></li></ol></div>",
        )
    
    def test_blockquotes(self):
        """Test converting blockquotes to HTML nodes."""
        md = """
> This is a blockquote
> spanning multiple lines
> in the document
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote spanning multiple lines in the document</blockquote></div>",
        )
    
    def test_blockquotes_with_formatting(self):
        """Test blockquotes with inline formatting."""
        md = """
> Blockquote with **bold** text
> and _italic_ text
> and `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Blockquote with <b>bold</b> text and <i>italic</i> text and <code>code</code> text</blockquote></div>",
        )
    
    def test_links(self):
        """Test converting links to HTML nodes."""
        md = """
This is a paragraph with a [link to example](https://example.com).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with a <a href=\"https://example.com\">link to example</a>.</p></div>",
        )
    
    def test_images(self):
        """Test converting images to HTML nodes."""
        md = """
This is a paragraph with an ![image alt text](https://example.com/image.jpg).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with an <img src=\"https://example.com/image.jpg\" alt=\"image alt text\"></img>.</p></div>",
        )
    
    def test_complex_document(self):
        """Test converting a complex markdown document with multiple elements."""
        md = """
# Document Title

This is a paragraph with **bold** and _italic_ text.

## Section 1

This is a paragraph with a [link](https://example.com) and `code`.

- List item 1
- List item 2 with **bold**
- List item 3 with _italic_

## Section 2

> This is a blockquote
> with multiple lines

```
def example():
    print("This is a code block")
    # With comments
```

1. Ordered item 1
2. Ordered item 2
3. Ordered item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Document Title</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><h2>Section 1</h2><p>This is a paragraph with a <a href=\"https://example.com\">link</a> and <code>code</code>.</p><ul><li>List item 1</li><li>List item 2 with <b>bold</b></li><li>List item 3 with <i>italic</i></li></ul><h2>Section 2</h2><blockquote>This is a blockquote with multiple lines</blockquote><pre><code>def example():\n    print(\"This is a code block\")\n    # With comments\n</code></pre><ol><li>Ordered item 1</li><li>Ordered item 2</li><li>Ordered item 3</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_empty_input(self):
        """Test converting an empty markdown string."""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>",
        )
    
    def test_whitespace_only(self):
        """Test converting a markdown string with only whitespace."""
        md = "   \n  \n  \t  "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>",
        )
    
    def test_code_with_language(self):
        """Test code blocks with language specifier."""
        md = """
```python
def hello_world():
    print("Hello, world!")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>def hello_world():\n    print(\"Hello, world!\")\n</code></pre></div>",
        )
        
    def test_adjacent_blocks(self):
        """Test handling of adjacent blocks of different types."""
        md = """
# Heading 1
Paragraph right after heading without blank line
- List item right after paragraph without blank line
> Blockquote right after list without blank line
```
Code right after blockquote without blank line
```
"""
        # This test checks how the function handles markdown that doesn't have blank lines between blocks.
        # Because there are no blank lines, the parser considers this as a single block
        # and the block_to_block_type function returns BlockType.HEADING for the entire content
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1 Paragraph right after heading without blank line - List item right after paragraph without blank line > Blockquote right after list without blank line <code></code><code> Code right after blockquote without blank line </code><code></code></h1></div>",
        )


if __name__ == "__main__":
    unittest.main()