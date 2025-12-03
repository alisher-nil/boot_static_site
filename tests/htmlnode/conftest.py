import pytest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


@pytest.fixture
def html_node_props() -> dict:
    return {
        "color": "blue",
        "href": "https://www.google.com",
        "target": "_blank",
    }


@pytest.fixture
def html_node_params(html_node_props) -> dict:
    return {
        "tag": "p",
        "value": "some text",
        "children": [],
        "props": html_node_props,
    }


@pytest.fixture
def html_node(html_node_params) -> HTMLNode:
    return HTMLNode(**html_node_params)


@pytest.fixture
def parent_node() -> ParentNode:
    return ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )


@pytest.fixture
def parent_node_text() -> str:
    return "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
