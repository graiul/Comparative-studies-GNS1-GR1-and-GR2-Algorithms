# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Backtracking_STwig_Matching.py'],
             pathex=['C:\\Users\\Gheorghica Radu\\PycharmProjects\\STwig_pycharm\\To create executable file\\Backtracking_STwig_Matching'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Backtracking_STwig_Matching',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
