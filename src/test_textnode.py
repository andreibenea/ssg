import unittest

from textnode import TextNode, TextType
from convert_txt_to_html import text_node_to_html_node
from split_nodes_delimiter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode(
            "This is a text node", TextType.LINK, "https://www.linkedin.com"
        )
        self.assertNotEqual(node, node2)

    def test_url_not_none(self):
        node = TextNode("Testing URL", TextType.LINK, "https://www.google.com")
        self.assertIsNotNone(node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode(
            "This is the alt text for the image",
            TextType.IMAGE,
            "https://cdn.mywebsite.net/assets/logo.png",
        )
        html_node = text_node_to_html_node(node)
        expected_props = {
            "src": "https://cdn.mywebsite.net/assets/logo.png",
            "alt": "This is the alt text for the image",
        }
        self.assertEqual(html_node.tag, "img")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props, expected_props)

    def test_link(self):
        node = TextNode("Some click me text", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        expected_props = {"href": "https://www.google.com"}
        self.assertEqual(html_node.tag, "a")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props, expected_props)

    def test_delimiter_type_code(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_type_italic(self):
        expected_nodes = [
            TextNode("Its ", TextType.TEXT),
            TextNode("type", TextType.ITALIC),
            TextNode(" will be italic", TextType.TEXT),
        ]
        node = TextNode("Its _type_ will be italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_invalid(self):
        node = TextNode("Looking for _an exception", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertRaises(Exception, new_nodes)

    def test_delimiter_multiple_nodes(self):
        expected_nodes = [
            TextNode("Looking for ", TextType.TEXT),
            TextNode("Baldie", TextType.BOLD),
            TextNode(" now", TextType.TEXT),
            TextNode("Looking for _an_ italian", TextType.ITALIC),
        ]
        node_one = TextNode("Looking for **Baldie** now", TextType.TEXT)
        node_two = TextNode("Looking for _an_ italian", TextType.ITALIC)
        # node_three = TextNode("Looking for **another problem", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [node_one, node_two], "**", TextType.BOLD
        )
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_last_char_is_delimiter(self):
        pass


if __name__ == "__main__":
    unittest.main()
