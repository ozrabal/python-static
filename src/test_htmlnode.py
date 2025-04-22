import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        """Test that props_to_html returns an empty string when there are no props."""
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        """Test that props_to_html correctly formats a single property."""
        node = HTMLNode(tag="a", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
        
    def test_props_to_html_multiple_props(self):
        """Test that props_to_html correctly formats multiple properties."""
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "link-button"
            }
        )
        # The order of properties in a dictionary is not guaranteed,
        # so we check for each property separately
        result = node.props_to_html()
        self.assertTrue(result.startswith(" "))  # Check for leading space
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('class="link-button"', result)
        
    def test_init_default_values(self):
        """Test that HTMLNode initializes with proper default values."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {})
        
    def test_repr_method(self):
        """Test the string representation of HTMLNode."""
        node = HTMLNode(tag="p", value="Hello, world!", props={"class": "greeting"})
        expected = "HTMLNode(tag='p', value='Hello, world!', children=None, props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected)
        
    def test_to_html_not_implemented(self):
        """Test that to_html raises NotImplementedError."""
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()