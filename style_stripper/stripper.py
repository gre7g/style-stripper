"""DOCX Stripper"""

from docopt import docopt
import logging
import os
from schema import Schema, SchemaError
import sys

from style_stripper import __version__
from style_stripper.constants import CONSTANTS
from style_stripper.original_docx import OriginalDocx
from style_stripper.paragraph import Paragraph
from style_stripper.template import Template

# Constants:
LOG = logging.getLogger(__name__)


def ask(paragraph: Paragraph, offset: int) -> bool:
    # TODO: Make interactive
    LOG.warning("ask offset=%d text=%r", offset, paragraph.text)
    return True


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
    document = OriginalDocx(arguments["SOURCE"], ask)
    count_of_symbolic, count_of_blanks = document.find_divider_candidates()
    if count_of_symbolic:
        LOG.info("Found symbolic dividers, will not presume the blanks are meaningful")
        document.replace_symbolic()
        document.remove_blanks()
    elif CONSTANTS.DIVIDER.BLANK_PARAGRAPH_IF_NO_OTHER and count_of_blanks:
        if count_of_blanks < CONSTANTS.DIVIDER.MAX_BLANK_PARAGRAPH_DIVIDERS:
            LOG.info("Found no symbolic divers, will presume blanks are meaningful")
        else:
            LOG.info("Found too many blanks to presume they are dividers, will ignore them")
            document.remove_blanks()
    template = Template(CONSTANTS.PAGE.TEMPLATE)
    for paragraph in document.paragraphs:
        if paragraph.divider:
            style = "Separator"
        else:
            style = None
        template.add_content(paragraph.text, style)
    template.save_as(r"..\temp.docx")

    return 0


if __name__ == "__main__":
    main()
    # TODO: Detect chapters
    # TODO: Detect The End
