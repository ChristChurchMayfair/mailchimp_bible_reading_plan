import unittest
from BiblePassageReference import BiblePassageReference

class TestPassageReferenceParsing(unittest.TestCase):

    def test_basic_reference(self):
        reference_string = "Mark 1"

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual(passage_reference.book, "Mark")
        self.assertEqual(passage_reference.starting_chapter, 1, "start chapter")
        self.assertEqual(passage_reference.starting_verse, 1, "start verse")
        self.assertEqual(passage_reference.end_chapter, 1, "end chapter")
        self.assertEqual(passage_reference.end_verse, -1, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book(), 'Not a whole book.')
        self.assertEqual(True, passage_reference.is_whole_chapter(), 'Is a whole chapter.')

    def test_whole_book_parsing(self):

        reference_string = 'Genesis'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("Genesis", passage_reference.book)
        self.assertEqual(1, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(1, passage_reference.starting_verse, "starting verse")

        self.assertEqual(True, passage_reference.is_whole_book(), "is a whole book")


    def test_passage_within_chapter(self):

        reference_string = 'Matthew 14:3-10'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("Matthew", passage_reference.book)
        self.assertEqual(14, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(3, passage_reference.starting_verse, "starting verse")
        self.assertEqual(14, passage_reference.end_chapter, "end chapter")
        self.assertEqual(10, passage_reference.end_verse, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book())
        self.assertEqual(False, passage_reference.is_whole_chapter())


    def test_passage_spanning_chapters(self):

        reference_string = 'Matthew 14:3-15:30'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("Matthew", passage_reference.book)
        self.assertEqual(14, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(3, passage_reference.starting_verse, "starting verse")
        self.assertEqual(15, passage_reference.end_chapter, "end chapter")
        self.assertEqual(30, passage_reference.end_verse, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book())
        self.assertEqual(False, passage_reference.is_whole_chapter())

    def test_passage_with_numerical_prefix(self):
        reference_string = '1 Peter 14:3-15:30'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("1 Peter", passage_reference.book)
        self.assertEqual(14, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(3, passage_reference.starting_verse, "starting verse")
        self.assertEqual(15, passage_reference.end_chapter, "end chapter")
        self.assertEqual(30, passage_reference.end_verse, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book())
        self.assertEqual(False, passage_reference.is_whole_chapter())

    def test_passage_with_multiple_book_parts(self):
        reference_string = 'Song of Songs 14:3-15:30'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("Song of Songs", passage_reference.book)
        self.assertEqual(14, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(3, passage_reference.starting_verse, "starting verse")
        self.assertEqual(15, passage_reference.end_chapter, "end chapter")
        self.assertEqual(30, passage_reference.end_verse, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book())
        self.assertEqual(False, passage_reference.is_whole_chapter())


    def test_single_chapter_book(self):
        reference_string = '3 John'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("3 John", passage_reference.book)
        self.assertEqual(1, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(1, passage_reference.starting_verse, "starting verse")
        self.assertEqual(-1, passage_reference.end_chapter, "end chapter")
        self.assertEqual(-1, passage_reference.end_verse, "end verse")

        self.assertEqual(True, passage_reference.is_whole_book())
        self.assertEqual(False, passage_reference.is_whole_chapter())

    def test_passage_with_multiple_chapters(self):
        reference_string = 'Psalm 5-6'

        passage_reference = BiblePassageReference.parse(reference_string)

        self.assertEqual("Psalm", passage_reference.book)
        self.assertEqual(5, passage_reference.starting_chapter, "starting chapter")
        self.assertEqual(1, passage_reference.starting_verse, "starting verse")
        self.assertEqual(6, passage_reference.end_chapter, "end chapter")
        self.assertEqual(-1, passage_reference.end_verse, "end verse")

        self.assertEqual(False, passage_reference.is_whole_book())
        self.assertEqual(True, passage_reference.is_whole_chapter())