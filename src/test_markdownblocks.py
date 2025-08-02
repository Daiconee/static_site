import unittest
from markdown_blocks import *

class MarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UNORDERED_LIST)

        md = """
> This is a quote
> This is also a quote

>This is also a quote

1. This is and ordered list
2. This is the same ordered list
3. still the same ordered list

- This is a list
- with items

``` this is a block
of code ```

```` this is not a line of code ````

-This is not a list
-with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.CODE)
        self.assertEqual(block_to_block_type(blocks[5]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[6]), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()