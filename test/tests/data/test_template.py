from unittest import TestCase
from unittest.mock import Mock, patch, call

from style_stripper.data.template import Template


class TestTemplate(TestCase):
    @patch("style_stripper.data.template.Document")
    def test_add_content_and_save(self, Document):
        """Should be able to add content to a document and save it."""
        style1 = Mock()
        style1.name = "First Paragraph"
        style2 = Mock()
        style2.name = "Normal"
        document = Mock()
        document.styles = [style1, style2]
        document.paragraphs = [Mock()]
        runs = [Mock() for _ in range(14)]
        document.paragraphs[0].add_run.side_effect = runs[0:1]
        additional_paragraphs = [Mock() for _ in range(4)]
        document.add_paragraph.side_effect = list(additional_paragraphs)
        additional_paragraphs[0].add_run.side_effect = runs[1:4]
        additional_paragraphs[1].add_run.side_effect = runs[4:6]
        additional_paragraphs[2].add_run.side_effect = runs[6:8]
        additional_paragraphs[3].add_run.side_effect = runs[8:14]
        Document.return_value = document

        t = Template("path/to/input")
        t.add_content("line with no italic in it")
        t.add_content("line with ❰italic❱ in it")
        t.add_content("❰italic❱ in the beginning")
        t.add_content("at the end there's ❰italic❱")
        t.add_content("multiple ❰italic❱❰italic❱ and more ❰italic❱ on this line")
        t.save_as("path/to/output")

        Document.assert_called_once_with("path/to/input")
        assert document.paragraphs[0].text == ""
        assert document.paragraphs[0].style == style1
        document.paragraphs[0].assert_has_calls(
            [call.add_run("line with no italic in it")]
        )
        additional_paragraphs[0].assert_has_calls(
            [call.add_run("line with "), call.add_run("italic"), call.add_run(" in it")]
        )
        assert additional_paragraphs[0].style == style2
        additional_paragraphs[1].assert_has_calls(
            [call.add_run("italic"), call.add_run(" in the beginning")]
        )
        assert additional_paragraphs[1].style == style2
        additional_paragraphs[2].assert_has_calls(
            [call.add_run("at the end there's "), call.add_run("italic")]
        )
        assert additional_paragraphs[2].style == style2
        additional_paragraphs[3].assert_has_calls(
            [
                call.add_run("multiple "),
                call.add_run("italic"),
                call.add_run("italic"),
                call.add_run(" and more "),
                call.add_run("italic"),
                call.add_run(" on this line"),
            ]
        )
        assert additional_paragraphs[3].style == style2

        for index, italic in enumerate(
            [
                False,
                False,
                True,
                False,
                True,
                False,
                False,
                True,
                False,
                True,
                True,
                False,
                True,
                False,
            ]
        ):
            assert runs[index].italic == italic

        document.save.assert_called_once_with("path/to/output")
