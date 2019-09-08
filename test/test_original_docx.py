from unittest import TestCase
from unittest.mock import Mock, call, patch

from style_stripper.original_docx import OriginalDocx


class TestOriginalDocx(TestCase):
    @patch("style_stripper.original_docx.Paragraph")
    @patch("style_stripper.original_docx.Document")
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
        