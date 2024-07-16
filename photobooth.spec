# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['photobooth.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/grego/miniconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml', 'cv2/data'), ('photo.wav', '.')],
    hiddenimports=['pyimod02_importers', 'pep517', 'pygame.fastevent', 'pygame.overlay', 'pygrabber.dshow_graph', 'comtypes.stream'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='photobooth',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
