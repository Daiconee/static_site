from textnode import TextNode, TextType

def main():
    newTextNode = TextNode("This is some anchor text", TextType.CODE, "https://www.boot.dev")
    print(newTextNode)
    print("test")

if __name__ == "__main__":
    main()