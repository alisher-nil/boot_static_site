import pytest

from src.textnode import TextNode, TextType


@pytest.fixture
def bold_text_node():
    return TextNode("This is a text node", TextType.BOLD)


@pytest.fixture
def italic_text_node():
    return TextNode("This is a text node", TextType.ITALIC)
