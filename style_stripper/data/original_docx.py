from docx import Document
import logging
import re
from typing import List, Tuple, Optional

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.data.paragraph import Paragraph, QuestionableTick

try:
    from style_stripper.data.book import Book
except ImportError:
    Book = None

# Constants:
LOG = logging.getLogger(__name__)


class OriginalDocx(object):
    def __init__(self, path: str, book: Book) -> None:
        self.book = book
        self.questionable_ticks: List[Tuple[Paragraph, int]] = []

        self.paragraphs: List[Paragraph] = []
        self.symbolic_divider_indexes: List[int] = []
        doc = Document(path)

        word_count = 0
        for paragraph in doc.paragraphs:
            paragraph_obj = Paragraph()

            for run in paragraph.runs:
                paragraph_obj.add(run.text, run.italic)
            paragraph_obj.get_word_count()
            word_count += paragraph_obj.word_count

            # # must_change.append((offset, "‘" if ask_function(self, offset) else "’"))

            # LOG.debug(paragraph_obj.text)
            self.paragraphs.append(paragraph_obj)

        self.book.author = doc.core_properties.author
        self.book.title = doc.core_properties.title
        self.book.word_count = word_count
        self.book.last_modified = doc.core_properties.modified

    def fix_spaces(self):
        for paragraph in self.paragraphs:
            paragraph.fix_spaces(self.book.config)

    def fix_italic_boundaries(self):
        for paragraph in self.paragraphs:
            paragraph.fix_italic_boundaries(self.book.config)

    def fix_ellipses(self):
        for paragraph in self.paragraphs:
            paragraph.fix_ellipses(self.book.config)

    def fix_quotes_and_dashes(self):
        for paragraph in self.paragraphs:
            paragraph.fix_quotes_and_dashes(self.book.config)

    def fix_ticks(self) -> List[QuestionableTick]:
        self.questionable_ticks = []
        for paragraph in self.paragraphs:
            paragraph.fix_ticks(self.book.config, self.questionable_ticks)
        return self.questionable_ticks

    def find_heading_candidates(self) -> Tuple[int, int, int]:
        part = chapter = end = 0
        for paragraph in self.paragraphs:
            for pattern in CONSTANTS.HEADINGS.SEARCH_PART:
                if pattern.search(paragraph.text):
                    part += 1
                    break
            for pattern in CONSTANTS.HEADINGS.SEARCH_CHAPTER:
                if pattern.search(paragraph.text):
                    chapter += 1
                    break
            for pattern in CONSTANTS.HEADINGS.SEARCH_THE_END:
                if pattern.search(paragraph.text):
                    end += 1
                    break

        LOG.debug("parts found: %d", part)
        LOG.debug("chapters found: %d", chapter)
        LOG.debug("the end found: %d", end)
        return part, chapter, end

    @staticmethod
    def matches_any(searches: re.Pattern, text: str):
        for search in searches:
            if search.search(text):
                return True
        else:
            return False

    def style_part_chapter(self, chapter_style: str):
        found_part = found_chapter = None
        group = []
        index = 0
        while index < len(self.paragraphs):
            paragraph = self.paragraphs[index]
            if paragraph.text == "":
                group.append(index)
            elif self.matches_any(CONSTANTS.HEADINGS.SEARCH_PART, paragraph.text):
                group.append(index)
                found_part = paragraph
            elif found_part:
                found_part.style = CONSTANTS.STYLING.NAMES.HEADING1
                self.paragraphs[group[0]:group[-1] + 1] = [found_part]
                index = group[0]
                found_part = None
                group = []
            elif self.matches_any(CONSTANTS.HEADINGS.SEARCH_CHAPTER, paragraph.text):
                group.append(index)
                found_chapter = paragraph
            elif found_chapter:
                found_chapter.style = chapter_style
                self.paragraphs[group[0]:group[-1]+1] = [found_chapter]
                index = group[0]
                found_chapter = None
                group = []
            else:
                group = []

            index += 1

    def style_end(self):
        found_end = None
        group = []
        index = 0
        while index < len(self.paragraphs):
            paragraph = self.paragraphs[index]
            if paragraph.text == "":
                group.append(index)
            elif self.matches_any(CONSTANTS.HEADINGS.SEARCH_THE_END, paragraph.text):
                group.append(index)
                found_end = paragraph
            elif found_end:
                found_end.style = CONSTANTS.STYLING.NAMES.THE_END
                self.paragraphs[group[0]:group[-1]+1] = [found_end]
                index = group[0]
                found_end = None
                group = []
            else:
                group = []

            index += 1

    def add_end(self):
        end = Paragraph(self.book.config[HEADINGS][THE_END])
        end.style = CONSTANTS.STYLING.NAMES.THE_END
        self.paragraphs.append(end)

    def find_divider_candidates(self) -> Tuple[int, int]:
        count_of_symbolic = count_of_blanks = 0
        found_blank = found_symbol = False
        group = []
        for index, paragraph in enumerate(self.paragraphs):
            if not CONSTANTS.DIVIDER.SEARCH.search(paragraph.text):  # No word content
                group.append(index)
                if paragraph.text == "":
                    found_blank = True
                else:
                    found_symbol = True
            else:
                if found_symbol:
                    self.symbolic_divider_indexes.append(group)
                    count_of_symbolic += 1
                elif found_blank:
                    count_of_blanks += 1
                found_blank = found_symbol = False
                group = []

        LOG.debug("symbolic dividers found: %d", count_of_symbolic)
        LOG.debug("symbolic blanks found: %d", count_of_blanks)

        return count_of_symbolic, count_of_blanks

    def replace_symbolic(self) -> None:
        for index in self.symbolic_divider_indexes:
            if self.book.config[DIVIDER][REPLACE_WITH_NEW]:
                self.paragraphs[index] = Paragraph(self.book.config[DIVIDER][NEW])
            self.paragraphs[index].style = CONSTANTS.STYLING.NAMES.DIVIDER

    def remove_blanks(self) -> None:
        # Indexes are meaninless once we delete paragraphs
        self.symbolic_divider_indexes = []

        index = 0
        while index < len(self.paragraphs):
            if self.paragraphs[index].text:
                index += 1
            else:
                del self.paragraphs[index]

    def replace_blanks(self) -> None:
        # Indexes are meaninless once we delete paragraphs
        self.symbolic_divider_indexes = []

        in_blanks = False
        index = 0
        while index < len(self.paragraphs):
            if self.paragraphs[index].text:
                index += 1
                in_blanks = False
            else:
                if in_blanks:
                    if self.book.config[DIVIDER][REPLACE_WITH_NEW]:
                        del self.paragraphs[index]
                    else:
                        self.paragraphs[index].style = self.book.config[STYLING][NAMES][DIVIDER]
                        index += 1
                else:
                    if self.book.config[DIVIDER][REPLACE_WITH_NEW]:
                        self.paragraphs[index] = Paragraph(self.book.config[DIVIDER][NEW])
                    self.paragraphs[index].style = CONSTANTS.STYLING.NAMES.DIVIDER
                    index += 1
                    in_blanks = True

        # May have stuck a divider at the end by accident
        if self.paragraphs[-1].style == CONSTANTS.STYLING.NAMES.DIVIDER:
            del self.paragraphs[-1]
