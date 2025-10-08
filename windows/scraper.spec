# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../config', 'config'),
        ('../src', 'src'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'customtkinter',
        'matplotlib.backends.backend_tkagg',
        'seaborn',
        'pandas',
        'requests',
        'tqdm',
        'python-dotenv',
        'openpyxl',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeywordPositionScraper',
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
    icon=None,
)