#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS构建脚本
将rss目录下的所有子文件夹中的markdown和xml文件转换为rss.xml文件
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

# 配置
RSS_DIR = 'rss'
OUTPUT_FILE = 'rss.xml'

# RSS头部模板
RSS_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>KINGTU 企业信息</title>
    <link>https://kt.github.io/</link>
    <description>KT 技术与服务网站的 RSS 订阅源。订阅此源获取最新项目、案例、知识分享更新。</description>
    <language>zh-cn</language>
    <lastBuildDate>{last_build_date}</lastBuildDate>
    <atom:link href="https://kt.github.io/rss.xml" rel="self" type="application/rss+xml" />

    <!-- 自动生成：请勿手动编辑 -->
    <!-- 由 build_rss.py 脚本从 rss/ 目录合并生成 -->
    <!-- 最后更新时间: {update_time} -->

'''

RSS_FOOTER = '''
  </channel>
</rss>
'''

def parse_pubdate(pubdate_str):
    """解析pubDate字符串为datetime对象"""
    try:
        # 尝试解析RSS格式的日期
        dt = datetime.strptime(pubdate_str, '%a, %d %b %Y %H:%M:%S %z')
        # 移除时区信息，使其成为offset-naive
        return dt.replace(tzinfo=None)
    except ValueError:
        # 尝试其他格式
        try:
            return datetime.strptime(pubdate_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.now()

def parse_markdown(file_path):
    """解析markdown文件，提取标题、日期和内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s+(.*)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "未命名"
    
    # 提取日期（从标题或文件名）
    date_match = re.search(r'\d{4}-\d{2}', title)
    if not date_match:
        # 从文件名提取日期
        filename = os.path.basename(file_path)
        date_match = re.search(r'\d{4}\d{2}\d{2}', filename)
    
    date_str = date_match.group(0) if date_match else datetime.now().strftime('%Y%m%d')
    # 格式化日期为RSS格式
    if len(date_str) == 8:
        date_obj = datetime.strptime(date_str, '%Y%m%d')
    else:
        date_obj = datetime.strptime(date_str, '%Y-%m')
    pubdate_str = date_obj.strftime('%a, %d %b %Y %H:%M:%S +0800')
    
    # 提取内容，转换为HTML
    # 处理标题
    html_content = re.sub(r'^##\s+(.*)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    html_content = re.sub(r'^#\s+(.*)$', r'', html_content, flags=re.MULTILINE)
    # 处理图片
    html_content = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" style="max-width: 100%; height: auto;">', html_content)
    # 处理段落
    html_content = re.sub(r'\n\n(.*?)\n\n', r'<p>\1</p>', html_content, flags=re.DOTALL)
    # 清理多余的空行
    html_content = re.sub(r'\n+', r'<br>', html_content)
    
    # 生成item元素
    item = ET.Element('item')
    
    title_elem = ET.SubElement(item, 'title')
    title_elem.text = title
    
    link_elem = ET.SubElement(item, 'link')
    # 生成唯一链接
    link = f"https://kt.github.io/post/{date_str}-{re.sub(r'\s+', '-', title.lower())}.html"
    link_elem.text = link
    
    description_elem = ET.SubElement(item, 'description')
    # 直接设置文本内容，让ElementTree自动处理
    description_elem.text = html_content
    
    pubdate_elem = ET.SubElement(item, 'pubDate')
    pubdate_elem.text = pubdate_str
    
    guid_elem = ET.SubElement(item, 'guid', {'isPermaLink': 'true'})
    guid_elem.text = link
    
    return date_obj, ET.tostring(item, encoding='unicode')

def parse_xml(file_path):
    """解析xml文件，提取item元素"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 为没有根元素的XML添加临时根元素
        if not content.strip().startswith('<'):
            print(f"文件 {os.path.basename(file_path)} 格式不正确，跳过处理")
            return []
        
        # 检查是否有根元素
        root_match = re.match(r'^\s*<([a-zA-Z0-9_:]+)', content)
        if not root_match:
            # 添加临时根元素
            content = f'<root>{content}</root>'
        
        # 解析XML内容
        root = ET.fromstring(content)
        
        # 查找所有item元素
        items = []
        for item in root.findall('.//item'):
            # 提取pubDate
            pubdate_elem = item.find('pubDate')
            if pubdate_elem is not None:
                pubdate_str = pubdate_elem.text
                pubdate = parse_pubdate(pubdate_str)
                items.append((pubdate, ET.tostring(item, encoding='unicode')))
        return items
    except Exception as e:
        print(f"处理文件 {os.path.basename(file_path)} 时出错: {e}")
        return []

def main():
    """主函数"""
    print("开始构建RSS文件...")
    
    # 创建rss目录（如果不存在）
    if not os.path.exists(RSS_DIR):
        os.makedirs(RSS_DIR)
        print(f"创建了 {RSS_DIR} 目录")
    
    # 收集所有item元素
    items = []
    
    # 遍历rss目录下的所有子文件夹
    for root_dir, dirs, files in os.walk(RSS_DIR):
        # 跳过根目录
        if root_dir == RSS_DIR:
            continue
        
        print(f"处理目录: {os.path.basename(root_dir)}")
        
        # 处理目录中的文件
        for filename in files:
            if filename.endswith('.md'):
                # 处理markdown文件
                file_path = os.path.join(root_dir, filename)
                print(f"处理文件: {filename}")
                try:
                    pubdate, item_str = parse_markdown(file_path)
                    items.append((pubdate, item_str))
                except Exception as e:
                    print(f"处理markdown文件 {filename} 时出错: {e}")
            elif filename.endswith('.xml'):
                # 处理xml文件
                file_path = os.path.join(root_dir, filename)
                print(f"处理文件: {filename}")
                xml_items = parse_xml(file_path)
                items.extend(xml_items)
    
    # 按日期排序（最新的在前）
    items.sort(key=lambda x: x[0], reverse=True)
    
    # 生成最终的RSS内容
    now = datetime.now()
    last_build_date = now.strftime('%a, %d %b %Y %H:%M:%S +0800')
    update_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    rss_content = RSS_HEADER.format(last_build_date=last_build_date, update_time=update_time)
    
    # 添加排序后的item
    for _, item_str in items:
        rss_content += f"    {item_str.strip()}\n\n"
    
    rss_content += RSS_FOOTER
    
    # 写入输出文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"构建完成！生成了 {OUTPUT_FILE} 文件")
    print(f"共包含 {len(items)} 个条目")

if __name__ == '__main__':
    main()