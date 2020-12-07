# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\Users\\eshan\\UCLA Drive\\Programming\\ytp-bootcamp\\azure\\solution\\src\\main\\python\\main.py'],
             pathex=['D:\\Users\\eshan\\UCLA Drive\\Programming\\ytp-bootcamp\\azure\\solution\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['d:\\users\\eshan\\ucla drive\\programming\\ytp-bootcamp\\azure\\solution\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['D:\\Users\\eshan\\UCLA Drive\\Programming\\ytp-bootcamp\\azure\\solution\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
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
          name='Updata Demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='D:\\Users\\eshan\\UCLA Drive\\Programming\\ytp-bootcamp\\azure\\solution\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Updata Demo')
