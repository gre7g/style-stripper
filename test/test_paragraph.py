from unittest.mock import patch
from unittest import TestCase

from style_stripper.paragraph import Paragraph


class TestParagraph(TestCase):
    def test_add(self):
        """Should be able to add strings"""
        paragraph = Paragraph()
        paragraph.add("plain", False)
        paragraph.add("italic", True)
        paragraph.add("more plain", False)
        paragraph.add("more italic", True)
        paragraph.add("even more italic", True)
        assert paragraph.text == "plain❰italic❱more plain❰more italiceven more italic❱"

    @patch("style_stripper.paragraph.CONSTANTS")
    def test_fix_spaces(self, CONSTANTS):
        """Should be able to fix spaces"""
        paragraph = Paragraph()
        paragraph.text = "    some text    more text    "
        CONSTANTS.SPACES.PURGE_LEADING_WHITESPACE = False
        CONSTANTS.SPACES.PURGE_TRAILING_WHITESPACE = False
        CONSTANTS.SPACES.PURGE_DOUBLE_SPACES = False
        paragraph.fix_spaces()
        assert paragraph.text == "    some text    more text    "
        paragraph.text = "    some text    more text    "
        CONSTANTS.SPACES.PURGE_LEADING_WHITESPACE = True
        paragraph.fix_spaces()
        assert paragraph.text == "some text    more text    "
        paragraph.text = "    some text    more text    "
        CONSTANTS.SPACES.PURGE_LEADING_WHITESPACE = False
        CONSTANTS.SPACES.PURGE_TRAILING_WHITESPACE = True
        paragraph.fix_spaces()
        assert paragraph.text == "    some text    more text"
        paragraph.text = "    some text    more text    "
        CONSTANTS.SPACES.PURGE_TRAILING_WHITESPACE = False
        CONSTANTS.SPACES.PURGE_DOUBLE_SPACES = True
        paragraph.fix_spaces()
        assert paragraph.text == " some text more text "

    @patch("style_stripper.paragraph.CONSTANTS")
    def test_fix_quotes_and_dashes(self, CONSTANTS):
        """Should be able to fix quotes and dashes"""
        paragraph = Paragraph()
        paragraph.text = 'This is "some poorly“ quoted text ”that needs" to be fixed.'
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = False
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == 'This is "some poorly“ quoted text ”that needs" to be fixed.'
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = True
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == 'This is “some poorly” quoted text “that needs” to be fixed.'
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = False
        CONSTANTS.DASHES.CONVERT_TO_EM_DASH = True
        CONSTANTS.DASHES.CONVERT_TO_EN_DASH = False
        CONSTANTS.DASHES.CONVERT_DOUBLE_DASHES = False
        paragraph = Paragraph()
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes()
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = True
        CONSTANTS.DASHES.CONVERT_TO_EM_DASH = False
        paragraph = Paragraph()
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote” - has been broken - “in the middle.” And then -- trouble.'
        CONSTANTS.DASHES.CONVERT_TO_EM_DASH = True
        paragraph = Paragraph()
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote”—has been broken—“in the middle.” And then -- trouble.'
        CONSTANTS.DASHES.CONVERT_TO_EM_DASH = False
        CONSTANTS.DASHES.CONVERT_TO_EN_DASH = True
        paragraph = Paragraph()
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote” – has been broken – “in the middle.” And then -- trouble.'
        CONSTANTS.DASHES.CONVERT_TO_EM_DASH = True
        CONSTANTS.DASHES.CONVERT_TO_EN_DASH = False
        CONSTANTS.DASHES.CONVERT_DOUBLE_DASHES = True
        paragraph = Paragraph()
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote”—has been broken—“in the middle.” And then—trouble.'

    @patch("style_stripper.paragraph.CONSTANTS")
    def test_fix_italic_boundaries(self, CONSTANTS):
        """Should be able to fix italic boundaries"""
        paragraph = Paragraph()
        paragraph.text = " ❰  italic❱   ❰more italic  ❱ "
        CONSTANTS.ITALIC.ADJUST_TO_INCLUDE_PUNCTUATION = False
        paragraph.fix_italic_boundaries()
        assert paragraph.text == " ❰  italic❱   ❰more italic  ❱ "
        paragraph.text = 'before "❰italic❱", after'
        paragraph.fix_italic_boundaries()
        assert paragraph.text == 'before "❰italic❱", after'
        paragraph.text = " ❰  italic❱   ❰more italic  ❱ "
        CONSTANTS.ITALIC.ADJUST_TO_INCLUDE_PUNCTUATION = True
        paragraph.fix_italic_boundaries()
        assert paragraph.text == "   ❰italic   more italic❱   "
        paragraph.text = 'before "❰italic❱", after'
        paragraph.fix_italic_boundaries()
        assert paragraph.text == 'before ❰"italic",❱ after'
