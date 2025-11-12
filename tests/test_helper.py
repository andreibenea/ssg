import unittest

from src.textnode import TextNode, TextType
from src.node_helper import BlockType
from src.node_helper import (
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
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

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_paragraph(self):
        md = "Just a single paragraph with **bold** and _italic_."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just a single paragraph with **bold** and _italic_."],
        )

    def test_markdown_to_blocks_two_paragraphs(self):
        md = """First paragraph with a [link](https://boot.dev).

    Second paragraph with `code`."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with a [link](https://boot.dev).",
                "Second paragraph with `code`.",
            ],
        )

    def test_markdown_to_blocks_list_only(self):
        md = """- one
- two
- three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- one\n- two\n- three"],
        )

    def test_markdown_to_blocks_para_then_list_then_para(self):
        md = """Intro paragraph with **context**.

- item A
- item B
- item C

Closing paragraph with _emphasis_."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Intro paragraph with **context**.",
                "- item A\n- item B\n- item C",
                "Closing paragraph with _emphasis_.",
            ],
        )

    def test_markdown_to_blocks_three_line_paragraph(self):
        md = """This paragraph
spans multiple
lines with `code` and **bold**."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This paragraph\nspans multiple\nlines with `code` and **bold**."],
        )

    def test_markdown_to_blocks_heading_and_paragraph(self):
        md = """# Title

    This is the body under the title."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "This is the body under the title.",
            ],
        )

    def test_markdown_to_blocks_leading_and_trailing_blank_lines(self):
        md = """

    First block text.

    Second block text.

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block text.",
                "Second block text.",
            ],
        )

    def test_markdown_to_blocks_extra_blank_lines_are_ignored(self):
        # Even though "well-written" uses a single blank line, ensure robustness.
        md = """Para 1.


    Para 2.



    Para 3."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Para 1.",
                "Para 2.",
                "Para 3.",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        block = "Learning **Python** opens up endless possibilities — from _automation_ and data analysis to web apps and AI — all starting with a simple `print('Hello, world!')`."
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "## This is a Level 2 Heading"
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_max(self):
        block = "###### This is a Level 6 Heading"
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_invalid(self):
        block = "```This is NOT a code block"
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = "> 'The only way to learn a new programming language is by writing programs in it.' — Dennis Ritchie"
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- Apples  
- Bananas  
- Cherries
"""
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. Install Python  
2. Write your first script  
3. Run and debug your code
"""
        block_type = block_to_block_type(block)
        print(block_type)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"testprintHTML: {html}")
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_h1(self):
        md = "# Title One"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Title One</h1></div>",
        )

    def test_paragraph_collapses_single_newlines(self):
        md = "First line\nsecond line\nthird line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>First line second line third line</p></div>",
        )

    # 3) Heading level 6 (upper bound)
    def test_heading_h6(self):
        md = "###### Tiny Title"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h6>Tiny Title</h6></div>",
        )

    # 4) Heading-like but missing space => paragraph (per spec “# + space”)
    def test_heading_missing_space_is_paragraph(self):
        md = "##Not a heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>##Not a heading</p></div>",
        )

    # 5) Quote: every line must start with '>' and ends up in a single blockquote
    def test_quote_multiline(self):
        md = "> line one\n> line two\n> line three"
        html = markdown_to_html_node(md).to_html()
        # common simple rendering: wrap joined lines in a single paragraph inside blockquote
        self.assertEqual(
            html,
            "<div><blockquote>line one line two line three</blockquote></div>",
        )

    # 6) Unordered list: each line starts with "- " => <ul><li>..</li>...</ul>
    def test_unordered_list_basic(self):
        md = "- apples\n- bananas\n- cherries"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>apples</li><li>bananas</li><li>cherries</li></ul></div>",
        )

    # 7) Ordered list: must start at 1 and increment by 1
    def test_ordered_list_incrementing(self):
        md = "1. step one\n2. step two\n3. step three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>step one</li><li>step two</li><li>step three</li></ol></div>",
        )

    # 8) Ordered list that does NOT increment properly: treat as paragraph (per spec)
    def test_ordered_list_bad_numbering_falls_back_to_paragraph(self):
        md = "1. first\n3. third"
        html = markdown_to_html_node(md).to_html()
        # no blank line separator => single paragraph, with internal \n collapsed to space
        self.assertEqual(
            html,
            "<div><p>1. first 3. third</p></div>",
        )

    # 9) Code block preserves literal text (including inline MD) and newlines
    # def test_codeblock_preserves_inline_and_newlines(self):
    # md = """
    # 10) Code block with leading empty lines around should still be detected and preserved
    def test_codeblock_with_leading_trailing_space(self):
        md = "\n```\nline A\nline B\n```\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>line A\nline B\n</code></pre></div>",
        )

    # 11) Paragraph with unmatched inline delimiter should raise (your splitter’s rule)
    def test_paragraph_unmatched_bold_raises(self):
        md = "This **never closes"
        with self.assertRaises(Exception):
            markdown_to_html_node(md)

    def test_list_item_inline_link(self):
        md = "- Read [Boot.dev](https://www.boot.dev)"
        html = markdown_to_html_node(md).to_html()
        assert (
            html
            == '<div><ul><li>Read <a href="https://www.boot.dev">Boot.dev</a></li></ul></div>'
        )

    def test_list_item_inline_italic(self):
        md = "- Disney _didn't ruin it_"
        html = markdown_to_html_node(md).to_html()
        assert html == "<div><ul><li>Disney <i>didn't ruin it</i></li></ul></div>"

    def test_quote_no_stray_caret(self):
        md = '> "A quote."\n>\n> -- Author'
        html = markdown_to_html_node(md).to_html()
        assert html == '<div><blockquote>"A quote." -- Author</blockquote></div>'

    def test_quote_with_inline_formatting(self):
        md = "> This is a *quote* with **bold**, `code`, and a [link](https://example.com)."
        html = markdown_to_html_node(md).to_html()
        assert html == (
            "<div><blockquote>"
            "This is a *quote* with <b>bold</b>, "
            "<code>code</code>, and a "
            '<a href="https://example.com">link</a>.'
            "</blockquote></div>"
        )
