# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['style_stripper\\MainApp.py'],
             pathex=['C:\\Users\\hafel\\Documents\\Projects\\style-stripper'],
             binaries=[],
             datas=[('README.md', '.'), ('style_stripper\\data\\lorem_ipsum.txt', 'data'), ('style_stripper\\docx_templates\\*.docx', 'docx_templates')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MainApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MainApp')
