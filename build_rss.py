#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS构建脚本
将rss目录下的分类XML文件合并成一个完整的rss.xml文件
"""

import os
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
        return datetime.strptime(pubdate_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        # 尝试其他格式
        try:
            return datetime.strptime(pubdate_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.now()

def main():
    """主函数"""
    print("开始构建RSS文件...")
    
    # 创建rss目录（如果不存在）
    if not os.path.exists(RSS_DIR):
        os.makedirs(RSS_DIR)
        print(f"创建了 {RSS_DIR} 目录")
    
    # 收集所有item元素
    items = []
    
    # 遍历rss目录下的所有XML文件
    for filename in os.listdir(RSS_DIR):
        if filename.endswith('.xml'):
            file_path = os.path.join(RSS_DIR, filename)
            print(f"处理文件: {filename}")
            
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 为没有根元素的XML添加临时根元素
                if not content.strip().startswith('<'):
                    print(f"文件 {filename} 格式不正确，跳过处理")
                    continue
                
                # 检查是否有根元素
                import re
                root_match = re.match(r'^\s*<([a-zA-Z0-9_:]+)', content)
                if not root_match:
                    # 添加临时根元素
                    content = f'<root>{content}</root>'
                
                # 解析XML内容
                root = ET.fromstring(content)
                
                # 查找所有item元素
                for item in root.findall('.//item'):
                    # 提取pubDate
                    pubdate_elem = item.find('pubDate')
                    if pubdate_elem is not None:
                        pubdate_str = pubdate_elem.text
                        pubdate = parse_pubdate(pubdate_str)
                        items.append((pubdate, ET.tostring(item, encoding='unicode')))
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
    
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