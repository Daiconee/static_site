import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node1 = TextNode("node", TextType.CODE, "https://docs.python.org/3/library/unittest.html")
        node2 = TextNode("node", TextType.CODE, "https://docs.python.org/3/library/unittest.html")
        self.assertEqual(node1, node2)
        
        node1 = TextNode("node", TextType.CODE)
        node2 = TextNode("node", TextType.CODE)
        self.assertEqual(node1, node2)
        
        node1 = TextNode("node", TextType.CODE, "https://docs.python.org/3/library/unittest.html")
        node2 = TextNode("node", TextType.CODE)
        self.assertNotEqual(node1, node2)

        node1 = TextNode("node", TextType.CODE, "https://docs.python.org/3/library/unittest.html")
        self.assertEqual(repr(node1), 'TextNode(node, code text, https://docs.python.org/3/library/unittest.html)')
    

        

if __name__ == "__main__":
    unittest.main()