from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode

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

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()