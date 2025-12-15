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
    block_splitter = "\n\n"
    blocks = [block.strip() for block in markdown.split(block_splitter) if block.strip()]
    return blocks


def block_to_block_type(markdown: str) -> BlockType:
    heading_pattern = r"^[#]{1,6} .*$"
    if re.match(heading_pattern, markdown):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH
