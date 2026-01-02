import re
from typing import Sequence

from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link
from src.markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from src.textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.UNORDERED_LIST:
                nodes.append(ulist_block_to_html_node(block))
            case BlockType.ORDERED_LIST:
                nodes.append(olist_block_to_html_node(block))
            case BlockType.HEADING:
                nodes.append(heading_block_to_html_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_block_to_html_node(block))
            case BlockType.CODE:
                nodes.append(code_block_to_html_node(block))
            case _:  # Paragraph
                nodes.append(paragraph_block_html_node(block))
    return ParentNode("div", nodes)


def ulist_block_to_html_node(block: str) -> HTMLNode:
    pattern = r"^-\s(?P<value>.*?)$"
    lines = block.split("\n")
    nodes = []
    for line in lines:
        if matches := re.match(pattern, line):
            li_value = matches.group("value")
            nodes.append(ParentNode("li", text_to_html_nodes(li_value)))
        else:
            raise ValueError("Invalid unordered list format")
    return ParentNode("ul", nodes)


def olist_block_to_html_node(block: str) -> HTMLNode:
    pattern = r"^\d\.+?\s(?P<value>.*?)$"
    lines = block.split("\n")
    nodes = []
    for line in lines:
        if matches := re.match(pattern, line):
            li_value = matches.group("value")
            nodes.append(ParentNode("li", text_to_html_nodes(li_value)))
        else:
            raise ValueError("Invalid ordered list format")
    return ParentNode("ol", nodes)


def heading_block_to_html_node(block: str) -> HTMLNode:
    pattern = r"^(?P<heading_level>#{1,6})\s(?P<value>.*)$"
    if matches := re.match(pattern, block):
        level = len(matches.group("heading_level"))
        value = matches.group("value")
        return ParentNode(f"h{level}", text_to_html_nodes(value))
    else:
        raise ValueError("Invalid heading block format")


def quote_block_to_html_node(block: str) -> HTMLNode:
    pattern = r"^>\s?(?P<value>.*?)$"
    lines = block.split("\n")
    nodes = []
    for line in lines:
        if matches := re.match(pattern, line):
            value = matches.group("value")
            if value:
                nodes.append(ParentNode(None, text_to_html_nodes(value)))
        else:
            raise ValueError("Invalid quote block format")
    return ParentNode("blockquote", nodes)


def code_block_to_html_node(block: str) -> HTMLNode:
    pattern = r"^```(?P<code>[\s\S]*?)```$"
    nodes = []
    if matches := re.match(pattern, block):
        code = matches.group("code").lstrip()
        nodes.append(LeafNode("code", code))
    else:
        raise ValueError("Invalid code block format")

    return ParentNode("pre", nodes)


def paragraph_block_html_node(block: str) -> HTMLNode:
    return ParentNode("p", text_to_html_nodes(block))


def text_to_html_nodes(text: str) -> Sequence[HTMLNode]:
    text_nodes = text_to_text_nodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def text_to_text_nodes(text: str) -> Sequence[TextNode]:
    clean_text = " ".join(text.split("\n"))
    nodes = [TextNode(clean_text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
