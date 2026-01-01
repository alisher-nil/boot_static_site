import re
from typing import Callable, Sequence

from .textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: Sequence[TextNode],
    delimiter: str,
    text_type: TextType,
) -> Sequence[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        new_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(
                "invalid markdown syntax, either opening or closing "
                f"delimeter ({delimiter}) is missing"
            )

        for i in range(len(parts)):
            part = parts[i]
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

        result.extend(new_nodes)
    return result


def split_nodes_image(old_nodes: Sequence[TextNode]) -> list[TextNode]:
    markdown_template = "![{text}]({url})"
    return split_media_nodes(old_nodes, markdown_template, extract_markdown_images)


def split_nodes_link(old_nodes: Sequence[TextNode]) -> list[TextNode]:
    markdown_template = "[{text}]({url})"
    return split_media_nodes(old_nodes, markdown_template, extract_markdown_links)


def split_media_nodes(
    old_nodes: Sequence[TextNode],
    markdown_template: str,
    extractor: Callable,
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if not node.text:
            continue
        text_url_pairs = extractor(node.text)
        if not text_url_pairs:
            result.append(node)
            continue
        text_to_split = node.text
        for text, url in text_url_pairs:
            separator = markdown_template.format(text=text, url=url)
            sections = text_to_split.split(separator, 1)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(text, TextType.IMAGE, url))
            text_to_split = sections[1]
    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    pairs = re.findall(pattern, text)
    return pairs


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    pairs = re.findall(pattern, text)
    return pairs


def extract_title(markdown: str):
    pattern = r"^#\s(?P<title>.*?)$"
    if matches := re.match(pattern, markdown, re.MULTILINE):
        title = matches.group("title")
        return title
    else:
        raise ValueError("No title found in markdown")
