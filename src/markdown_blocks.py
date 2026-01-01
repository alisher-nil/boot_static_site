import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    splitter = "\n\n"
    return [block.strip() for block in markdown.split(splitter) if block.strip()]


def block_to_block_type(markdown: str) -> BlockType:
    heading_pattern = r"^#{1,6}\s.*$"
    code_pattern = r"^```[\s\S]*?```$"
    quote_pattern = r"^>.*?$"
    ulist_pattern = r"^-\s.*?$"
    if re.match(heading_pattern, markdown):
        return BlockType.HEADING
    elif re.match(code_pattern, markdown):
        return BlockType.CODE
    elif re.match(quote_pattern, markdown, re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(ulist_pattern, markdown, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def is_ordered_list(markdown: str) -> bool:
    lines = markdown.split("\n")
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\.\s", line):
            return False
    return True
