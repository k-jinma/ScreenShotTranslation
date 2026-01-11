# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # .envファイルは含めない（ユーザーが自分で設定する必要がある）
        # EasyOCRのモデルファイルを含める場合（オプション）
        # ('C:\\Users\\ユーザー名\\.EasyOCR\\model', '.EasyOCR/model'),
    ],
    hiddenimports=[
        # EasyOCRとその依存関係
        'easyocr',
        'torch',
        'torchvision',
        'cv2',
        'PIL',
        'numpy',
        'scipy',
        'skimage',
        # Deep Translator
        'deep_translator',
        # Google Generative AI
        'google.generativeai',
        'google.ai.generativelanguage',
        # その他
        'dotenv',
        'win32clipboard',
        'win32con',
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
    name='ScreenshotTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPXで圧縮（ファイルサイズを削減）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # コンソールウィンドウを非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # アイコンファイルがあれば指定: 'icon.ico'
)
