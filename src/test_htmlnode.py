import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        htmlNode2 = HTMLNode("input", value="Daicone", 
                             props = {"href" : "link.com", "type": "text"})
        htmlNode1 = HTMLNode("div", children=[htmlNode2])
        
        htmlNode2_props = ' href="link.com" type="text"'
        self.assertEqual(htmlNode2_props, htmlNode2.props_to_html())

        htmlNode1_repr = f'HMTLNode(div, None, [{htmlNode2}], None)'
        self.assertEqual(htmlNode1_repr, repr(htmlNode1))

        # ---------- checking with eval function ------------------------------------
        # ---------- note that for this, the repr function will need to change
        # ---------- to have (tag={self.tag}, value={self.value} ...)
        # reconstructed_htmlNode1 = eval(repr(htmlNode1)) 
        # self.assertEqual(reconstructed_htmlNode1.tag, htmlNode1.tag)
        # self.assertEqual(reconstructed_htmlNode1.value, htmlNode1.value)
        # self.assertListEqual(reconstructed_htmlNode1.children, htmlNode1.children)
        # self.assertListEqual(reconstructed_htmlNode1.children, htmlNode1.children)
        # self.assertDictEqual(reconstructed_htmlNode1.props, htmlNode1.props)
        # ---------------------------------------------------------------------------

    def test_leaf_to_html(self):
        Leafnode = LeafNode("p", "Hello, world!")
        self.assertEqual(Leafnode.to_html(), "<p>Hello, world!</p>")

        Leafnode = LeafNode("a", "here is a link")
        self.assertEqual(Leafnode.to_html(), "<a>here is a link</a>")

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


if __name__ == "__main__":
    unittest.main()