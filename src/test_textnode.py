import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        textNode1 = TextNode("node", TextType.LINK, "https://docs.python.org/3/library/unittest.html")
        textNode2 = TextNode("node", TextType.LINK, "https://docs.python.org/3/library/unittest.html")
        self.assertEqual(textNode1, textNode2)
        
        textNode1 = TextNode("node", TextType.LINK)
        textNode2 = TextNode("node", TextType.LINK)
        self.assertEqual(textNode1, textNode2)
        
        textNode1 = TextNode("node", TextType.LINK, "https://docs.python.org/3/library/unittest.html")
        textNode2 = TextNode("node", TextType.LINK)
        self.assertNotEqual(textNode1, textNode2)

        textNode1 = TextNode("node", TextType.LINK, "https://docs.python.org/3/library/unittest.html")
        self.assertEqual(repr(textNode1), 'TextNode(node, LINK, https://docs.python.org/3/library/unittest.html)')
    

class TestTextNodetoHTMLNode(unittest.TestCase):
    def test_link(self):
        textNode1 = TextNode("node", TextType.LINK, "https://docs.python.org/3/library/unittest.html")
        htmlNode1 = text_node_to_html_node(textNode1)
        htmlNode1_tohtml = '<a href="https://docs.python.org/3/library/unittest.html">node</a>'
        self.assertEqual(htmlNode1.to_html(), htmlNode1_tohtml)

    def test_text(self):
        textNode1 = TextNode("This is a text node", TextType.TEXT)
        htmlNode1 = text_node_to_html_node(textNode1)
        self.assertEqual(htmlNode1.tag, None)
        self.assertEqual(htmlNode1.value, "This is a text node")

class TextSplitNodes(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual( 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ], 
            new_nodes,
        )

    def test_split_nodes_bold(self):
        node = TextNode("**This is text with** a bolded word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual( 
            [
                TextNode("This is text with", TextType.BOLD),
                TextNode(" a bolded word", TextType.TEXT),
            ], 
            new_nodes,
        )

        node = TextNode("**This is text with** a *bolded* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual( 
            [
                TextNode("This is text with", TextType.BOLD),
                TextNode(" a *bolded* word", TextType.TEXT),
            ], 
            new_nodes,
        )
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


class TestRegex(unittest.TestCase):
    def test_regex_images(self):
        text = "This is text with a ![random image](https://picsum.photos/200/300) and ![another random image](https://picsum.photos/200/200)"
        res = [
            ("random image", "https://picsum.photos/200/300"),
            ("another random image", "https://picsum.photos/200/200")
        ]
        self.assertListEqual(res, extract_markdown_images(text))

    def test_regex_links(self):
        text = "This is text with a link [to a website](https://www.functionsarevalues.com) and [to youtube](https://www.youtube.com)"
        res = [
            ("to a website", "https://www.functionsarevalues.com"),
            ("to youtube", "https://www.youtube.com")
        ]
        self.assertListEqual(res, extract_markdown_links(text))

    def test_regex_links_images(self):
        text = "This is text with a link [to a website](https://www.functionsarevalues.com) and a ![random image](https://picsum.photos/200/300)"
        res = [
            ("to a website", "https://www.functionsarevalues.com"),
        ]
        self.assertListEqual(res, extract_markdown_links(text))

    
        
class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        text_image = "This is text with a ![random image](https://picsum.photos/200/300) and ![another random image](https://picsum.photos/200/200)"
        node = TextNode(text_image, TextType.TEXT)
        res = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("random image", TextType.IMAGE, "https://picsum.photos/200/300"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another random image", TextType.IMAGE, "https://picsum.photos/200/200"),
        ]
        #print(split_nodes_image([node]))
        self.assertListEqual(res, split_nodes_image([node]))

        text_image = "This is text with a link [to a website](https://www.functionsarevalues.com) and a ![random image](https://picsum.photos/200/300)"
        node = TextNode(text_image, TextType.TEXT)
        res = [
            TextNode("This is text with a link [to a website](https://www.functionsarevalues.com) and a ", TextType.TEXT),
            TextNode("random image", TextType.IMAGE, "https://picsum.photos/200/300"),
        ]
        #print(split_nodes_image([node]))
        self.assertListEqual(res, split_nodes_image([node]))

    def test_split_nodes_links(self):
        text_link = "This is text with a link [to a website](https://www.functionsarevalues.com) and [to youtube](https://www.youtube.com)"
        node = TextNode(text_link, TextType.TEXT)
        res = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to a website", TextType.LINK, "https://www.functionsarevalues.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
        ]
        #print(split_nodes_link([node]))
        self.assertListEqual(res, split_nodes_link([node]))

        text_link = "This is text with a link [to a website](https://www.functionsarevalues.com) and a ![random image](https://picsum.photos/200/300)"
        node = TextNode(text_link, TextType.TEXT)
        res = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to a website", TextType.LINK, "https://www.functionsarevalues.com"),
            TextNode(" and a ![random image](https://picsum.photos/200/300)", TextType.TEXT),
        ]
        #print(split_nodes_link([node]))
        self.assertListEqual(res, split_nodes_link([node]))

class TextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(res, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()