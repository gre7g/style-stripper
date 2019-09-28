from distutils.core import setup
import py2exe


setup(
    name="Style Stripper",
    version="1.0",
    description="Strips chaff from .docx files and formats them in a standard manner",
    author="Gre7g Luterman",
    author_email="gre7g.luterman@gmail.com",
    url="https://github.com/gre7g/style-stripper",
    packages=["style_stripper"],
    console=["MainApp.py"],
)
