from typing import Sequence

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    result = None
    match text_node.text_type:
        case TextType.TEXT:
            result = LeafNode(None, text_node.text)
        case TextType.BOLD:
            result = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            result = LeafNode("i", text_node.text)
        case TextType.CODE:
            result = LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Link node must contain url")
            result = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Image node msut cantain a source")
            result = LeafNode("code", "", {"src": text_node.url, "alt": text_node.text})

    if result is None:
        raise ValueError(f"unknown text type: {text_node}")
    return result


def split_nodes_delimiter(old_nodes: Sequence[TextNode], delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text_parts = node.text.split(delimiter)

    return result
