import unittest
from htmlnode import HTMLNode, LeafNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a_with_props(self):
        """Test an anchor tag with href property."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_to_html_img(self):
        """Test an img tag with properties."""
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image"></img>')
        
    def test_leaf_to_html_span_with_class(self):
        """Test a span with a class attribute."""
        node = LeafNode("span", "Styled text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Styled text</span>')
        
    def test_leaf_to_html_no_tag(self):
        """Test a leaf node with no tag (raw text)."""
        node = LeafNode(None, "Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")
        
    def test_leaf_to_html_no_value(self):
        """Test that a leaf node with no value raises ValueError."""
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_leaf_node_no_children(self):
        """Test that LeafNode doesn't allow children."""
        node = LeafNode("p", "Test")
        self.assertIsNone(node.children)

if __name__ == "__main__":
    unittest.main()