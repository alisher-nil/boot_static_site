import pytest

from src.markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from src.textnode import TextNode, TextType


class TestSplitNodes:
    def test_convert_function(self):
        node = TextNode(
            "`def main():...` a simple example `return None`",
            text_type=TextType.TEXT,
        )
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(result) == 3

    def test_empty_list(self):
        nodes = split_nodes_delimiter([], "~", TextType.BOLD)
        assert len(nodes) == 0

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        assert len(nodes) == 0

    def test_invalid_string(self):
        node = TextNode("bad code` no opening backtick", TextType.TEXT)
        with pytest.raises(ValueError, match="invalid markdown syntax"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_two_types(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        assert new_nodes == [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]


class TestExtractMarkdown:
    @pytest.mark.parametrize(
        "text, expected_matches",
        [
            (
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                [("image", "https://i.imgur.com/zjjcJKZ.png")],
            ),
            (
                "This is text with link and no image [image](https://i.imgur.com/zjjcJKZ.png)",
                [],
            ),
            (
                "This is text with two images ![image](https://i.imgur.com/zjjcJKZ.png), "
                "![another_image](https://i.imgur.com/zjjcTRU.png)",
                [
                    ("image", "https://i.imgur.com/zjjcJKZ.png"),
                    ("another_image", "https://i.imgur.com/zjjcTRU.png"),
                ],
            ),
        ],
    )
    def test_extract_markdown_images(self, text, expected_matches):
        matches = extract_markdown_images(text)
        assert matches == expected_matches

    @pytest.mark.parametrize(
        "text, expected_matches",
        [
            (
                "This is text with a link [shitsumon](https://www.example.com)",
                [("shitsumon", "https://www.example.com")],
            ),
            (
                "This is text with image ![image](https://i.imgur.com/zjjcJKZ.png)",
                [],
            ),
            (
                "This is text with two links [shitsumon](https://www.example.com), "
                "[mysaly](https://www.example.net)",
                [
                    ("shitsumon", "https://www.example.com"),
                    ("mysaly", "https://www.example.net"),
                ],
            ),
        ],
    )
    def test_extract_markdown_links(self, text, expected_matches):
        matches = extract_markdown_links(text)
        assert matches == expected_matches
