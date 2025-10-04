import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_unequal(self):
        node = TextNode("Text node 1", TextType.PLAIN)
        another_node = TextNode("Text node 2", TextType.PLAIN)
        self.assertNotEqual(node, another_node)

    def test_different_types(self):
        common_text = "Same text"
        type1 = TextType.BOLD
        type2 = TextType.PLAIN
        node_1 = TextNode(common_text, type1)
        node_2 = TextNode(common_text, type2)
        self.assertNotEqual(node_1, node_2)

    def test_eq_non_empty_url(self):
        text = "test text"
        type = TextType.LINK
        url = "http://www.example.com"
        node_1 = TextNode(text, type, url)
        node_2 = TextNode(text, type, url)
        self.assertEqual(node_1, node_2)


if __name__ == "__main__":
    unittest.main()
