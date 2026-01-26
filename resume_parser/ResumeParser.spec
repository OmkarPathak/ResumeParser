# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os
import sys

# Function to find package path
def get_package_path(package_name):
    import importlib
    try:
        module = importlib.import_module(package_name)
        # Handle cases where module is a namespace package or has no __file__
        if hasattr(module, '__file__'):
             return os.path.dirname(module.__file__)
        return os.path.dirname(module.__path__[0])
    except ImportError:
        return None

# Manually define datas and hiddenimports
datas = [
    ('parser_app/templates', 'parser_app/templates'),
    ('parser_app/static', 'parser_app/static'),
    ('models', 'models'), # Include AI models at root (matched with settings.BASE_DIR)
    ('db.sqlite3', '.'),
]

binaries = []
hiddenimports=[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'parser_app',
    'whitenoise.middleware',
    'whitenoise',
    # AI Dependencies
    'llama_cpp', 
    'huggingface_hub',
    'crispy_forms.templatetags.crispy_forms_tags', 
    'webview',
]

# Packages to specifically handle
packages_to_collect = [
    'crispy_forms',
    'docx2txt',
    'pdfminer',
    'llama_cpp', # Explicitly collect to get libllama.dylib
]

# Dynamic collection
for pkg in packages_to_collect:
    try:
        tmp_ret = collect_all(pkg)
        datas += tmp_ret[0]
        binaries += tmp_ret[1]
        hiddenimports += tmp_ret[2]
    except Exception as e:
        print(f"Warning: Could not collect {pkg}: {e}")

a = Analysis(
    ['desktop_main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='ResumeParser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ResumeParser',
)
