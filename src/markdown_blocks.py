from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [item.strip() for item in blocks]
    blocks = [item for item in blocks if item]
    return blocks

def block_to_block_type(block: str):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.fullmatch(r"^`{3}(?!`)[\s\S]*?(?<!`)`{3}$", block):
        # negative lookbehind ^`{3}(?!`) at start 
        # and negative lookahead (?<!`)`{3}$ at end for exactly 3 "`"
        # [\s\S]*? non greedy 
        return BlockType.CODE
    elif check_lines_in_block(block, ">"):
        return BlockType.QUOTE
    elif check_lines_in_block(block, "- "):
        return BlockType.UNORDERED_LIST
    elif check_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


    
def check_lines_in_block(block: str, start: str):
    ls = block.split("\n")
    ls = [item.strip() for item in ls]
    for line in ls:
        if not re.match(r"^" + start, line):
           return False
    return True

def check_ordered_list(block: str):
    ls = block.split("\n")
    ls = [item.strip() for item in ls]
    i = 1
    for line in ls:
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True


def markdown_to_html_node(markdown):
    pass