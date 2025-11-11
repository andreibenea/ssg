import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    test_props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }

    def test_all_none(self):
        html_node = HTMLNode()
        self.assertIsNone(html_node.tag)
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_props_result(self):
        html_node = HTMLNode("p", "Some paragraph text", None, self.test_props)
        attr_str = html_node.props_to_html()
        compare_str = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(attr_str, compare_str)

    def test_not_impl_error(self):
        html_node = HTMLNode("p", "Some paragraph text", None, self.test_props)
        self.assertRaises(NotImplementedError, html_node.to_html)

    def test_leaf_to_html_p(self):
        html_node = LeafNode("p", "Hello, world!")
        self.assertEqual(html_node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_li(self):
        html_node = LeafNode("li", "An item in a list")
        self.assertEqual(html_node.to_html(), "<li>An item in a list</li>")

    def test_leaf_to_html_a(self):
        html_node = LeafNode("a", "Click me!", None, self.test_props)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_many_children(self):
        child_node_one = LeafNode("div", "child_one")
        child_node_two = LeafNode("span", "child_two")
        child_node_three = LeafNode("span", "child_three")
        parent_node = ParentNode(
            "div", [child_node_one, child_node_two, child_node_three]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><div>child_one</div><span>child_two</span><span>child_three</span></div>",
        )

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
