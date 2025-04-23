import unittest
import sys
import os

# Add the parent directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.textnode import TextNode, TextType
from src.main import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        """Test extracting multiple links from text."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        """Test handling text with no link markdown."""
        node = TextNode("This is text with no links", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_link_at_start(self):
        """Test handling link markdown at the start of text."""
        node = TextNode(
            "[starting link](https://example.com) followed by text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("starting link", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        """Test handling link markdown at the end of text."""
        node = TextNode(
            "Text followed by [ending link](https://example.com/end)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.NORMAL),
                TextNode("ending link", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_link_with_empty_text(self):
        """Test handling link with empty text."""
        node = TextNode(
            "Link with no text: [](https://example.com/empty)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with no text: ", TextType.NORMAL),
                TextNode("", TextType.LINK, "https://example.com/empty"),
            ],
            new_nodes,
        )

    def test_link_with_empty_url(self):
        """Test handling link with empty URL."""
        node = TextNode(
            "Link with no URL: [click here]()",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with no URL: ", TextType.NORMAL),
                TextNode("click here", TextType.LINK, ""),
            ],
            new_nodes,
        )

    def test_only_link(self):
        """Test handling node containing only a link."""
        node = TextNode("[standalone link](https://example.com/alone)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("standalone link", TextType.LINK, "https://example.com/alone"),
            ],
            new_nodes,
        )

    def test_multiple_links_no_text(self):
        """Test handling multiple links with no text between them."""
        node = TextNode(
            "[first](https://example.com/first)[second](https://example.com/second)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com/first"),
                TextNode("second", TextType.LINK, "https://example.com/second"),
            ],
            new_nodes,
        )

    def test_skip_non_normal_nodes(self):
        """Test that only NORMAL text nodes get processed."""
        nodes = [
            TextNode("Normal text with [link](https://example.com)", TextType.NORMAL),
            TextNode("Bold text with [link](https://example.com/bold)", TextType.BOLD)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Normal text with ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                # Bold node remains unchanged
                TextNode("Bold text with [link](https://example.com/bold)", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_link_with_special_chars(self):
        """Test handling links with special characters in text."""
        node = TextNode(
            "Link with special chars: [test (1) - title!](https://example.com/special)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with special chars: ", TextType.NORMAL),
                TextNode("test (1) - title!", TextType.LINK, "https://example.com/special"),
            ],
            new_nodes,
        )

    def test_mixed_node_list(self):
        """Test processing a list with mixed node types."""
        nodes = [
            TextNode("Text with [link](https://example.com/link)", TextType.NORMAL),
            TextNode("Image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode("More text with [another](https://example.com/another)", TextType.NORMAL)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com/link"),
                TextNode("Image", TextType.IMAGE, "https://example.com/img.jpg"),  # Unchanged
                TextNode("More text with ", TextType.NORMAL),
                TextNode("another", TextType.LINK, "https://example.com/another"),
            ],
            new_nodes,
        )

    def test_malformed_link_markdown(self):
        """Test handling malformed link markdown."""
        node = TextNode(
            "This has [incomplete link markdown](https://example.com and [another malformed one",
            TextType.NORMAL,
        )
        # Since our function relies on the extraction function, which uses regex,
        # it shouldn't match malformed markdown, so the text should remain unchanged
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_url_with_special_chars(self):
        """Test handling URLs with special characters."""
        node = TextNode(
            "Link with URL params: [my site](https://example.com/page?id=123&format=html)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with URL params: ", TextType.NORMAL),
                TextNode("my site", TextType.LINK, "https://example.com/page?id=123&format=html"),
            ],
            new_nodes,
        )

    def test_adjacent_links_with_text(self):
        """Test handling adjacent links separated by text."""
        node = TextNode(
            "Start [first](https://example.com/first) middle [second](https://example.com/second) end",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.NORMAL),
                TextNode("first", TextType.LINK, "https://example.com/first"),
                TextNode(" middle ", TextType.NORMAL),
                TextNode("second", TextType.LINK, "https://example.com/second"),
                TextNode(" end", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_links_vs_images(self):
        """Test that image markdown isn't processed as links."""
        node = TextNode(
            "This has a ![image](https://example.com/img.jpg) and a [link](https://example.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                # Image markdown should remain unparsed since we're only processing links
                TextNode("This has a ![image](https://example.com/img.jpg) and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_complex_link_scenarios(self):
        """Test complex scenarios with multiple links and special characters."""
        node = TextNode(
            "Check [this](https://example.com) and also [that](https://example.org). [Final link](https://final.com)!",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.NORMAL),
                TextNode("this", TextType.LINK, "https://example.com"),
                TextNode(" and also ", TextType.NORMAL),
                TextNode("that", TextType.LINK, "https://example.org"),
                TextNode(". ", TextType.NORMAL),
                TextNode("Final link", TextType.LINK, "https://final.com"),
                TextNode("!", TextType.NORMAL),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()