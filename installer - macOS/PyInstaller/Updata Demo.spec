# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/PARRY/Desktop/ctrl-z/src/main/python/main.py'],
             pathex=['/Users/PARRY/Desktop/ctrl-z/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/PARRY/Desktop/ctrl-z/venv/lib/python3.6/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/PARRY/Desktop/ctrl-z/target/PyInstaller/fbs_pyinstaller_hook.py'],
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
          console=False , icon='/Users/PARRY/Desktop/ctrl-z/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Updata Demo')
app = BUNDLE(coll,
             name='Updata Demo.app',
             icon='/Users/PARRY/Desktop/ctrl-z/target/Icon.icns',
             bundle_identifier=None)
