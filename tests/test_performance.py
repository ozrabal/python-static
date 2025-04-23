import unittest
import sys
import os
import time

# Add the current directory to sys.path to make imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.main import text_to_textnodes, text_node_to_html_node
from src.htmlnode import ParentNode


class TestPerformance(unittest.TestCase):
    def test_large_document_performance(self):
        """Test processing performance with a large markdown document"""
        # Create a large markdown document with repeated elements
        large_markdown = ""
        
        # Add 50 paragraphs with various markdown elements
        for i in range(50):
            large_markdown += f"## Heading {i}\n\n"
            large_markdown += f"This is paragraph {i} with **bold text** and _italic text_ and `code`.\n\n"
            large_markdown += f"* List item with [link {i}](https://example.com/{i})\n"
            large_markdown += f"* Another item with ![image {i}](https://example.com/image{i}.jpg)\n\n"
        
        # Measure the time it takes to convert to text nodes
        start_time = time.time()
        nodes = text_to_textnodes(large_markdown)
        text_nodes_time = time.time() - start_time
        
        # Measure the time it takes to convert to HTML nodes
        start_time = time.time()
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        html_nodes_time = time.time() - start_time
        
        # Measure the time it takes to generate HTML
        start_time = time.time()
        parent = ParentNode("div", html_nodes)
        html = parent.to_html()
        html_generation_time = time.time() - start_time
        
        # Print performance information
        print(f"\nPerformance Test Results:")
        print(f"- Document size: {len(large_markdown)} characters")
        print(f"- Text nodes generated: {len(nodes)}")
        print(f"- Text to nodes conversion: {text_nodes_time:.4f} seconds")
        print(f"- Nodes to HTML conversion: {html_nodes_time:.4f} seconds")
        print(f"- HTML generation: {html_generation_time:.4f} seconds")
        print(f"- Total time: {text_nodes_time + html_nodes_time + html_generation_time:.4f} seconds")
        
        # Simple assertions to ensure the test passes while providing useful performance data
        self.assertTrue(len(nodes) > 100)  # Should have generated many nodes
        self.assertTrue(len(html) > 1000)  # Should have generated substantial HTML
    
    def test_many_nested_delimiters(self):
        """Test performance with many nested delimiters"""
        # Create text with many nested delimiters
        nested_text = "Start "
        
        # Add 20 nested bold/italic sections
        for i in range(20):
            nested_text += f"**bold {i} _italic {i}_ still bold** "
        
        start_time = time.time()
        nodes = text_to_textnodes(nested_text)
        processing_time = time.time() - start_time
        
        print(f"\nNested Delimiters Test:")
        print(f"- Processing time: {processing_time:.4f} seconds")
        print(f"- Nodes generated: {len(nodes)}")
        
        # Verify it processed without errors
        self.assertTrue(len(nodes) > 40)  # Should have many nodes from the nested content
    
    def test_repeated_link_patterns(self):
        """Test performance with many links"""
        # Create text with many links
        links_text = ""
        for i in range(100):
            links_text += f"This is link {i}: [Link {i}](https://example.com/{i}) and "
        
        start_time = time.time()
        nodes = text_to_textnodes(links_text)
        processing_time = time.time() - start_time
        
        print(f"\nMany Links Test:")
        print(f"- Processing time: {processing_time:.4f} seconds")
        print(f"- Nodes generated: {len(nodes)}")
        print(f"- Links processed: {sum(1 for node in nodes if node.text_type == node.text_type.LINK)}")
        
        # Verify links were processed correctly
        self.assertEqual(100, sum(1 for node in nodes if node.text_type == node.text_type.LINK))


if __name__ == "__main__":
    unittest.main()