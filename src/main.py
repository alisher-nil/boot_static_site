from textnode import TextNode, TextType


def main():
    node = TextNode(
        "hello",
        TextType.BOLD,
        "https://www.google.com",
    )
    print(node)


if __name__ == "__main__":
    main()
