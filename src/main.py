from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode, ParentNode
import re
from enum import Enum
from copy_static import copy_static_to_public

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block (str): A block of markdown text (with leading/trailing whitespace already stripped)
        
    Returns:
        BlockType: The type of the markdown block
    """
    # Check for heading (starts with 1-6 # characters, followed by a space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
        
    # Check for code block (starts with 3 backticks and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by a space)
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    # - Every line must start with a number followed by a . and a space
    # - Numbers must start at 1 and increment by 1 for each line
    is_ordered_list = True
    for i, line in enumerate(lines):
        if not re.match(f"^{i+1}\\. ", line):
            is_ordered_list = False
            break
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    # If none of the above conditions match, it's a paragraph
    return BlockType.PARAGRAPH

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

def extract_title(markdown):
    """
    Extract the h1 header from a markdown string.
    
    Args:
        markdown (str): The markdown string to extract the title from
        
    Returns:
        str: The title text (without the # and leading/trailing whitespace)
        
    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split("\n")
    
    for line in lines:
        # Check for a line that starts with a single # followed by a space
        if line.strip().startswith("# "):
            # Return the title without the # and any leading/trailing whitespace
            return line.strip()[2:].strip()
    
    # If no h1 header is found, raise an exception
    raise Exception("No h1 header found in the markdown")

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path (str): Path to the source markdown file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the output HTML file should be written
    """
    import os
    
    # Print informative message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, "r") as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the output file
    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_root=None):
    """
    Recursively crawl through content directory and generate HTML pages for all markdown files.
    
    Args:
        dir_path_content (str): Path to the content directory to crawl
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory where HTML files will be written
        content_root (str, optional): The root content directory path for relative path calculation
    """
    import os
    
    # If this is the initial call, set content_root to the current directory
    if content_root is None:
        content_root = dir_path_content
    
    # Print informative message
    print(f"Crawling directory: {dir_path_content}")
    
    # List all entries in the directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        # If the entry is a directory, recursively process it
        if os.path.isdir(entry_path):
            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, dest_dir_path, content_root)
            
        # If the entry is a markdown file, generate an HTML page
        elif entry.endswith(".md"):
            # Get the relative path from the content root directory
            rel_path = os.path.relpath(os.path.dirname(entry_path), content_root)
            
            # Create output filename (replace .md with .html)
            output_filename = entry.replace(".md", ".html")
            
            # Handle index.md files specially
            if output_filename == "index.html":
                # For index.md files, put in the corresponding directory
                if rel_path == '.':  # If it's in the root content dir
                    output_path = os.path.join(dest_dir_path, output_filename)
                else:  # If it's in a subdirectory
                    output_dir = os.path.join(dest_dir_path, rel_path)
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, output_filename)
            else:
                # For non-index files, create a directory with the same name and use index.html inside
                base_name = output_filename.replace(".html", "")
                if rel_path == '.':  # If it's in the root content dir
                    output_dir = os.path.join(dest_dir_path, base_name)
                else:  # If it's in a subdirectory
                    output_dir = os.path.join(dest_dir_path, rel_path, base_name)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, "index.html")
            
            # Generate the HTML file
            generate_page(entry_path, template_path, output_path)
            
    print(f"Finished processing directory: {dir_path_content}")

def text_to_children(text):
    """
    Convert markdown text to a list of HTMLNode objects.
    
    Args:
        text (str): The markdown text to convert
        
    Returns:
        list: A list of HTMLNode objects
    """
    # First convert to TextNodes
    nodes = text_to_textnodes(text)
    
    # Then convert each TextNode to an HTMLNode
    return [text_node_to_html_node(node) for node in nodes]

def extract_heading_level(block):
    """
    Extract the heading level from a heading block.
    
    Args:
        block (str): A markdown heading block
        
    Returns:
        int: The heading level (1-6)
    """
    # Count the number of # characters at the start
    match = re.match(r"^(#{1,6})\s", block)
    if match:
        return len(match.group(1))
    return 1  # Default to h1 if pattern doesn't match

def process_list_items(block, is_ordered=False):
    """
    Process list items and return them as HTMLNode objects.
    
    Args:
        block (str): A markdown list block
        is_ordered (bool): Whether this is an ordered list
        
    Returns:
        list: A list of HTMLNode objects representing list items
    """
    lines = block.split("\n")
    item_nodes = []
    
    for line in lines:
        # Remove the list marker
        if is_ordered:
            # For ordered lists, remove numbers and period
            content = re.sub(r"^\d+\.\s+", "", line)
        else:
            # For unordered lists, remove "- "
            content = line[2:] if line.startswith("- ") else line
        
        # Convert the content to HTML nodes
        item_children = text_to_children(content)
        
        # Create a list item node
        item_node = ParentNode("li", item_children)
        item_nodes.append(item_node)
    
    return item_nodes

def process_quote_content(block):
    """
    Process quote content by removing the '>' prefix from each line.
    
    Args:
        block (str): A markdown quote block
        
    Returns:
        str: The quote content without '>' prefixes
    """
    lines = block.split("\n")
    # Remove '>' from the start of each line and join with spaces (not newlines)
    return " ".join([line[1:].lstrip() if line.startswith(">") else line for line in lines])

def markdown_to_html_node(markdown):
    """
    Convert a markdown string to an HTML node.
    
    Args:
        markdown (str): The markdown string to convert
        
    Returns:
        ParentNode: The root HTML node containing the converted markdown
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Store all the block nodes
    block_nodes = []
    
    # Process each block
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            # Create paragraph node with inline markdown parsed
            # Replace newlines with spaces for proper paragraph rendering
            block = block.replace("\n", " ")
            children = text_to_children(block)
            block_nodes.append(ParentNode("p", children))
            
        elif block_type == BlockType.HEADING:
            # Get heading level (h1-h6)
            level = extract_heading_level(block)
            
            # Remove the heading markers and parse the content
            # Also replace newlines with spaces
            content = re.sub(r"^#{1,6}\s+", "", block).replace("\n", " ")
            children = text_to_children(content)
            
            # Create heading node
            block_nodes.append(ParentNode(f"h{level}", children))
            
        elif block_type == BlockType.CODE:
            # For code blocks, don't parse inline markdown
            # Remove the code block markers but preserve internal newlines
            if block.startswith("```") and block.endswith("```"):
                # Get the content between the opening ``` and closing ```
                # First, remove the opening line (which may contain a language specifier)
                start_idx = block.find("\n") + 1
                # Then, remove the closing ```
                end_idx = block.rfind("```")
                
                # Extract content, preserving newlines and ensuring it ends with a newline
                # as expected by the tests
                code_content = block[start_idx:end_idx]
                
                # Create a text node and convert it directly without parsing markdown
                code_node = TextNode(code_content, TextType.NORMAL)
                code_html = text_node_to_html_node(code_node)
                
                # Wrap in <pre><code>
                block_nodes.append(ParentNode("pre", [ParentNode("code", [code_html])]))
            
        elif block_type == BlockType.QUOTE:
            # Process quote content, joining lines with spaces instead of preserving newlines
            quote_content = process_quote_content(block)
            
            # Parse inline markdown inside the quote
            children = text_to_children(quote_content)
            
            # Create blockquote node
            block_nodes.append(ParentNode("blockquote", children))
            
        elif block_type == BlockType.UNORDERED_LIST:
            # Process unordered list items
            item_nodes = process_list_items(block, is_ordered=False)
            
            # Create unordered list node
            block_nodes.append(ParentNode("ul", item_nodes))
            
        elif block_type == BlockType.ORDERED_LIST:
            # Process ordered list items
            item_nodes = process_list_items(block, is_ordered=True)
            
            # Create ordered list node
            block_nodes.append(ParentNode("ol", item_nodes))
    
    # Create a parent div node containing all block nodes
    return ParentNode("div", block_nodes)

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
    import os
    
    # Get the paths relative to the current file location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Define paths for various files and directories
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    # Step 1: Delete anything in the public directory and copy static files
    print("Copying static files to public directory...")
    copy_static_to_public(static_dir, public_dir)
    
    # Step 2: Generate HTML pages from markdown recursively
    print("Generating HTML pages from markdown...")
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("Static site generation completed successfully!")

if __name__ == "__main__":
    main()