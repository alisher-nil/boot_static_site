import pytest

from src.htmlnode import HTMLNode


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
