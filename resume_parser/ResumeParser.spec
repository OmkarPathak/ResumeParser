# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os
import sys

# Function to find package path
def get_package_path(package_name):
    import importlib
    try:
        module = importlib.import_module(package_name)
        return os.path.dirname(module.__file__)
    except ImportError:
        return None

# Manually define datas and hiddenimports
datas = [
    ('parser_app/templates', 'parser_app/templates'),
    ('parser_app/static', 'parser_app/static'),
    ('env/lib/python3.9/site-packages/en_core_web_sm', 'en_core_web_sm'),
    ('env/lib/python3.9/site-packages/spacy', 'spacy'),
]

binaries = []
hiddenimports = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parser_app',
    'parser_app.templatetags',
    'crispy_forms',
    'crispy_forms.templatetags.crispy_forms_tags', 
    'en_core_web_sm',
]

# Collect important packages
packages_to_collect = [
    'spacy', 
    'pyresparser', 
    'thinc', 
    'srsly', 
    'cymem', 
    'preshed', 
    'blis', 
    'crispy_forms'
]

for pkg in packages_to_collect:
    try:
        tmp_ret = collect_all(pkg)
        datas += tmp_ret[0]
        binaries += tmp_ret[1]
        hiddenimports += tmp_ret[2]
    except Exception as e:
        print(f"Warning: Could not collect {pkg}: {e}")

# Explicitly add crispy_forms templates if not found by collect_all
crispy_path = get_package_path('crispy_forms')
if crispy_path:
    datas.append((os.path.join(crispy_path, 'templates'), 'crispy_forms/templates'))

a = Analysis(
    ['manage.py'],
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
