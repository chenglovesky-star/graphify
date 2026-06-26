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
from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_data_files,
    collect_all,
)

block_cipher = None

# Hidden imports: 显式列出 PyInstaller 静态分析可能漏掉的包
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

# openai / tiktoken 用 collect_all 自动拉所有子模块+资源(更可靠)
# PyInstaller hiddenimports 不会拉传递依赖;collect_all 一次性打包
openai_datas, openai_binaries, openai_hidden = collect_all('openai')
tiktoken_datas, tiktoken_binaries, tiktoken_hidden = collect_all('tiktoken')
httpx_datas, httpx_binaries, httpx_hidden = collect_all('httpx')

hidden += openai_hidden + tiktoken_hidden + httpx_hidden
# 注: openai/tiktoken/httpx 的 datas 和 binaries 由 Analysis 接收

a = Analysis(
    ['graphify/__main__.py'],
    pathex=[],
    binaries=openai_binaries + tiktoken_binaries + httpx_binaries,
    datas=openai_datas + tiktoken_datas + httpx_datas,
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
    strip=False,           # Windows 上 strip=True 会导致 python311.dll 加载失败（已知问题）
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