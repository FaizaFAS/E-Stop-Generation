# -*- mode: python -*-

block_cipher = None


a = Analysis(['E-Stop_Generator.py'],
             pathex=['C:\\Users\\youf\\Desktop\\E-Stop Generation\\To Compile'],
             binaries=[],
             hookspath=None)
a.datas += [('E00 - Blank 640x480.xml', 'C:\\Users\\youf\\Desktop\\E-Stop Generation\\E00 - Blank 640x480.xml', 'DATA')]
a.datas += [('E00 - Blank 1280x800.xml', 'C:\\Users\\youf\\Desktop\\E-Stop Generation\\E00 - Blank 1280x800.xml', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='E-Stop_Generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
