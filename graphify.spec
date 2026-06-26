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

# onedir 模式(目录式): 不打 onefile, 而是产出一个 graphify/ 目录 + 主 binary
# 为什么不用 onefile:
#   1. PyInstaller onefile 把内容解包到 _MEIPASS 临时目录,graphify 用 multiprocessing
#      fork 子进程,子进程找不到原始 binary 路径 → 报 "unknown command --multiprocessing-fork"
#   2. onedir 模式 binary 就在固定位置,multiprocessing 工作正常
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,    # binaries 放 COLLECT,不在 EXE 里(onedir 关键)
    name='graphify',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
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
    name='graphify',
)