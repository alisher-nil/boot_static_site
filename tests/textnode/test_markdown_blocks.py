import pytest

from src.markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownBlocks:
    test_cases = [
        (
            (
                "**bold** text\n"
                "\n"
                "_italic_ text and `code` text\n"
                "same paragraph\n"
                "\n"
                "- list item 1\n"
                "- list item 2\n"
            ),
            [
                "**bold** text",
                ("_italic_ text and `code` text\nsame paragraph"),
                "- list item 1\n- list item 2",
            ],
        ),
        (
            ("LINE ONE\n\nLINE TWO "),
            ["LINE ONE", "LINE TWO"],
        ),
    ]

    @pytest.mark.parametrize("md, expected_result", test_cases)
    def test_markdown_to_blocks(self, md, expected_result):
        blocks = markdown_to_blocks(md)
        assert blocks == expected_result


class TestMarkdownToBlockTypes:
    simple_test_cases = [
        ("This is a simple paragraph.", BlockType.PARAGRAPH),
        ("# This is a heading", BlockType.HEADING),
        ("```\ncode block\n```", BlockType.CODE),
        ("```code line```", BlockType.CODE),
        ("> This is a quote.", BlockType.QUOTE),
        ("- Item 1", BlockType.UNORDERED_LIST),
        ("1. First item", BlockType.ORDERED_LIST),
    ]
    multiline_test_cases = [
        (
            "> This is a blockquote.\n> It spans multiple lines.",
            BlockType.QUOTE,
        ),
        (
            "```\ndef hello_world():\n    print('Hello, world!')\n```",
            BlockType.CODE,
        ),
        (
            "- Item 1\n- Item 2\n- Item 3",
            BlockType.UNORDERED_LIST,
        ),
        (
            "1. First item\n2. Second item\n3. Third item",
            BlockType.ORDERED_LIST,
        ),
        (
            "2. First item\n3. Second item\n4. Third item",
            BlockType.PARAGRAPH,
        ),
    ]

    @pytest.mark.parametrize("md, expected_type", simple_test_cases)
    def test_block_to_block_type(self, md, expected_type):
        assert block_to_block_type(md) == expected_type

    @pytest.mark.parametrize("md, expected_type", multiline_test_cases)
    def test_multiline(self, md, expected_type):
        assert block_to_block_type(md) == expected_type
