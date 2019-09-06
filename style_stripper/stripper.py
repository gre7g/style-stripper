"""DOCX Stripper"""

from docopt import docopt
from docx import Document
import logging
import os
import re
from schema import Schema, SchemaError
from spellchecker import SpellChecker
import sys
from typing import List

from style_stripper import __version__
from style_stripper.constants import CONSTANTS

# Constants:
SEARCH_LEADING_WHITESPACE = re.compile(r"^\s+")
SEARCH_TRAILING_WHITESPACE = re.compile(r"\s+$")
SEARCH_DOUBLE_WHITESPACE = re.compile(r"\s{2,}")
SEARCH_ANY_QUOTE = re.compile('["“”]')
SEARCH_QUOTES_OR_TICKS = re.compile(r"[“”‘’]")
LOG = logging.getLogger(__name__)


class Run(object):
    def __init__(self, text: str, italic: bool) -> None:
        self.text, self.italic = text, italic

    def __str__(self) -> str:
        return ("<i>%s</i>" % self.text) if self.italic else self.text

    def __repr__(self) -> str:
        return repr(("<i>%s</i>" % self.text) if self.italic else self.text)


class Paragraph(object):
    runs: List[Run]

    def __init__(self) -> None:
        self.runs = []

    def add_run(self, text: str, italic: bool) -> None:
        self.runs.append(Run(text, italic))

    def fix_spaces(self) -> None:
        if CONSTANTS.SPACES.PURGE_LEADING_WHITESPACE:
            while self.runs:
                match = SEARCH_LEADING_WHITESPACE.search(self.runs[0].text)
                if match:
                    self.runs[0].text = self.runs[0].text[match.end():]
                    if self.runs[0].text:
                        break
                    else:
                        del self.runs[0]
                else:
                    break

        if CONSTANTS.SPACES.PURGE_TRAILING_WHITESPACE:
            while self.runs:
                match = SEARCH_TRAILING_WHITESPACE.search(self.runs[-1].text)
                if match:
                    self.runs[-1].text = self.runs[-1].text[:match.start()]
                    if self.runs[-1].text:
                        break
                    else:
                        del self.runs[-1]
                else:
                    break

        if CONSTANTS.SPACES.PURGE_DOUBLE_SPACES:
            run_num = 0
            while run_num < len(self.runs):
                run = self.runs[run_num]
                run.text = SEARCH_DOUBLE_WHITESPACE.sub(" ", run.text)

                # Compress space at end of this run and beginning of next run
                if run_num < (len(self.runs) - 1):
                    next_run = self.runs[run_num + 1]

                    # Merge runs if possible
                    if run.italic == next_run.italic:
                        run.text += next_run.text
                        del self.runs[run_num + 1]
                        continue

                    match1 = SEARCH_TRAILING_WHITESPACE.search(run.text)
                    match2 = SEARCH_LEADING_WHITESPACE.search(next_run.text)
                    if match1 and match2:
                        run.text = run.text[:match1.start()]
                        next_run.text = " " + next_run.text[match2.end():]

                if run.text:
                    run_num += 1
                else:
                    del self.runs[run_num]

    def fix_quotes(self) -> None:
        if CONSTANTS.QUOTES.CONVERT_TO_CURLY:
            even = True
            for run in self.runs:
                for match in SEARCH_ANY_QUOTE.finditer(run.text):
                    even = not even
                    quote = '”' if even else '“'
                    run.text = run.text[:match.start()] + quote + run.text[match.end():]

    def fix_ticks(self):
        if CONSTANTS.QUOTES.CONVERT_TO_CURLY:

    def __str__(self) -> str:
        return "".join(str(run) for run in self.runs)

    def __repr__(self) -> str:
        return repr(self.runs)


class StrippedDocx(object):
    def __init__(self, path: str) -> None:
        document = Document(path)
        for paragraph in document.paragraphs:
            paragraph_obj = Paragraph()
            for run in paragraph.runs:
                paragraph_obj.add_run(run.text, run.italic)
            paragraph_obj.fix_spaces()
            paragraph_obj.fix_quotes()
            print(repr(paragraph_obj))


def main() -> int:  # Exit code
    """DOCX Stripper

Usage:
    %(prog)s -h|--help
    %(prog)s -V|--version
    %(prog)s [-v] SOURCE

Options:
-h --help                 Show help
-v --verbose              Verbose output
-V --version              Display version information and quit

"""

    SCHEMA = Schema({
        "--help": bool,
        "--verbose": bool,
        "--version": bool,
        "SOURCE": str,
    })
    # Parse arguments
    arguments = docopt(main.__doc__ % {"prog": os.path.basename(__file__)}, version=__version__)

    # Validation
    try:
        SCHEMA.validate(arguments)
    except SchemaError as error:
        sys.exit(error)

    # Logging on verbose
    logging.basicConfig(level=logging.DEBUG if arguments["--verbose"] else logging.INFO)

    # Import document
    document = StrippedDocx(arguments["SOURCE"])

    return 0


if __name__ == "__main__":
    s = SpellChecker(distance=1)
    print(s.unknown(['this', 'is', 'a', 'baad', 'word']))
    main()
