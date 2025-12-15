import pytest

from src.markdown_blocks import markdown_to_blocks


class TestMarkdownBlocks:
    @pytest.mark.parametrize(
        "md, expected_result",
        (
            (
                """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            ),
            (
                """
LINE ONE


LINE TWO
""",
                ["LINE ONE", "LINE TWO"],
            ),
        ),
    )
    def test_markdown_to_blocks(self, md, expected_result):
        blocks = markdown_to_blocks(md)
        assert blocks == expected_result
