class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
      self.tag = tag  # HTML tag name (e.g., "p", "a", "h1")
      self.value = value  # Value inside the tag (e.g., text)
      self.children = children  # List of HTMLNode children
      self.props = props if props is not None else {}  # Attributes dictionary (e.g., {"href": "..."})

  def __repr__(self):
      """
      Return a string representation of the HTMLNode for debugging purposes.
      
      Returns:
          str: A string showing the node's tag, value, children, and props.
      """
      return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

  def props_to_html(self):
      """
      Convert the node's properties dictionary to an HTML attributes string.
      
      Returns:
          str: A string containing all the HTML attributes, starting with a space
              if there are any attributes, or an empty string otherwise.
      """
      if not self.props:
          return ""
      
      props_list = []
      for prop_key, prop_value in self.props.items():
          props_list.append(f'{prop_key}="{prop_value}"')
      
      return " " + " ".join(props_list)

  def to_html(self):
      raise NotImplementedError("Subclasses must implement to_html()")

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
      """
      Initialize a LeafNode, which is an HTMLNode that cannot have children.
      
      Args:
          tag: HTML tag name (e.g., "p", "a", "h1"). Can be None for raw text.
          value: Required value inside the tag (e.g., text).
          props: Attributes dictionary (e.g., {"href": "..."}). Optional.
      """
      super().__init__(tag=tag, value=value, children=None, props=props)
      
  def to_html(self):
      """
      Convert the LeafNode to its HTML string representation.
      
      Returns:
          str: The HTML representation of this node.
          
      Raises:
          ValueError: If the leaf node has no value.
      """
      if self.value is None:
          raise ValueError("LeafNode must have a value")
          
      if self.tag is None:
          return self.value
          
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



