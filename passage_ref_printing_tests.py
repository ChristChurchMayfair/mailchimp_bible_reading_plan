import unittest
from BiblePassageReference import BiblePassageReference


class TestPassageReferenceParsing(unittest.TestCase):

    def test_single_chapter_ref_printing(self):
        reference = BiblePassageReference("Genesis", 1, 1, 1, -1)
        expected_pretty_string = "Genesis 1"

        self.assertEqual(expected_pretty_string, reference.pretty(), "nicely formatted string")

    def test_multi_chapter_ref_printing(self):
        reference = BiblePassageReference("Genesis", 1, 1, 2, -1)
        expected_pretty_string = "Genesis 1-2"

        self.assertEqual(expected_pretty_string, reference.pretty(), "nicely formatted string")


    def test_partially_full_ref_printing(self):
        reference = BiblePassageReference("Genesis", 1, 1, 2, 11)
        expected_pretty_string = "Genesis 1-2:11"

        self.assertEqual(expected_pretty_string, reference.pretty(), "nicely formatted string")

    def test_full_ref_printing(self):
        reference = BiblePassageReference("Genesis", 1, 4, 2, 11)
        expected_pretty_string = "Genesis 1:4-2:11"

        self.assertEqual(expected_pretty_string, reference.pretty(), "nicely formatted string")

    def test_single_chapter_books(self):
        reference = BiblePassageReference("3 John", 1, 1, -1, -1)
        expected_pretty_string = "3 John"

        self.assertEqual(expected_pretty_string, reference.pretty(), "nicely formatted string")



