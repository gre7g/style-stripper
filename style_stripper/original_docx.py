from docx import Document
import logging
from types import FunctionType
from typing import List

from style_stripper.paragraph import Paragraph

# Constants:
LOG = logging.getLogger(__name__)


class OriginalDocx(object):
    def __init__(self, path: str, ask_function: FunctionType) -> None:
        self.paragraphs: List[Paragraph] = []
        doc = Document(path)
        for paragraph in doc.paragraphs:
            paragraph_obj = Paragraph()

            for run in paragraph.runs:
                paragraph_obj.add(run.text, run.italic)

            paragraph_obj.fix_spaces()
            paragraph_obj.fix_italic_boundaries()
            paragraph_obj.fix_quotes_and_dashes()
            paragraph_obj.fix_ticks(ask_function)

            LOG.debug(paragraph_obj.text)
            self.paragraphs.append(paragraph_obj)
