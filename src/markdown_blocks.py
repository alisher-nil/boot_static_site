def markdown_to_blocks(markdown: str) -> list[str]:
    block_splitter = "\n\n"
    blocks = [block.strip() for block in markdown.split(block_splitter) if block.strip()]
    return blocks
