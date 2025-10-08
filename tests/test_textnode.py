import pytest

from src.textnode import TextNode, TextType


class TestTextNode:
    @pytest.mark.parametrize(
        "type1, type2",
        [
            [TextType.BOLD, TextType.CODE],
            [TextType.BOLD, TextType.TEXT],
        ],
    )
    def test_different_types(self, type1, type2):
        common_text = "same text for both"
        node1 = TextNode(common_text, type1)
        node2 = TextNode(common_text, type2)
        assert node1 != node2
