import pytest

from src.markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    split_nodes_delimiter,
    split_nodes_image,
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
                "This is text with a link [example_one](https://www.example.com)",
                [("example_one", "https://www.example.com")],
            ),
            (
                "This is text with image ![image](https://i.imgur.com/zjjcJKZ.png)",
                [],
            ),
            (
                "This is text with two links [example_one](https://www.example.com), "
                "[example_two](https://www.example.net)",
                [
                    ("example_one", "https://www.example.com"),
                    ("example_two", "https://www.example.net"),
                ],
            ),
        ],
    )
    def test_extract_markdown_links(self, text, expected_matches):
        matches = extract_markdown_links(text)
        assert matches == expected_matches

    @pytest.mark.parametrize(
        "text, result_nodes",
        (
            (
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and "
                "another ![image2](https://i.imgur.com/3elNhQu.png)",
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                ],
            ),
            (
                "![1_image](https://i.imgur.com/zjjcJKZ.png)",
                [TextNode("1_image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            ),
            (
                "[link](https://i.imgur.com/not_empty.png)",
                [TextNode("[link](https://i.imgur.com/not_empty.png)", TextType.TEXT)],
            ),
            ("", []),
        ),
    )
    def test_split_images(self, text, result_nodes):
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert new_nodes == result_nodes

    @pytest.mark.parametrize(
        "nodes, result_nodes",
        (
            (
                [
                    TextNode("![link](https://i.imgur.com/not_empty.png)", TextType.TEXT),
                    TextNode("[link](https://i.imgur.com/not_empty.png)", TextType.TEXT),
                ],
                [
                    TextNode("link", TextType.IMAGE, "https://i.imgur.com/not_empty.png"),
                    TextNode("[link](https://i.imgur.com/not_empty.png)", TextType.TEXT),
                ],
            ),
            (
                [
                    TextNode("some text", TextType.TEXT),
                    TextNode("some text", TextType.TEXT),
                ],
                [
                    TextNode("some text", TextType.TEXT),
                    TextNode("some text", TextType.TEXT),
                ],
            ),
        ),
    )
    def test_split_multiple_nodes(self, nodes, result_nodes):
        new_nodes = split_nodes_image(nodes)
        assert new_nodes == result_nodes


class TestUtils:
    def test_title_extraction(self):
        markdown_with_title = "# This is a Title\n\nSome content here."
        title = extract_title(markdown_with_title)
        assert title == "This is a Title"

    def test_title_extraction_no_title(self):
        markdown_without_title = "No title here, just content."
        with pytest.raises(ValueError, match="No title found in markdown"):
            extract_title(markdown_without_title)
