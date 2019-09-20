from docx import Document
from typing import Dict, Any


def fetch_docx_details(
    path: str  # Path to file
) -> Dict[str, Any]:
    """Fetch details from a .docx template."""
    doc = Document(path)

    # Basic info we need can be found in the first (only) section
    first_section = doc.sections[0]
    details = {
        "comments": doc.core_properties.comments,
        "different_first_page_header_footer": bool(first_section.different_first_page_header_footer),
        "page_height": first_section.page_height,
        "page_width": first_section.page_width,
        "top_margin": first_section.top_margin,
        "bottom_margin": first_section.bottom_margin,
        "left_margin": first_section.left_margin,
        "right_margin": first_section.right_margin,
        "header_distance": first_section.header_distance,
        "footer_distance": first_section.footer_distance,
        "gutter": first_section.gutter
    }

    # Map the styles into a dictionary so we can find one at will
    styles_by_name = {style.name: style for style in doc.styles}

    # Look up some info on the following styles:
    for name in ["Normal", "Heading 1", "Heading 2", "Header", "Footer", "Separator", "First Paragraph"]:
        details[name] = {}
        # Items we want:
        for attr, func in [
            ("font", lambda style: style.font.name),
            ("font_size", lambda style: style.font.size),
            ("italic", lambda style: style.font.italic),
            ("bold", lambda style: style.font.bold),
            ("alignment", lambda style: style.paragraph_format.alignment),
            ("space_before", lambda style: style.paragraph_format.space_before),
            ("space_after", lambda style: style.paragraph_format.space_after),
            ("first_line_indent", lambda style: style.paragraph_format.first_line_indent),
            ("line_spacing", lambda style: style.paragraph_format.line_spacing)
        ]:
            current_style = styles_by_name[name]
            while True:
                # Save it
                value = func(current_style)
                details[name][attr] = value

                # None indicates that the style doesn't override settings in the base style. For None values, recurse
                # into the base styles to find an actual value
                if value is None:
                    if current_style.base_style is None:
                        # Ran out of styles to check. Just leave the value None.
                        break
                    else:
                        current_style = styles_by_name[current_style.base_style.name]
                else:
                    # Found one!
                    break

    return details
