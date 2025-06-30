#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB文件合并工具
将多个EPUB文件按顺序合并成一个文件，保留原有的图片和文字，保持原有的顺序和位置
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import tempfile
from typing import List, Dict, Tuple
import argparse
import logging
import re
import urllib.parse

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EpubMerger:
    def __init__(self, language='zh-CN'):
        self.namespace = {'ns': 'http://www.idpf.org/2007/opf'}
        self.merged_content = []
        self.merged_resources = {}
        self.resource_counter = 1
        # 添加资源路径映射
        self.resource_mapping = {}  # 原始路径 -> 新路径
        self.id_mapping = {}  # 原始ID -> 新ID
        # 添加语言设置
        self.language = language
        # 添加文件名计数器，避免重名
        self.filename_counter = {}
        
    def extract_epub(self, epub_path: str) -> str:
        """解压EPUB文件到临时目录"""
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return temp_dir
    
    def parse_container_xml(self, temp_dir: str) -> str:
        """解析container.xml获取content.opf路径"""
        container_path = os.path.join(temp_dir, 'META-INF', 'container.xml')
        if not os.path.exists(container_path):
            raise FileNotFoundError(f"找不到container.xml文件: {container_path}")
        
        tree = ET.parse(container_path)
        root = tree.getroot()
        
        # 定义container.xml的命名空间
        container_ns = {'container': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        
        # 查找rootfile元素，尝试不同的方法
        rootfiles = root.findall('.//rootfile')
        if not rootfiles:
            # 尝试带命名空间的方法
            rootfiles = root.findall('.//container:rootfile', container_ns)
        
        for rootfile in rootfiles:
            full_path = rootfile.get('full-path')
            if full_path:
                return os.path.join(temp_dir, full_path)
        
        # 如果还是找不到，尝试直接查找
        for elem in root.iter():
            if elem.tag.endswith('rootfile') or 'rootfile' in elem.tag:
                full_path = elem.get('full-path')
                if full_path:
                    return os.path.join(temp_dir, full_path)
        
        raise ValueError("在container.xml中找不到rootfile")
    
    def parse_content_opf(self, opf_path: str) -> Tuple[List[str], Dict[str, str]]:
        """解析content.opf文件，获取spine顺序和manifest资源"""
        tree = ET.parse(opf_path)
        root = tree.getroot()
        
        # 获取manifest中的资源
        manifest = {}
        for item in root.findall('.//ns:item', self.namespace):
            item_id = item.get('id')
            href = item.get('href')
            media_type = item.get('media-type')
            if item_id and href:
                manifest[item_id] = {
                    'href': href,
                    'media-type': media_type
                }
        
        # 获取spine顺序
        spine = []
        for itemref in root.findall('.//ns:itemref', self.namespace):
            idref = itemref.get('idref')
            if idref in manifest:
                spine.append(idref)
        
        return spine, manifest
    
    def read_file_content(self, base_path: str, file_path: str) -> str:
        """读取文件内容"""
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def copy_resource(self, source_base: str, source_path: str, target_base: str, target_path: str):
        """复制资源文件"""
        source_full = os.path.join(source_base, source_path)
        target_full = os.path.join(target_base, target_path)
        
        # 确保目标目录存在
        os.makedirs(os.path.dirname(target_full), exist_ok=True)
        
        if os.path.exists(source_full):
            shutil.copy2(source_full, target_full)
            logger.info(f"复制资源: {source_path} -> {target_path}")
    
    def normalize_path(self, path: str, base_path: str) -> str:
        """标准化路径，处理各种相对路径情况"""
        if not path:
            return path
            
        original_path = path
        
        # 移除开头的 './'
        if path.startswith('./'):
            path = path[2:]
        
        # 处理绝对路径（相对于EPUB根目录）
        if path.startswith('/'):
            path = path[1:]
        
        # 处理包含 '../' 的路径
        if '../' in path:
            # 计算相对路径
            path_parts = path.split('/')
            base_parts = base_path.split(os.sep)
            
            # 移除路径中的 '..'
            while path_parts and path_parts[0] == '..':
                path_parts.pop(0)
                if base_parts:
                    base_parts.pop()
            
            # 重新组合路径
            if base_parts:
                path = os.path.join(*base_parts, *path_parts)
            else:
                path = '/'.join(path_parts)
        
        # 统一路径分隔符为 '/'
        path = path.replace('\\', '/')
        
        logger.debug(f"路径标准化: {original_path} -> {path}")
        return path
    
    def get_unique_filename(self, original_filename: str) -> str:
        """生成唯一的文件名，避免重名冲突"""
        name, ext = os.path.splitext(original_filename)
        if original_filename not in self.filename_counter:
            self.filename_counter[original_filename] = 1
            return original_filename
        else:
            self.filename_counter[original_filename] += 1
            return f"{name}_{self.filename_counter[original_filename]}{ext}"
    
    def update_html_references(self, html_content: str, base_path: str, resource_mapping: Dict) -> str:
        """更新HTML文件中的资源引用"""
        if not html_content:
            return html_content
            
        # 更新img标签的src属性
        def update_img_src(match):
            src = match.group(1)
            if src and not src.startswith(('http://', 'https://', 'data:')):
                # 处理相对路径
                if src.startswith('#'):
                    return match.group(0)  # 锚点链接，保持不变
                
                # 解析相对路径
                try:
                    # 标准化路径
                    normalized_path = self.normalize_path(src, base_path)
                    
                    # 查找对应的新路径
                    if normalized_path in resource_mapping:
                        new_path = resource_mapping[normalized_path]
                        logger.info(f"更新图片引用: {src} -> {new_path}")
                        return f'src="{new_path}"'
                    else:
                        # 尝试其他可能的路径变体
                        possible_paths = [
                            normalized_path,
                            src,
                            src.lstrip('./'),
                            src.lstrip('/'),
                            os.path.basename(src)
                        ]
                        
                        for test_path in possible_paths:
                            if test_path in resource_mapping:
                                new_path = resource_mapping[test_path]
                                logger.info(f"更新图片引用(变体): {src} -> {new_path}")
                                return f'src="{new_path}"'
                        
                        logger.warning(f"未找到资源映射: {normalized_path} (原始: {src})")
                        logger.debug(f"可用的资源映射键: {list(resource_mapping.keys())[:10]}...")
                except Exception as e:
                    logger.warning(f"更新图片引用失败: {src}, 错误: {e}")
            
            return match.group(0)
        
        # 使用正则表达式更新img标签
        html_content = re.sub(r'src=["\']([^"\']*)["\']', update_img_src, html_content, flags=re.IGNORECASE)
        
        # 更新CSS中的背景图片引用
        def update_css_background(match):
            url = match.group(1)
            if url and not url.startswith(('http://', 'https://', 'data:')):
                # 移除url()包装
                clean_url = url.strip('"\'')
                if clean_url.startswith('#'):
                    return match.group(0)  # 锚点链接，保持不变
                
                try:
                    # 标准化路径
                    normalized_path = self.normalize_path(clean_url, base_path)
                    
                    if normalized_path in resource_mapping:
                        new_path = resource_mapping[normalized_path]
                        logger.info(f"更新CSS背景图片: {clean_url} -> {new_path}")
                        return f'url("{new_path}")'
                    else:
                        # 尝试其他可能的路径变体
                        possible_paths = [
                            normalized_path,
                            clean_url,
                            clean_url.lstrip('./'),
                            clean_url.lstrip('/'),
                            os.path.basename(clean_url)
                        ]
                        
                        for test_path in possible_paths:
                            if test_path in resource_mapping:
                                new_path = resource_mapping[test_path]
                                logger.info(f"更新CSS背景图片(变体): {clean_url} -> {new_path}")
                                return f'url("{new_path}")'
                        
                        logger.warning(f"未找到CSS资源映射: {normalized_path} (原始: {clean_url})")
                except Exception as e:
                    logger.warning(f"更新CSS背景图片失败: {clean_url}, 错误: {e}")
            
            return match.group(0)
        
        # 更新CSS中的url()引用
        html_content = re.sub(r'url\(["\']?([^"\')\s]*)["\']?\)', update_css_background, html_content, flags=re.IGNORECASE)
        
        return html_content
    
    def merge_epub(self, epub_files: List[str], output_path: str):
        """合并多个EPUB文件"""
        logger.info(f"开始合并 {len(epub_files)} 个EPUB文件")
        
        # 创建临时目录用于合并
        merged_temp_dir = tempfile.mkdtemp()
        
        try:
            # 创建META-INF目录
            meta_inf_dir = os.path.join(merged_temp_dir, 'META-INF')
            os.makedirs(meta_inf_dir, exist_ok=True)
            
            # 创建container.xml
            container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
            
            with open(os.path.join(meta_inf_dir, 'container.xml'), 'w', encoding='utf-8') as f:
                f.write(container_xml)
            
            # 合并所有EPUB文件
            all_spine_items = []
            all_manifest = {}
            all_resources = {}
            
            # 重置全局资源映射
            self.resource_mapping = {}
            self.id_mapping = {}
            self.filename_counter = {}
            
            for i, epub_file in enumerate(epub_files):
                logger.info(f"处理第 {i+1} 个文件: {epub_file}")
                
                # 解压EPUB
                temp_dir = self.extract_epub(epub_file)
                
                try:
                    # 解析content.opf
                    opf_path = self.parse_container_xml(temp_dir)
                    spine, manifest = self.parse_content_opf(opf_path)
                    
                    # 获取基础路径
                    base_path = os.path.dirname(opf_path)
                    
                    # 首先处理所有资源（图片、CSS等），建立映射关系
                    for item_id, item_info in manifest.items():
                        if item_id not in spine:  # 不是spine项目
                            href = item_info['href']
                            media_type = item_info['media-type']
                            
                            # 生成新的ID
                            new_id = f"item_{self.resource_counter:04d}"
                            self.resource_counter += 1
                            
                            # 生成唯一的文件名
                            original_filename = os.path.basename(href)
                            unique_filename = self.get_unique_filename(original_filename)
                            new_href = f"resources/{unique_filename}"
                            
                            # 复制文件到resources目录
                            self.copy_resource(base_path, href, merged_temp_dir, new_href)
                            
                            # 建立映射关系（使用文件内的相对路径）
                            self.resource_mapping[href] = new_href
                            self.id_mapping[item_id] = new_id
                            
                            logger.info(f"资源映射: {href} -> {new_href} (类型: {media_type})")
                            
                            all_resources[new_id] = {
                                'href': new_href,
                                'media_type': media_type,
                                'original_href': href
                            }
                    
                    # 然后处理spine项目（HTML文件）
                    for item_id in spine:
                        if item_id in manifest:
                            item_info = manifest[item_id]
                            href = item_info['href']
                            media_type = item_info['media-type']
                            
                            # 生成新的ID
                            new_id = f"item_{self.resource_counter:04d}"
                            self.resource_counter += 1
                            
                            # 读取文件内容
                            content = self.read_file_content(base_path, href)
                            
                            # 如果是HTML文件，需要更新资源引用
                            if media_type == 'application/xhtml+xml':
                                logger.info(f"处理HTML文件: {href}")
                                # 使用全局资源映射
                                content = self.update_html_references(content, base_path, self.resource_mapping)
                            
                            # 保存到合并的资源中
                            all_resources[new_id] = {
                                'content': content,
                                'media_type': media_type,
                                'original_href': href
                            }
                            
                            all_spine_items.append(new_id)
                
                finally:
                    # 清理临时目录
                    shutil.rmtree(temp_dir)
            
            # 创建合并后的content.opf
            self.create_merged_opf(merged_temp_dir, all_spine_items, all_resources)
            
            # 创建EPUB文件
            self.create_epub(merged_temp_dir, output_path)
            
            logger.info(f"合并完成，输出文件: {output_path}")
            
        finally:
            # 清理临时目录
            shutil.rmtree(merged_temp_dir)
    
    def create_merged_opf(self, temp_dir: str, spine_items: List[str], resources: Dict):
        """创建合并后的content.opf文件"""
        opf_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>合并的EPUB文件</dc:title>
        <dc:creator>EPUB合并工具</dc:creator>
        <dc:language>{self.language}</dc:language>
        <dc:identifier id="uid">merged-epub-{self.resource_counter}</dc:identifier>
    </metadata>
    <manifest>
'''
        
        # 添加所有资源到manifest
        for item_id, item_info in resources.items():
            if 'href' in item_info:
                # 文件资源
                opf_content += f'        <item id="{item_id}" href="{item_info["href"]}" media-type="{item_info["media_type"]}"/>\n'
            else:
                # 内容资源
                opf_content += f'        <item id="{item_id}" href="{item_id}.xhtml" media-type="{item_info["media_type"]}"/>\n'
        
        opf_content += '''    </manifest>
    <spine>
'''
        
        # 添加spine项目
        for item_id in spine_items:
            opf_content += f'        <itemref idref="{item_id}"/>\n'
        
        opf_content += '''    </spine>
</package>'''
        
        # 写入content.opf
        with open(os.path.join(temp_dir, 'content.opf'), 'w', encoding='utf-8') as f:
            f.write(opf_content)
        
        # 写入所有内容文件
        for item_id, item_info in resources.items():
            if 'content' in item_info:
                content_file = os.path.join(temp_dir, f'{item_id}.xhtml')
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(item_info['content'])
    
    def create_epub(self, temp_dir: str, output_path: str):
        """创建最终的EPUB文件"""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

def main():
    parser = argparse.ArgumentParser(description='合并多个EPUB文件')
    parser.add_argument('input_files', nargs='+', help='输入的EPUB文件列表')
    parser.add_argument('-o', '--output', default='merged.epub', help='输出文件名')
    parser.add_argument('-l', '--language', default='zh-CN', 
                       help='输出EPUB的语言代码 (默认: zh-CN, 例如: en-US, ja-JP, ko-KR)')
    
    args = parser.parse_args()
    
    # 检查输入文件
    for epub_file in args.input_files:
        if not os.path.exists(epub_file):
            logger.error(f"文件不存在: {epub_file}")
            return
    
    # 创建合并器并执行合并
    merger = EpubMerger(language=args.language)
    try:
        merger.merge_epub(args.input_files, args.output)
        print(f"✅ 合并成功！输出文件: {args.output}")
        print(f"🌍 语言设置: {args.language}")
    except Exception as e:
        logger.error(f"合并失败: {str(e)}")
        print(f"❌ 合并失败: {str(e)}")

if __name__ == "__main__":
    main() 