import unittest

from textnode import TextNode, TextType
from node_helper import (
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
)


class TestHelper(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected_matches = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(matches, expected_matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected_matches = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(matches, expected_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) plus even more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" plus even more text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with no image and a little bit of more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with no image and a little bit of more text",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_images_not_type_text(self):
        node = TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) for you to check out!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link ",
                    TextType.TEXT,
                ),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and ",
                    TextType.TEXT,
                ),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(
                    " for you to check out!",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )
