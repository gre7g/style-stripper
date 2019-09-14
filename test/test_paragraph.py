import re
from unittest import TestCase
from unittest.mock import patch, Mock, call

from style_stripper.control.settings_control import Settings
from style_stripper.data.paragraph import Paragraph


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

    def test_fix_spaces(self):
        """Should be able to fix spaces"""
        settings = Settings()
        config = settings.latest_config
        paragraph = Paragraph()
        paragraph.set_dash_class_member(config)
        paragraph.text = "    some text    more text    "
        config["SPACES"]["PURGE_LEADING_WHITESPACE"] = False
        config["SPACES"]["PURGE_TRAILING_WHITESPACE"] = False
        config["SPACES"]["PURGE_DOUBLE_SPACES"] = False
        paragraph.fix_spaces(config)
        assert paragraph.text == "    some text    more text    "
        paragraph.text = "    some text    more text    "
        config["SPACES"]["PURGE_LEADING_WHITESPACE"] = True
        paragraph.fix_spaces(config)
        assert paragraph.text == "some text    more text    "
        paragraph.text = "    some text    more text    "
        config["SPACES"]["PURGE_LEADING_WHITESPACE"] = False
        config["SPACES"]["PURGE_TRAILING_WHITESPACE"] = True
        paragraph.fix_spaces(config)
        assert paragraph.text == "    some text    more text"
        paragraph.text = "    some text    more text    "
        config["SPACES"]["PURGE_TRAILING_WHITESPACE"] = False
        config["SPACES"]["PURGE_DOUBLE_SPACES"] = True
        paragraph.fix_spaces(config)
        assert paragraph.text == " some text more text "

    def test_fix_quotes_and_dashes(self):
        """Should be able to fix quotes and dashes"""
        settings = Settings()
        config = settings.latest_config
        paragraph = Paragraph()
        paragraph.text = 'This is "some poorly“ quoted text ”that needs" to be fixed.'
        config["QUOTES"]["CONVERT_TO_CURLY"] = False
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == 'This is "some poorly“ quoted text ”that needs" to be fixed.'
        config["QUOTES"]["CONVERT_TO_CURLY"] = True
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == 'This is “some poorly” quoted text “that needs” to be fixed.'
        config["QUOTES"]["CONVERT_TO_CURLY"] = False
        config["DASHES"]["CONVERT_TO_EM_DASH"] = True
        config["DASHES"]["CONVERT_TO_EN_DASH"] = False
        config["DASHES"]["CONVERT_DOUBLE_DASHES"] = False
        config["DASHES"]["FIX_DASH_AT_END_OF_QUOTE"] = False
        config["DASHES"]["FORCE_ALL_EN_OR_EM"] = False
        paragraph.set_dash_class_member(config)
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes(config)
        config["QUOTES"]["CONVERT_TO_CURLY"] = True
        config["DASHES"]["CONVERT_TO_EM_DASH"] = False
        paragraph.set_dash_class_member(config)
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote” - has been broken - “in the middle.” And then -- trouble.'
        config["DASHES"]["CONVERT_TO_EM_DASH"] = True
        paragraph.set_dash_class_member(config)
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote”—has been broken—“in the middle.” And then -- trouble.'
        config["DASHES"]["CONVERT_TO_EM_DASH"] = False
        config["DASHES"]["CONVERT_TO_EN_DASH"] = True
        paragraph.set_dash_class_member(config)
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote” – has been broken – “in the middle.” And then -- trouble.'
        config["DASHES"]["CONVERT_TO_EM_DASH"] = True
        config["DASHES"]["CONVERT_TO_EN_DASH"] = False
        config["DASHES"]["CONVERT_DOUBLE_DASHES"] = True
        paragraph.set_dash_class_member(config)
        paragraph.text = '"This quote" - has been broken - "in the middle." And then -- trouble.'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote”—has been broken—“in the middle.” And then—trouble.'
        paragraph.text = '"This quote ends in a dash-"'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote ends in a dash-”'
        config["DASHES"]["FIX_DASH_AT_END_OF_QUOTE"] = True
        paragraph.text = '"This quote ends in a dash-"'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == '“This quote ends in a dash—”'
        paragraph.text = 'wrong em – dash'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == 'wrong em – dash'
        config["DASHES"]["FORCE_ALL_EN_OR_EM"] = True
        paragraph.text = 'wrong em – dash'
        paragraph.fix_quotes_and_dashes(config)
        assert paragraph.text == 'wrong em—dash'

    def test_fix_italic_boundaries(self):
        """Should be able to fix italic boundaries"""
        settings = Settings()
        config = settings.latest_config
        paragraph = Paragraph()
        paragraph.text = " ❰  italic❱   ❰more italic  ❱ "
        config["ITALIC"]["ADJUST_TO_INCLUDE_PUNCTUATION"] = False
        paragraph.fix_italic_boundaries(config)
        assert paragraph.text == " ❰  italic❱   ❰more italic  ❱ "
        paragraph.text = 'before "❰italic❱", after'
        paragraph.fix_italic_boundaries(config)
        assert paragraph.text == 'before "❰italic❱", after'
        paragraph.text = " ❰  italic❱   ❰more italic  ❱ "
        config["ITALIC"]["ADJUST_TO_INCLUDE_PUNCTUATION"] = True
        paragraph.fix_italic_boundaries(config)
        assert paragraph.text == "   ❰italic   more italic❱   "
        paragraph.text = 'before "❰italic❱", after'
        paragraph.fix_italic_boundaries(config)
        assert paragraph.text == 'before ❰"italic",❱ after'

    @patch("style_stripper.data.paragraph.CONSTANTS")
    def test_fix_ellipses(self, CONSTANTS):
        """Should be able to fix ellipses"""
        settings = Settings()
        config = settings.latest_config
        CONSTANTS.ELLIPSES.SEARCH = re.compile(r"\.\.\.|…")
        config["ELLIPSES"]["NEW"] = " . . . "
        paragraph = Paragraph()
        paragraph.text = "one... two… three"
        config["ELLIPSES"]["REPLACE_WITH_NEW"] = False
        paragraph.fix_ellipses(config)
        assert paragraph.text == "one... two… three"
        config["ELLIPSES"]["REPLACE_WITH_NEW"] = True
        paragraph.fix_ellipses(config)
        assert paragraph.text == "one\u200a.\u200a.\u200a.\u200a two\u200a.\u200a.\u200a.\u200a three"

    def test_fix_ticks(self):
        """Should be able to fix ticks"""
        settings = Settings()
        config = settings.latest_config
        paragraph = Paragraph()
        paragraph.text = "don't"
        config["QUOTES"]["CONVERT_TO_CURLY"] = False
        ask = Mock()
        ask.return_value = True
        paragraph.fix_ticks(ask, config)
        ask.assert_not_called()
        assert paragraph.text == "don't"
        paragraph.text = "don't ’nuff bein‘ “goin' 'nuff” “ one 'two' 'three.' 'four 'five six' seven” eight “nine 'ten"
        config["QUOTES"]["CONVERT_TO_CURLY"] = True
        paragraph.fix_ticks(ask, config)
        assert paragraph.text == \
            "don’t ’nuff bein’ “goin’ ’nuff” “ one ‘two’ ‘three.’ ‘four ‘five six’ seven” eight “nine ’ten"
        ask.assert_has_calls([call(paragraph, 38), call(paragraph, 44), call(paragraph, 59), call(paragraph, 53)])
        ask = Mock()
        ask.return_value = False
        paragraph.text = "don't ’nuff bein‘ “goin' 'nuff” “ one 'two' 'three.' 'four 'five six' seven” eight “nine 'ten"
        paragraph.fix_ticks(ask, config)
        assert paragraph.text == \
            "don’t ’nuff bein’ “goin’ ’nuff” “ one ’two’ ’three.’ ’four ’five six’ seven” eight “nine ’ten"
        ask.assert_has_calls([call(paragraph, 38), call(paragraph, 44), call(paragraph, 59), call(paragraph, 53)])
