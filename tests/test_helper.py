import unittest

from textnode import TextNode, TextType
from node_helper import (
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_split_links_link_only_node(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes
        )

    def test_text_to_textnodes(self):
        txt_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_bold(self):
        txt_str = "This is **bold text** only."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" only.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_italic(self):
        txt_str = "Testing an _italic phrase_ in isolation."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Testing an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in isolation.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_code(self):
        txt_str = "Inline `code block` check."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Inline ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" check.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_image(self):
        txt_str = "Here is an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_link(self):
        txt_str = "Visit [Boot.dev](https://boot.dev) for coding!"
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" for coding!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_code_with_link_inside(self):
        txt_str = "Do not parse `[link](https://boot.dev)` inside code."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Do not parse ", TextType.TEXT),
                TextNode("[link](https://boot.dev)", TextType.CODE),
                TextNode(" inside code.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_invalid_unclosed_code_raises(self):
        txt_str = "This has `unclosed code."
        with self.assertRaises(Exception):
            text_to_textnodes(txt_str)

    def test_text_to_textnodes_bold_and_italic(self):
        txt_str = "This is **bold** and _italic_ text."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_code_image_italic_link(self):
        txt_str = "Mix `code` and ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) plus _style_ and a [link](https://boot.dev)."
        new_nodes = text_to_textnodes(txt_str)
        self.assertListEqual(
            [
                TextNode("Mix ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" plus ", TextType.TEXT),
                TextNode("style", TextType.ITALIC),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
