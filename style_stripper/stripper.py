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

    # Convert dividers
    count_of_symbolic, count_of_blanks = document.find_divider_candidates()
    if count_of_symbolic:
        LOG.info("Found symbolic dividers, will not presume the blanks are meaningful")
        document.replace_symbolic()
        document.remove_blanks()
    elif CONSTANTS.DIVIDER.BLANK_PARAGRAPH_IF_NO_OTHER and count_of_blanks:
        if count_of_blanks < CONSTANTS.DIVIDER.MAX_BLANK_PARAGRAPH_DIVIDERS:
            LOG.info("Found no symbolic dividers, will presume blanks are meaningful")
            document.replace_blanks()
        else:
            LOG.info("Found too many blanks to presume they are dividers, will ignore them")
            document.remove_blanks()

    # Convert headings
    part, chapter, end = document.find_heading_candidates()
    part_style = chapter_style = end_style = None
    if part and CONSTANTS.HEADINGS.STYLE_PART:
        part_style = CONSTANTS.STYLING.NAMES.HEADING1
        if CONSTANTS.HEADINGS.STYLE_CHAPTER:
            chapter_style = CONSTANTS.STYLING.NAMES.HEADING2
    elif CONSTANTS.HEADINGS.STYLE_CHAPTER:
        chapter_style = CONSTANTS.STYLING.NAMES.HEADING1
    if CONSTANTS.HEADINGS.STYLE_THE_END:
        end_style = CONSTANTS.STYLING.NAMES.THE_END
    document.style_headings(part_style, chapter_style, end_style)

    # Clean up
    document.remove_dividers_before_headings()

    # Open a template file to format the output
    template = Template(CONSTANTS.PAGE.TEMPLATE)

    # Dump paragraphs into the template
    for paragraph in document.paragraphs:
        # May need to insert breaks before the headings
        if paragraph.style in [CONSTANTS.STYLING.NAMES.HEADING1, CONSTANTS.STYLING.NAMES.HEADING2]:
            if CONSTANTS.HEADINGS.BREAK_BEFORE_HEADING is not None:
                if CONSTANTS.HEADINGS.HEADER_FOOTER_AFTER_BREAK:
                    template.add_page_break()
                else:
                    # template.add_content()
                    template.add_content()
                    template.add_section(CONSTANTS.HEADINGS.BREAK_BEFORE_HEADING)

        template.add_content(paragraph.text, paragraph.style)

    # Save the resulting file
    template.save_as(r"..\temp.docx")

    return 0


if __name__ == "__main__":
    main()
