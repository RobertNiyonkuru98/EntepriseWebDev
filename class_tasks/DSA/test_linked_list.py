import unittest
from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.ll = LinkedList()
        self.ll.add_node(10)
        self.ll.add_node(20)
        self.ll.add_node(30)

    def test_add_node(self):
        self.ll.add_node(40)
        self.assertTrue(self.ll.search_node(40))

    def test_search_node(self):
        self.assertTrue(self.ll.search_node(20))
        self.assertFalse(self.ll.search_node(100))

    def test_delete_node(self):
        self.assertTrue(self.ll.delete_node(20))
        self.assertFalse(self.ll.search_node(20))


if __name__ == "__main__":
    unittest.main()
