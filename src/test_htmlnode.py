import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node(self):
        tag = "b"
        value = "some text"
        node = HTMLNode(tag, value)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)

    def test_props_to_html(self):
        test_props = {
            "href": "https://www.example.com",
            "target": "_blank",
        }
        expected_result = ' href="https://www.example.com" target="_blank"'
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), expected_result)

    def test_not_implemented(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        expected_result = '<a href="https://www.example.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_result)

    def test_leaf_value_error(self):
        node = LeafNode("p", "")
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_multiple_children(self):
        child_node = LeafNode("i", "I can therefore I must")
        node = ParentNode("p", [child_node for _ in range(3)])
        expected_result = (
            "<p>"
            "<i>I can therefore I must</i>"
            "<i>I can therefore I must</i>"
            "<i>I can therefore I must</i>"
            "</p>"
        )
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
