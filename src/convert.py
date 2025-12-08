from typing import Sequence

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
            raise ValueError("invalid markdown syntax")

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
