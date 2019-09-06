"""DOCX Stripper"""

from docopt import docopt
from docx import Document
import logging
import os
from schema import Schema, SchemaError
import sys

from style_stripper import __version__

LOG = logging.getLogger(__name__)


class StrippedDocx(object):
    def __init__(self, path) -> None:
        document = Document(path)
        for paragraph in document.paragraphs:
            text = "".join(run.text for run in paragraph.runs)
            print(text)


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
    main()
