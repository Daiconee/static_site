from typing import List
import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: List[TextNode], 
                          delimiter: str, text_type: TextType):
    ls = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ls.append(old_node)
            continue
        old_node_textNodes = old_node.text.split(delimiter)
        if len(old_node_textNodes) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for index, item in enumerate(old_node_textNodes):
            if not item: # skip empty strings (handles cases such as: "example text **bold****bold** example text")
                continue
            if index % 2: # odd index = textType
                ls.append(TextNode(item, text_type))
            else:
                ls.append(TextNode(item, TextType.TEXT))
    return ls

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: List[TextNode]):
    ls = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ls.append(old_node)
            continue
        text = old_node.text
        if not text:
            return Exception("TextNode is empty, no image splitting possible")
        images = extract_markdown_images(text) # list of image tuples
        if images: # there are images in text
            pattern = re.compile(r"!\[.*?\]\(.*?\)")
            text_list = pattern.split(text)
            for i in range(len(text_list)):
                if not text_list[i]:
                    continue
                ls.append(TextNode(text_list[i], TextType.TEXT))
                if i < len(text_list) - 1:
                    alt_text = images[i][0]
                    url = images[i][1]
                    ls.append(TextNode(alt_text, TextType.IMAGE, url))
        else:
            ls.append(old_node) # if no image, TextNode is just original text
        
    return ls
            

def split_nodes_link(old_nodes: List[TextNode]):
    ls = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ls.append(old_node)
            continue
        text = old_node.text
        if not text:
            return Exception("TextNode is empty, no image splitting possible")
        links = extract_markdown_links(text) # list of link tuples
        if links: # there are links in text
            pattern = re.compile(r"(?<!!)\[.*?\]\(.*?\)")
            text_list = pattern.split(text)
            for i in range(len(text_list)):
                if not text_list[i]:
                    continue
                ls.append(TextNode(text_list[i], TextType.TEXT))
                if i < len(text_list) - 1:
                    alt_text = links[i][0]
                    url = links[i][1]
                    ls.append(TextNode(alt_text, TextType.LINK, url))
        else:
            ls.append(old_node) # if no link, TextNode is just original text
        
    return ls


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    textNodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    textNodes = split_nodes_delimiter(textNodes, "_", TextType.ITALIC)
    textNodes = split_nodes_delimiter(textNodes, "`", TextType.CODE)
    textNodes = split_nodes_image(textNodes)
    textNodes = split_nodes_link(textNodes)
    return textNodes


def delimiter_test():
    s1 = "example text **bold****bold** example text"
    ls = s1.split("**")
    # shows that skipping empty string preserves TextType indexing
    ls2 = []
    for index, item in enumerate(ls):
            if not item: 
                continue
            if index % 2: # odd index = textType
                ls2.append([item, "BOLD"])
            else:
                ls2.append([item, "TEXT"])
    print(ls2)
    s1 = "**bold****bold** example text"
    ls = s1.split("**")
    
    # shows that starting with delimiter does not cause issues
    ls2 = []
    for index, item in enumerate(ls):
            if not item: 
                continue
            if index % 2: # odd index = textType
                ls2.append([item, "BOLD"])
            else:
                ls2.append([item, "TEXT"])
    print(ls2)


def text_to_textnodes_test():
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))


# if __name__ == "__main__":
#     # delimiter_test()
#     # text_to_textnodes_test()
