from unittest import TestCase
from unittest.mock import patch, Mock, call

from style_stripper.paragraph import Paragraph


class TestParagraph(TestCase):
    def test_add(self):
        """Should be able to add strings"""
        paragraph = Paragraph("initial value")
        assert paragraph.text == "initial value"
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
        CONSTANTS.DASHES.FIX_DASH_AT_END_OF_QUOTE = False
        CONSTANTS.DASHES.FORCE_ALL_EN_OR_EM = False
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
        paragraph.text = '"This quote ends in a dash-"'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote ends in a dash-”'
        CONSTANTS.DASHES.FIX_DASH_AT_END_OF_QUOTE = True
        paragraph.text = '"This quote ends in a dash-"'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == '“This quote ends in a dash—”'
        paragraph.text = 'wrong em – dash'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == 'wrong em – dash'
        CONSTANTS.DASHES.FORCE_ALL_EN_OR_EM = True
        paragraph.text = 'wrong em – dash'
        paragraph.fix_quotes_and_dashes()
        assert paragraph.text == 'wrong em—dash'

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

    @patch("style_stripper.paragraph.CONSTANTS")
    def test_fix_ticks(self, CONSTANTS):
        """Should be able to fix ticks"""
        paragraph = Paragraph()
        paragraph.text = "don't"
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = False
        ask = Mock()
        ask.return_value = True
        paragraph.fix_ticks(ask)
        ask.assert_not_called()
        assert paragraph.text == "don't"
        paragraph.text = "don't ’nuff bein‘ “goin' 'nuff” “ one 'two' 'three.' 'four 'five six' seven” eight “nine 'ten"
        CONSTANTS.QUOTES.CONVERT_TO_CURLY = True
        paragraph.fix_ticks(ask)
        assert paragraph.text == \
            "don’t ’nuff bein’ “goin’ ’nuff” “ one ‘two’ ‘three.’ ‘four ‘five six’ seven” eight “nine ’ten"
        ask.assert_has_calls([call(paragraph, 38), call(paragraph, 44), call(paragraph, 59), call(paragraph, 53)])
        ask = Mock()
        ask.return_value = False
        paragraph.text = "don't ’nuff bein‘ “goin' 'nuff” “ one 'two' 'three.' 'four 'five six' seven” eight “nine 'ten"
        paragraph.fix_ticks(ask)
        assert paragraph.text == \
            "don’t ’nuff bein’ “goin’ ’nuff” “ one ’two’ ’three.’ ’four ’five six’ seven” eight “nine ’ten"
        ask.assert_has_calls([call(paragraph, 38), call(paragraph, 44), call(paragraph, 59), call(paragraph, 53)])
