# -*- mode: python ; coding: utf-8 -*-
# graphify.spec - PyInstaller spec for building single-binary distribution
#
# Build: pyinstaller graphify.spec
# Output: dist/graphify (linux/mac) or dist/graphify.exe (windows)
#
# This produces a single-file executable that bundles the Python interpreter
# plus the graphify CLI, eliminating the need for users to install Python.
# Used by second-brain-installer to ship graphify as a self-contained binary.

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Hidden imports: explicit tree-sitter language packages that PyInstaller's
# static analysis misses. Each corresponds to a dependency in pyproject.toml.
hidden = [
    'graphify',
    'graphify.__main__',
    'tree_sitter',
]
for lang in [
    'python', 'javascript', 'typescript', 'tsx',
    'go', 'rust', 'java', 'groovy',
    'c', 'cpp', 'ruby', 'c_sharp',
    'kotlin', 'scala', 'php', 'swift',
    'lua', 'zig', 'powershell', 'elixir',
    'objc', 'julia', 'verilog', 'fortran',
    'bash', 'json',
]:
    hidden.append(f'tree_sitter_{lang}')

a = Analysis(
    ['graphify/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Standard library bloat
        'tkinter', 'test', 'unittest', 'pydoc', 'doctest',
        'xmlrpc', 'pdb',
        # Heavy optional deps not used by default `graphify` CLI
        # (kept in pyproject.toml as optional-dependencies)
        'matplotlib', 'numpy.f2py', 'scipy',
        'pandas', 'PyQt5', 'PyQt6', 'wx',
    ],
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
    a.datas,
    [],
    name='graphify',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,            # Strip symbols on linux/mac (smaller binary)
    upx=False,             # UPX compression is unstable across platforms, skip
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)