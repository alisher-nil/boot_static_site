import pytest

from textnode import TextNode, TextType


@pytest.fixture
def bold_text_params():
    return {"text": "This is a text node", "text_type": TextType.BOLD}


@pytest.fixture
def italic_text_params():
    return {"text": "This is a text node", "text_type": TextType.ITALIC}


@pytest.fixture
def bold_text_node(bold_text_params):
    return TextNode(**bold_text_params)


@pytest.fixture
def same_bold_text_node(bold_text_params):
    return TextNode(**bold_text_params)


@pytest.fixture
def different_bold_text_node():
    return TextNode("completely different text", TextType.BOLD)


@pytest.fixture
def italic_text_node(italic_text_params):
    return TextNode(**italic_text_params)
