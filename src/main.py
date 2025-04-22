from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode
import re

def extract_markdown_images(text):
    """
    Extract all markdown images from text and return a list of tuples with (alt_text, url).
    
    Args:
        text (str): The markdown text to analyze
        
    Returns:
        list: A list of tuples in the format [(alt_text, url), ...]
    """
    # Updated pattern to handle square brackets in alt text
    pattern = r"!\[(.*?)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    """
    Extract all markdown links from text and return a list of tuples with (anchor_text, url).
    Uses negative lookbehind to exclude markdown images.
    
    Args:
        text (str): The markdown text to analyze
        
    Returns:
        list: A list of tuples in the format [(anchor_text, url), ...]
    """
    # Updated pattern to handle square brackets in anchor text
    pattern = r"(?<!!)\[(.*?)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode based on its TextType.
    
    Args:
        text_node (TextNode): The TextNode to convert
        
    Returns:
        LeafNode: An HTML node representing the text node
        
    Raises:
        Exception: If the TextNode has an unrecognized TextType
    """
    if text_node.text_type == TextType.NORMAL:
        # For normal text, return a LeafNode with no tag
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        # For bold text, use a "b" tag
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        # For italic text, use an "i" tag
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        # For code text, use a "code" tag
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        # For links, use an "a" tag with href property
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        # For images, use an "img" tag with src and alt properties
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    else:
        raise Exception(f"Invalid TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes by delimiter and apply specified text_type to delimited content.
    
    Args:
        old_nodes (list): List of TextNode objects
        delimiter (str): The delimiter marking text for formatting (e.g., "`", "**", "_")
        text_type (TextType): The TextType to apply to text within delimiters
    
    Returns:
        list: New list of TextNode objects with text split based on delimiters
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process nodes of type NORMAL (we don't want to split already formatted text)
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Check if the delimiter exists in the node's text
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        
        # Process text with delimiters
        remaining_text = old_node.text
        while delimiter in remaining_text:
            # Find the first delimiter position
            start_pos = remaining_text.find(delimiter)
            
            # Add text before the delimiter as a normal node (if any)
            if start_pos > 0:
                new_nodes.append(TextNode(remaining_text[:start_pos], TextType.NORMAL))
            
            # Find the closing delimiter
            end_pos = remaining_text.find(delimiter, start_pos + len(delimiter))
            if end_pos == -1:  # No closing delimiter found
                # Add the rest as a normal node including the opening delimiter
                new_nodes.append(TextNode(remaining_text[start_pos:], TextType.NORMAL))
                remaining_text = ""
                break
            
            # Extract the content between delimiters
            content = remaining_text[start_pos + len(delimiter):end_pos]
            # Add as formatted node with specified text_type
            new_nodes.append(TextNode(content, text_type))
            
            # Update remaining text to continue processing
            remaining_text = remaining_text[end_pos + len(delimiter):]
        
        # Add any remaining text as a normal node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    
    return new_nodes

def split_nodes_image(old_nodes):
    """
    Split TextNodes by markdown image syntax and convert to image nodes.
    
    Args:
        old_nodes (list): List of TextNode objects
    
    Returns:
        list: New list of TextNode objects with images converted to image nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process nodes of type NORMAL (we don't want to split already formatted text)
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Extract all markdown images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images, keep the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process text with images
        remaining_text = old_node.text
        
        for image_alt, image_url in images:
            # Split the text at the image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)
            
            # Add the text before the image as a normal node (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            # Add the image as an image node (if not empty)
            if image_alt or image_url:  # At least one of them should be non-empty
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining text
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Add any remaining text as a normal node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Split TextNodes by markdown link syntax and convert to link nodes.
    
    Args:
        old_nodes (list): List of TextNode objects
    
    Returns:
        list: New list of TextNode objects with links converted to link nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process nodes of type NORMAL (we don't want to split already formatted text)
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Extract all markdown links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links, keep the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process text with links
        remaining_text = old_node.text
        
        for anchor_text, url in links:
            # Split the text at the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            sections = remaining_text.split(link_markdown, 1)
            
            # Add the text before the link as a normal node (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            # Add the link as a link node (if not empty)
            if anchor_text or url:  # At least one of them should be non-empty
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Update remaining text
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        # Add any remaining text as a normal node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    
    return new_nodes

def markdown_to_blocks(markdown):
    """
    Split a markdown string into blocks based on double newlines.
    
    Args:
        markdown (str): The raw markdown string
        
    Returns:
        list: A list of markdown block strings
    """
    # Split the markdown by double newlines
    blocks = markdown.split("\n\n")
    
    # Process each block: strip whitespace and remove empty blocks
    result = []
    for block in blocks:
        # Strip leading and trailing whitespace
        block = block.strip()
        
        # Only add non-empty blocks
        if block:
            result.append(block)
    
    return result

def text_to_textnodes(text):
    """
    Convert markdown text to a list of TextNode objects.
    
    This function processes the following markdown syntax:
    - Bold: **text**
    - Italic: _text_
    - Code: `text`
    - Images: ![alt text](url)
    - Links: [text](url)
    
    Args:
        text (str): Markdown text to convert
        
    Returns:
        list: List of TextNode objects
    """
    # Start with a single TextNode containing the entire text
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Process delimiters for various text formatting
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Process images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()