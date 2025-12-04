import pytest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode:
    def test_empty_value(self):
        node = LeafNode("b", "")
        with pytest.raises(ValueError):
            node.to_html()

    @pytest.mark.parametrize(
        "value, tag, props, result",
        (
            ("some text", "b", None, "<b>some text</b>"),
            ("some text", "", None, "some text"),
            (
                "some text",
                "a",
                {"href": "http://example.com"},
                '<a href="http://example.com">some text</a>',
            ),
        ),
    )
    def test_to_html(self, value, tag, props, result):
        node = LeafNode(tag, value, props)
        assert node.to_html() == result


class TestParentNode:
    @pytest.mark.parametrize(
        "node, result",
        (
            (
                ParentNode(
                    "p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]
                ),
                "<p><b>Bold text</b>Normal text</p>",
            ),
            (
                ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold text")])]),
                "<div><p><b>Bold text</b></p></div>",
            ),
        ),
    )
    def test_to_html(self, node, result):
        assert node.to_html() == result

    @pytest.mark.parametrize(
        "node, error_text",
        (
            (
                ParentNode("p", []),
                "ParentNode must have at least one child node",
            ),
            (
                ParentNode("p", None),
                "ParentNode must have at least one child node",
            ),
            (
                ParentNode("", [LeafNode("b", "Bold text")]),
                "ParentNode must have a tag",
            ),
            (
                ParentNode(None, [LeafNode("b", "Bold text")]),
                "ParentNode must have a tag",
            ),
        ),
    )
    def test_invalid_empty_values(self, node, error_text):
        with pytest.raises(ValueError, match=error_text):
            node.to_html()
