import unittest
import sys
import os

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.textnode import TextNode, TextType
from src.main import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        """Test extracting multiple images from text."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        """Test handling text with no image markdown."""
        node = TextNode("This is text with no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_image_at_start(self):
        """Test handling image markdown at the start of text."""
        node = TextNode(
            "![starting image](https://example.com/img.jpg) followed by text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("starting image", TextType.IMAGE, "https://example.com/img.jpg"),
                TextNode(" followed by text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        """Test handling image markdown at the end of text."""
        node = TextNode(
            "Text followed by ![ending image](https://example.com/end.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.NORMAL),
                TextNode("ending image", TextType.IMAGE, "https://example.com/end.jpg"),
            ],
            new_nodes,
        )

    def test_image_with_empty_alt_text(self):
        """Test handling image with empty alt text."""
        node = TextNode(
            "Image with no alt text: ![](https://example.com/noalt.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with no alt text: ", TextType.NORMAL),
                TextNode("", TextType.IMAGE, "https://example.com/noalt.jpg"),
            ],
            new_nodes,
        )

    def test_image_with_empty_url(self):
        """Test handling image with empty URL."""
        node = TextNode(
            "Image with no URL: ![alt text]()",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with no URL: ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, ""),
            ],
            new_nodes,
        )

    def test_only_image(self):
        """Test handling node containing only an image."""
        node = TextNode("![standalone image](https://example.com/alone.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("standalone image", TextType.IMAGE, "https://example.com/alone.jpg"),
            ],
            new_nodes,
        )

    def test_multiple_images_no_text(self):
        """Test handling multiple images with no text between them."""
        node = TextNode(
            "![first](https://example.com/first.jpg)![second](https://example.com/second.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
                TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
            ],
            new_nodes,
        )

    def test_skip_non_normal_nodes(self):
        """Test that only NORMAL text nodes get processed."""
        nodes = [
            TextNode("Normal text with ![image](https://example.com/img.jpg)", TextType.NORMAL),
            TextNode("Bold text with ![image](https://example.com/bold.jpg)", TextType.BOLD)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Normal text with ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
                # Bold node remains unchanged
                TextNode("Bold text with ![image](https://example.com/bold.jpg)", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_complex_image_alt_text(self):
        """Test handling images with complex alt text containing special characters."""
        node = TextNode(
            "Image with special chars: ![img (1) - title!](https://example.com/special.jpg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with special chars: ", TextType.NORMAL),
                TextNode("img (1) - title!", TextType.IMAGE, "https://example.com/special.jpg"),
            ],
            new_nodes,
        )

    def test_mixed_node_list(self):
        """Test processing a list with mixed node types."""
        nodes = [
            TextNode("Text with ![img](https://example.com/img.jpg)", TextType.NORMAL),
            TextNode("Link", TextType.LINK, "https://example.com"),
            TextNode("More text with ![another](https://example.com/another.jpg)", TextType.NORMAL)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.NORMAL),
                TextNode("img", TextType.IMAGE, "https://example.com/img.jpg"),
                TextNode("Link", TextType.LINK, "https://example.com"),  # Unchanged
                TextNode("More text with ", TextType.NORMAL),
                TextNode("another", TextType.IMAGE, "https://example.com/another.jpg"),
            ],
            new_nodes,
        )

    def test_malformed_image_markdown(self):
        """Test handling malformed image markdown."""
        node = TextNode(
            "This has ![incomplete image markdown](https://example.com and ![another malformed one",
            TextType.NORMAL,
        )
        # Since our function relies on the extraction function, which uses regex,
        # it shouldn't match malformed markdown, so the text should remain unchanged
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_url_with_special_chars(self):
        """Test handling URLs with special characters."""
        node = TextNode(
            "Image with URL params: ![image](https://example.com/img.jpg?size=large&format=png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with URL params: ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg?size=large&format=png"),
            ],
            new_nodes,
        )

    def test_adjacent_images_with_text(self):
        """Test handling adjacent images separated by text."""
        node = TextNode(
            "Start ![first](https://example.com/first.jpg) middle ![second](https://example.com/second.jpg) end",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.NORMAL),
                TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
                TextNode(" middle ", TextType.NORMAL),
                TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
                TextNode(" end", TextType.NORMAL),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()