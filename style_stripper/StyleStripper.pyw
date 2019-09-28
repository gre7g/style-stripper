import locale
import logging

from style_stripper.model.main_app import StyleStripperApp


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    locale.setlocale(locale.LC_NUMERIC, "")
    app = StyleStripperApp()
    app.init()
    app.MainLoop()
