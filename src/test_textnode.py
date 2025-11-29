import pytest
from pytest_lazy_fixtures import lf

from textnode import TextNode, TextType


class TestTextNode:
    def test_empty_url_init(self):
        node = TextNode("text", TextType.BOLD)
        assert node.url is None

    @pytest.mark.parametrize(
        "node1, node2, expected_result",
        [
            (lf("bold_text_node"), lf("same_bold_text_node"), True),
            (lf("bold_text_node"), lf("different_bold_text_node"), False),
            (lf("bold_text_node"), lf("italic_text_node"), False),
        ],
    )
    def test_eq(self, node1, node2, expected_result):
        assert (node1 == node2) == expected_result

    @pytest.mark.parametrize(
        "node, params",
        (
            (lf("bold_text_node"), lf("bold_text_params")),
            (lf("italic_text_node"), lf("italic_text_params")),
        ),
    )
    def test_str(self, node, params):
        text = params.get("text")
        text_type = params.get("text_type")
        url = params.get("url")

        expected_string = f"TextNode({text}, {text_type.value}, {url})"
        assert str(node) == expected_string
