import re


class BiblePassageReference:

    def __init__(self, book, starting_chapter, starting_verse, end_chapter, end_verse):
        self.book = book
        self.starting_chapter = starting_chapter
        self.starting_verse = starting_verse
        self.end_chapter = end_chapter
        self.end_verse = end_verse

    def is_whole_book(self):
        return self.end_chapter == -1

    def is_whole_chapter(self):
        return self.end_verse == -1 and self.end_chapter != -1

    def get_chapters(self):
        return list(range(self.starting_chapter, self.end_chapter + 1))

    def __str__(self):
        return self.book + ' ' + str(self.starting_chapter) + ':' + str(self.starting_verse) + '-' + str(
            self.end_chapter) + ':' + str(self.end_verse)

    def pretty(self):

        if self.is_whole_book():
            return self.book

        if self.starting_chapter == self.end_chapter and self.starting_verse == 1 and self.end_verse == -1:
            return self.book + ' ' + str(self.starting_chapter)

        if self.starting_chapter != self.end_chapter and self.starting_verse == 1 and self.end_verse == -1:
            return self.book + ' ' + str(self.starting_chapter) + '-' + str(self.end_chapter)

        if self.starting_verse == 1 and self.starting_chapter != self.end_chapter and self.end_verse != -1:
            return self.book + ' ' + str(self.starting_chapter) + '-' + str(self.end_chapter) + ':' + str(
                self.end_verse)

        return self.book + ' ' + str(self.starting_chapter) + ':' + str(self.starting_verse) + '-' + str(
            self.end_chapter) + ':' + str(self.end_verse)

    def __repr__(self):
        return "BibleRef." + self.book + '.' + str(self.starting_chapter) + ':' + str(self.starting_verse) + '-' + str(
            self.end_chapter) + ':' + str(self.end_verse)

    @classmethod
    def parse(cls, string):

        reference_matching_regex = re.compile(
            '(\d?[\sa-zA-Z]*[a-zA-Z]) ?(\d{1,3})?:?(\d{1,3})?-?(\d{1,3})?:?(\d{1,3})?')

        match = reference_matching_regex.match(string)

        if not match:
            return None

        book_name = match.group(1)

        if not match.group(2):
            start_chapter = 1
            start_verse = 1
            end_chapter = -1
            end_verse = -1

        if match.group(2):
            start_chapter = int(match.group(2))

        if not match.group(3):
            start_verse = 1
            end_verse = -1

        if match.group(1) and match.group(2) and not match.group(3) and match.group(4) and not match.group(5):
            start_chapter = int(match.group(2))
            start_verse = 1
            end_chapter = int(match.group(4))
            end_verse = -1

        if match.group(3):
            start_verse = int(match.group(3))

        if match.group(1) and match.group(2) and match.group(3) and match.group(4) and not match.group(5):
            end_verse = int(match.group(4))
            end_chapter = start_chapter

        if match.group(4) and match.group(5):
            end_chapter = int(match.group(4))
            end_verse = int(match.group(5))

        if match.group(2) and not match.group(4) and not match.group(5):
            end_chapter = start_chapter

        return BiblePassageReference(book_name, start_chapter, start_verse, end_chapter, end_verse)
