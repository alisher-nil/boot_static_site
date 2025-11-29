from textnode import TextNode, TextType


def main():
    node = TextNode("Cabbages and kings", TextType.BOLD, "http://www.example.com")
    print(node)


if __name__ == "__main__":
    main()
