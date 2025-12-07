from typing import Sequence

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: Sequence[TextNode],
    delimiter: str,
    text_type: TextType,
) -> Sequence[TextNode]: ...
