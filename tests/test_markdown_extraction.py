import unittest
from src.main import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_multiple(self):
        text = "Here are multiple images: ![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/1.png"),
            ("second", "https://example.com/2.png")
        ]
        self.assertListEqual(expected, matches)
        
    def test_extract_markdown_images_none(self):
        text = "This text has no images, just a [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
        
    def test_extract_markdown_images_with_special_characters(self):
        text = "Image with special chars in alt text: ![image with [brackets]](https://example.com/image.png)"
        # Our improved regex now correctly captures text with brackets
        matches = extract_markdown_images(text)
        self.assertListEqual([("image with [brackets]", "https://example.com/image.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
        
    def test_extract_markdown_links_multiple(self):
        text = "Check out [Boot.dev](https://www.boot.dev) and [YouTube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("Boot.dev", "https://www.boot.dev"),
            ("YouTube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)
        
    def test_extract_markdown_links_none(self):
        text = "This text has no links, just an ![image](https://example.com/pic.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
        
    def test_extract_markdown_links_ignore_images(self):
        text = "A ![image link](https://example.com/img.png) and a [text link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("text link", "https://example.com")], matches)
        
    def test_extract_markdown_links_with_special_characters(self):
        text = "Link with special chars: [link with [brackets]](https://example.com)"
        # Our improved regex now correctly captures text with brackets
        matches = extract_markdown_links(text)
        self.assertListEqual([("link with [brackets]", "https://example.com")], matches)
        
    def test_mixed_content(self):
        text = """This is a paragraph with both ![image](https://example.com/img.png) 
                 and [link](https://example.com) in the same text."""
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("image", "https://example.com/img.png")], image_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)


if __name__ == "__main__":
    unittest.main()