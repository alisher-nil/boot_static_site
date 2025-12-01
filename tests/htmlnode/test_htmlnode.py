import pytest

from src.htmlnode import HTMLNode


class TestHTMLNode:
    @pytest.mark.parametrize(
        "missing_param",
        ("tag", "value", "children", "props"),
    )
    def test_default_values(self, missing_param, html_node_params):
        html_node_params.pop(missing_param)
        node = HTMLNode(**html_node_params)
        assert getattr(node, missing_param, False) is None

    def test_to_html_not_implemented(self, html_node: HTMLNode):
        with pytest.raises(NotImplementedError):
            html_node.to_html()

    def test_props_to_html(self, html_node: HTMLNode, html_node_props: dict):
        parts = []
        for key, value in html_node_props.items():
            parts.append(f' {key}="{value}"')
        assert html_node.props_to_html() == "".join(parts)
