#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建RSS条目脚本
在rss目录下创建一个以当前日期时间命名的文件夹，并在其中生成一个md文件
"""

import os
from datetime import datetime

# 配置
RSS_DIR = 'rss'

# 获取当前日期时间
now = datetime.now()
# 生成文件夹名称：年月日时分
folder_name = now.strftime('%Y%m%d%H%M')
# 生成文件夹路径
folder_path = os.path.join(RSS_DIR, folder_name)

# 创建文件夹
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"创建了文件夹: {folder_path}")
else:
    print(f"文件夹已存在: {folder_path}")

# 生成md文件名
md_filename = f"{folder_name}.md"
md_file_path = os.path.join(folder_path, md_filename)

# 生成md文件内容
md_content = f"""# {now.strftime('%Y年%m月%d日 %H:%M')} - 新条目

## 标题

内容描述

## 图片

![图片描述]({folder_name}/image.jpg)
"""

# 写入md文件
with open(md_file_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"创建了md文件: {md_file_path}")
print("\n请编辑此md文件添加具体内容，然后运行 build_rss.bat 生成RSS文件")