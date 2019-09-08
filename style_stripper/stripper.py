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
    template = Template(CONSTANTS.PAGE.TEMPLATE)
    for paragraph in document.paragraphs:
        template.add_content(paragraph.text)
    template.save_as(r"..\temp.docx")

    return 0


if __name__ == "__main__":
    main()
