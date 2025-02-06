# -*- mode: python -*-

block_cipher = None


a = Analysis(['pfpanel.py'],
             pathex=[],
             binaries=[],
             datas=[ ('templates', 'templates', 'FOLDER') ], # 添加 templates 文件夹作为数据文件
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pfpanel', # 可执行文件名，可以自定义
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon=None) # console=True 表示创建控制台应用，icon 可以设置图标
