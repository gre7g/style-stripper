from unittest import TestCase
from unittest.mock import Mock, call, patch

from style_stripper.data.original_docx import OriginalDocx


class TestOriginalDocx(TestCase):
    @patch("style_stripper.data.original_docx.Paragraph")
    @patch("style_stripper.data.original_docx.Document")
    def test_create(self, Document, Paragraph):
        """Should be able to create a document."""
        runs = [Mock() for _ in range(3)]
        runs[0].text = "one"
        runs[0].italic = False
        runs[1].text = "two"
        runs[1].italic = True
        runs[2].text = "three"
        runs[2].italic = False
        doc = Mock()
        doc.paragraphs = [Mock(), Mock()]
        doc.paragraphs[0].runs = runs[0:2]
        doc.paragraphs[1].runs = runs[2:3]
        Document.return_value = doc
        para_objs = [Mock(), Mock()]
        Paragraph.side_effect = list(para_objs)
        ask = Mock()

        orig = OriginalDocx("path/to/docx", ask)

        Document.assert_called_once_with("path/to/docx")
        para_objs[0].assert_has_calls([
            call.add('one', False), call.add('two', True),
            call.fix_spaces(), call.fix_italic_boundaries(), call.fix_quotes_and_dashes(), call.fix_ticks(ask)
        ])
        para_objs[1].assert_has_calls([
            call.add('three', False),
            call.fix_spaces(), call.fix_italic_boundaries(), call.fix_quotes_and_dashes(), call.fix_ticks(ask)
        ])
        assert orig.paragraphs == para_objs

    @patch("style_stripper.data.original_docx.Document")
    def test_find_divider_and_replace(self, Document):
        """Should be able to count divider candidates and replace them."""
        doc = Mock()
        doc.paragraphs = []
        Document.return_value = doc
        ask = Mock()
        orig = OriginalDocx("path/to/docx", ask)

        paragraphs = []
        for text in ["  ❰# # #❱  ", "#", "", "", "", "***", "", "*"]:
            paragraph = Mock()
            paragraph.text = text
            paragraph.style = None
            paragraphs.append(paragraph)
        orig.paragraphs = list(paragraphs)

        assert orig.find_divider_candidates() == (4, 2)

        orig.replace_symbolic()
        for index, text in enumerate(["# # #", "# # #", "", "", "", "# # #", "", "# # #"]):
            assert text == orig.paragraphs[index].text
            assert orig.paragraphs[index].style == ("Separator" if text == "# # #" else None)

        orig.remove_blanks()
        for index, text in enumerate(["# # #", "# # #", "# # #", "# # #"]):
            assert text == orig.paragraphs[index].text
            assert orig.paragraphs[index].style == ("Separator" if text == "# # #" else None)

        orig.paragraphs = list(paragraphs)
        orig.replace_blanks()
        for index, text in enumerate(["  ❰# # #❱  ", "#", "# # #", "***", "# # #", "*"]):
            assert text == orig.paragraphs[index].text
            assert orig.paragraphs[index].style == ("Separator" if text == "# # #" else None)

    @patch("style_stripper.data.original_docx.Document")
    def test_find_headers_and_replace(self, Document):
        """Should be able to count headers and replace them."""
        doc = Mock()
        doc.paragraphs = []
        Document.return_value = doc
        ask = Mock()
        orig = OriginalDocx("path/to/docx", ask)

        paragraphs = []
        for text in ["Part I", "Part VI", "Chapter 1", "Chapter 2: It Continues", "The end", "Fin"]:
            paragraph = Mock()
            paragraph.text = text
            paragraph.style = None
            paragraphs.append(paragraph)
        orig.paragraphs = list(paragraphs)

        assert orig.find_heading_candidates() == (2, 2, 2)

        orig.style_headings("PART", "CHAPTER", "END")
        for index, style in enumerate(["PART", "PART", "CHAPTER", "CHAPTER", "END", "END"]):
            assert orig.paragraphs[index].style == style

    @patch("style_stripper.data.original_docx.Document")
    @patch("style_stripper.data.original_docx.CONSTANTS")
    def test_remove_dividers_before_headings(self, CONSTANTS, Document):
        """Should be able to remove dividers mistakenly placed before headings."""
        doc = Mock()
        doc.paragraphs = []
        Document.return_value = doc
        ask = Mock()
        orig = OriginalDocx("path/to/docx", ask)
        CONSTANTS.STYLING.NAMES.DIVIDER = "Separator"
        CONSTANTS.STYLING.NAMES.HEADING1 = "Heading 1"
        CONSTANTS.STYLING.NAMES.HEADING2 = "Heading 2"

        paragraphs = []
        for style in [None, None, "Separator", None, "Separator", "Heading 1", None, "Separator", "Heading 2", None]:
            paragraph = Mock()
            paragraph.style = style
            paragraphs.append(paragraph)
        orig.paragraphs = list(paragraphs)

        orig.remove_dividers_before_headings()

        orig.style_headings("PART", "CHAPTER", "END")
        for index, style in enumerate([None, None, "Separator", None, "Heading 1", None, "Heading 2", None]):
            assert orig.paragraphs[index].style == style
