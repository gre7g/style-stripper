::    --console
pyinstaller "style_stripper\StyleStripper.py" ^
    --noconfirm ^
    --windowed ^
    --add-data="README.md;." ^
    --add-data="style_stripper\data\lorem_ipsum.txt;data" ^
    --add-data="style_stripper\docx_templates\*.docx;docx_templates"
