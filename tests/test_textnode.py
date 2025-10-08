import pytest

from src.textnode import TextNode, TextType


class TestTextNode:
    @pytest.mark.parametrize(
        "type1, type2",
        [
            [TextType.BOLD, TextType.CODE],
            [TextType.ITALIC, TextType.TEXT],
        ],
    )
    def test_different_types(self, type1, type2):
        common_text = "same text for both"
        node1 = TextNode(common_text, type1)
        node2 = TextNode(common_text, type2)
        assert node1 != node2

    @pytest.mark.parametrize(
        "value1, value2",
        [
            ["text1", "text2"],
            ["same same", "but defferent"],
        ],
    )
    def test_different_values(self, value1, value2):
        node1 = TextNode(value1, TextType.TEXT)
        node2 = TextNode(value2, TextType.TEXT)
        assert node1 != node2
