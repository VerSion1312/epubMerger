#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB文件合并工具 - 现代化GUI版本
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from epub_merger import EpubMerger
import threading
from datetime import datetime

class ModernEpubMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EPUB文件合并工具")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 现代化颜色主题
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#64748b', 
            'success': '#059669',
            'warning': '#d97706',
            'error': '#dc2626',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text': '#1e293b',
            'text_secondary': '#64748b'
        }
        
        # 多语言支持
        self.current_language = 'zh-CN'
        self.languages = {
            'zh-CN': '中文 (简体)',
            'zh-TW': '中文 (繁体)',
            'en-US': 'English (US)',
            'ja-JP': '日本語',
            'ko-KR': '한국어'
        }
        
        # 界面文本字典
        self.texts = {
            'zh-CN': {
                'title': '📚 EPUB文件合并工具',
                'subtitle': '将多个EPUB文件按顺序合并，保留原有格式和内容',
                'file_section': '📁 选择EPUB文件',
                'output_section': '💾 输出设置',
                'status_section': '⚡ 处理状态',
                'add_files': '➕ 添加文件',
                'clear_files': '🗑️ 清空列表',
                'move_up': '⬆️ 上移',
                'move_down': '⬇️ 下移',
                'remove_selected': '❌ 删除选中',
                'output_filename': '输出文件名:',
                'select_location': '📁 选择位置',
                'language_setting': '语言设置:',
                'start_merge': '🚀 开始合并',
                'merging': '⏳ 合并中...',
                'ready': '准备就绪',
                'select_files': '请选择要合并的EPUB文件',
                'files_selected': '已选择 {} 个EPUB文件，准备就绪',
                'merge_complete': '✅ 合并完成！',
                'merge_failed': '❌ 合并失败',
                'last_update': '最后更新: {}',
                'warning': '警告',
                'error': '错误',
                'success': '成功',
                'select_files_warning': '请先选择要合并的EPUB文件！',
                'output_warning': '请指定输出文件名！',
                'merge_success': 'EPUB文件合并成功！\n\n输出文件: {}',
                'merge_error': '合并失败:\n{}',
                'select_epub_files': '选择EPUB文件',
                'select_output_location': '选择输出文件位置',
                'epub_files': 'EPUB文件',
                'all_files': '所有文件',
                'files_count': '{} 个文件',
                'processing': '正在合并EPUB文件...',
                'language_code': '语言代码: {}'
            },
            'zh-TW': {
                'title': '📚 EPUB檔案合併工具',
                'subtitle': '將多個EPUB檔案按順序合併，保留原有格式和內容',
                'file_section': '📁 選擇EPUB檔案',
                'output_section': '💾 輸出設定',
                'status_section': '⚡ 處理狀態',
                'add_files': '➕ 新增檔案',
                'clear_files': '🗑️ 清空清單',
                'move_up': '⬆️ 上移',
                'move_down': '⬇️ 下移',
                'remove_selected': '❌ 刪除選中',
                'output_filename': '輸出檔案名稱:',
                'select_location': '📁 選擇位置',
                'language_setting': '語言設定:',
                'start_merge': '🚀 開始合併',
                'merging': '⏳ 合併中...',
                'ready': '準備就緒',
                'select_files': '請選擇要合併的EPUB檔案',
                'files_selected': '已選擇 {} 個EPUB檔案，準備就緒',
                'merge_complete': '✅ 合併完成！',
                'merge_failed': '❌ 合併失敗',
                'last_update': '最後更新: {}',
                'warning': '警告',
                'error': '錯誤',
                'success': '成功',
                'select_files_warning': '請先選擇要合併的EPUB檔案！',
                'output_warning': '請指定輸出檔案名稱！',
                'merge_success': 'EPUB檔案合併成功！\n\n輸出檔案: {}',
                'merge_error': '合併失敗:\n{}',
                'select_epub_files': '選擇EPUB檔案',
                'select_output_location': '選擇輸出檔案位置',
                'epub_files': 'EPUB檔案',
                'all_files': '所有檔案',
                'files_count': '{} 個檔案',
                'processing': '正在合併EPUB檔案...',
                'language_code': '語言代碼: {}'
            },
            'en-US': {
                'title': '📚 EPUB File Merger Tool',
                'subtitle': 'Merge multiple EPUB files in sequence, preserving original format and content',
                'file_section': '📁 Select EPUB Files',
                'output_section': '💾 Output Settings',
                'status_section': '⚡ Processing Status',
                'add_files': '➕ Add Files',
                'clear_files': '🗑️ Clear List',
                'move_up': '⬆️ Move Up',
                'move_down': '⬇️ Move Down',
                'remove_selected': '❌ Delete Selected',
                'output_filename': 'Output Filename:',
                'select_location': '📁 Select Location',
                'language_setting': 'Language Setting:',
                'start_merge': '🚀 Start Merge',
                'merging': '⏳ Merging...',
                'ready': 'Ready',
                'select_files': 'Please select EPUB files to merge',
                'files_selected': '{} files selected, ready to merge',
                'merge_complete': '✅ Merge Complete!',
                'merge_failed': '❌ Merge Failed',
                'last_update': 'Last Update: {}',
                'warning': 'Warning',
                'error': 'Error',
                'success': 'Success',
                'select_files_warning': 'Please select EPUB files to merge first!',
                'output_warning': 'Please specify output filename!',
                'merge_success': 'EPUB files merged successfully!\n\nOutput file: {}',
                'merge_error': 'Merge failed:\n{}',
                'select_epub_files': 'Select EPUB Files',
                'select_output_location': 'Select Output File Location',
                'epub_files': 'EPUB Files',
                'all_files': 'All Files',
                'files_count': '{} files',
                'processing': 'Merging EPUB files...',
                'language_code': 'Language Code: {}'
            },
            'ja-JP': {
                'title': '📚 EPUBファイル結合ツール',
                'subtitle': '複数のEPUBファイルを順番に結合し、元のフォーマットとコンテンツを保持します',
                'file_section': '📁 EPUBファイルを選択',
                'output_section': '💾 出力設定',
                'status_section': '⚡ 処理状態',
                'add_files': '➕ ファイル追加',
                'clear_files': '🗑️ リストクリア',
                'move_up': '⬆️ 上に移動',
                'move_down': '⬇️ 下に移動',
                'remove_selected': '❌ 選択削除',
                'output_filename': '出力ファイル名:',
                'select_location': '📁 場所選択',
                'language_setting': '言語設定:',
                'start_merge': '🚀 結合開始',
                'merging': '⏳ 結合中...',
                'ready': '準備完了',
                'select_files': '結合するEPUBファイルを選択してください',
                'files_selected': '{}個のファイルが選択されました、結合準備完了',
                'merge_complete': '✅ 結合完了！',
                'merge_failed': '❌ 結合失敗',
                'last_update': '最終更新: {}',
                'warning': '警告',
                'error': 'エラー',
                'success': '成功',
                'select_files_warning': '結合するEPUBファイルを先に選択してください！',
                'output_warning': '出力ファイル名を指定してください！',
                'merge_success': 'EPUBファイルの結合が成功しました！\n\n出力ファイル: {}',
                'merge_error': '結合に失敗しました:\n{}',
                'select_epub_files': 'EPUBファイルを選択',
                'select_output_location': '出力ファイルの場所を選択',
                'epub_files': 'EPUBファイル',
                'all_files': 'すべてのファイル',
                'files_count': '{}個のファイル',
                'processing': 'EPUBファイルを結合中...',
                'language_code': '言語コード: {}'
            },
            'ko-KR': {
                'title': '📚 EPUB 파일 병합 도구',
                'subtitle': '여러 EPUB 파일을 순서대로 병합하여 원본 형식과 내용을 유지합니다',
                'file_section': '📁 EPUB 파일 선택',
                'output_section': '💾 출력 설정',
                'status_section': '⚡ 처리 상태',
                'add_files': '➕ 파일 추가',
                'clear_files': '🗑️ 목록 지우기',
                'move_up': '⬆️ 위로 이동',
                'move_down': '⬇️ 아래로 이동',
                'remove_selected': '❌ 선택 삭제',
                'output_filename': '출력 파일명:',
                'select_location': '📁 위치 선택',
                'language_setting': '언어 설정:',
                'start_merge': '🚀 병합 시작',
                'merging': '⏳ 병합 중...',
                'ready': '준비 완료',
                'select_files': '병합할 EPUB 파일을 선택하세요',
                'files_selected': '{}개 파일이 선택되었습니다, 병합 준비 완료',
                'merge_complete': '✅ 병합 완료!',
                'merge_failed': '❌ 병합 실패',
                'last_update': '마지막 업데이트: {}',
                'warning': '경고',
                'error': '오류',
                'success': '성공',
                'select_files_warning': '병합할 EPUB 파일을 먼저 선택하세요!',
                'output_warning': '출력 파일명을 지정하세요!',
                'merge_success': 'EPUB 파일 병합이 성공했습니다!\n\n출력 파일: {}',
                'merge_error': '병합에 실패했습니다:\n{}',
                'select_epub_files': 'EPUB 파일 선택',
                'select_output_location': '출력 파일 위치 선택',
                'epub_files': 'EPUB 파일',
                'all_files': '모든 파일',
                'files_count': '{}개 파일',
                'processing': 'EPUB 파일을 병합 중...',
                'language_code': '언어 코드: {}'
            }
        }
        
        self.epub_files = []
        self.setup_ui()
        
    def get_text(self, key):
        """获取当前语言的文本"""
        return self.texts.get(self.current_language, self.texts['zh-CN']).get(key, key)
        
    def change_language(self, language_code):
        """切换界面语言"""
        if language_code in self.texts:
            self.current_language = language_code
            self.update_ui_texts()
            
    def update_ui_texts(self):
        """更新界面文本"""
        # 更新窗口标题
        self.root.title(self.get_text('title'))
        
        # 更新标题区域
        if hasattr(self, 'title_label'):
            self.title_label.config(text=self.get_text('title'))
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.config(text=self.get_text('subtitle'))
            
        # 更新文件区域
        if hasattr(self, 'file_section_title'):
            self.file_section_title.config(text=self.get_text('file_section'))
            
        # 更新输出区域
        if hasattr(self, 'output_section_title'):
            self.output_section_title.config(text=self.get_text('output_section'))
        if hasattr(self, 'output_label'):
            self.output_label.config(text=self.get_text('output_filename'))
        if hasattr(self, 'language_label'):
            self.language_label.config(text=self.get_text('language_setting'))
        if hasattr(self, 'browse_btn'):
            self.browse_btn.config(text=self.get_text('select_location'))
            
        # 更新状态区域
        if hasattr(self, 'status_section_title'):
            self.status_section_title.config(text=self.get_text('status_section'))
            
        # 更新按钮
        if hasattr(self, 'add_btn'):
            self.add_btn.config(text=self.get_text('add_files'))
        if hasattr(self, 'clear_btn'):
            self.clear_btn.config(text=self.get_text('clear_files'))
        if hasattr(self, 'up_btn'):
            self.up_btn.config(text=self.get_text('move_up'))
        if hasattr(self, 'down_btn'):
            self.down_btn.config(text=self.get_text('move_down'))
        if hasattr(self, 'remove_btn'):
            self.remove_btn.config(text=self.get_text('remove_selected'))
        if hasattr(self, 'merge_button'):
            self.merge_button.config(text=self.get_text('start_merge'))
            
        # 更新状态
        self.update_status()
        
    def setup_ui(self):
        """设置现代化用户界面"""
        # 主容器 - 使用网格布局实现自适应
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 配置网格权重，实现自适应缩放
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=0)
        main_frame.rowconfigure(3, weight=0)
        main_frame.rowconfigure(4, weight=0)
        
        # 标题区域 - 跨越两列
        self.create_header(main_frame)
        
        # 左右布局区域 - 文件选择和输出设置
        self.create_left_right_section(main_frame)
        
        # 操作按钮区域
        self.create_action_section(main_frame)
        
        # 进度区域
        self.create_progress_section(main_frame)
        
    def create_header(self, parent):
        """创建标题区域"""
        header = tk.Frame(parent, bg=self.colors['background'])
        header.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        self.title_label = tk.Label(header, text=self.get_text('title'),
                        font=('Microsoft YaHei UI', 24, 'bold'),
                        fg=self.colors['primary'], bg=self.colors['background'])
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(header, text=self.get_text('subtitle'),
                           font=('Microsoft YaHei UI', 12),
                           fg=self.colors['text_secondary'], bg=self.colors['background'])
        self.subtitle_label.pack(pady=(5, 0))
        
        # 添加界面语言切换
        language_frame = tk.Frame(header, bg=self.colors['background'])
        language_frame.pack(pady=(10, 0))
        
        language_switch_label = tk.Label(language_frame, text="🌍 界面语言:",
                                        font=('Microsoft YaHei UI', 10),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['background'])
        language_switch_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 界面语言选择下拉框
        self.interface_language_var = tk.StringVar(value='zh-CN')
        self.interface_language_combo = ttk.Combobox(language_frame, 
                                                    textvariable=self.interface_language_var,
                                                    values=list(self.languages.values()),
                                                    font=('Microsoft YaHei UI', 9),
                                                    state='readonly', width=15)
        self.interface_language_combo.pack(side=tk.LEFT)
        self.interface_language_combo.set('中文 (简体)')
        
        # 绑定界面语言切换事件
        self.interface_language_combo.bind('<<ComboboxSelected>>', self.on_interface_language_change)
        
    def create_left_right_section(self, parent):
        """创建左右布局区域"""
        # 左侧：文件选择区域
        self.create_file_section(parent)
        
        # 右侧：输出设置区域
        self.create_output_section(parent)
        
    def create_file_section(self, parent):
        """创建文件选择区域（左侧）"""
        # 卡片容器
        card = tk.Frame(parent, bg=self.colors['surface'], 
                       relief='flat', bd=1, highlightthickness=1,
                       highlightbackground='#e2e8f0')
        card.grid(row=1, column=0, sticky='nsew', padx=(0, 10))
        
        # 配置卡片内部网格权重
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)
        
        # 卡片标题
        header = tk.Frame(card, bg=self.colors['surface'])
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=15)
        
        self.file_section_title = tk.Label(header, text=self.get_text('file_section'),
                        font=('Microsoft YaHei UI', 14, 'bold'),
                        fg=self.colors['text'], bg=self.colors['surface'])
        self.file_section_title.pack(side=tk.LEFT)
        
        self.file_count_label = tk.Label(header, text="0 个文件",
                                        font=('Microsoft YaHei UI', 10),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['surface'])
        self.file_count_label.pack(side=tk.RIGHT)
        
        # 文件列表
        list_frame = tk.Frame(card, bg=self.colors['surface'])
        list_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 15))
        
        # 配置列表框架的网格权重
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=8,
                                      font=('Microsoft YaHei UI', 10),
                                      bg='white', fg=self.colors['text'],
                                      selectbackground=self.colors['primary'],
                                      selectforeground='white',
                                      relief='flat', bd=1,
                                      highlightthickness=1,
                                      highlightcolor=self.colors['primary'])
        self.file_listbox.grid(row=0, column=0, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 按钮区域
        btn_frame = tk.Frame(card, bg=self.colors['surface'])
        btn_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # 第一行按钮
        row1 = tk.Frame(btn_frame, bg=self.colors['surface'])
        row1.pack(fill=tk.X, pady=(0, 10))
        
        self.add_btn = tk.Button(row1, text=self.get_text('add_files'), command=self.add_files,
                           font=('Microsoft YaHei UI', 10, 'bold'),
                           bg=self.colors['primary'], fg='white',
                           relief='flat', padx=20, pady=8, cursor='hand2')
        self.add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(row1, text=self.get_text('clear_files'), command=self.clear_files,
                             font=('Microsoft YaHei UI', 10),
                             bg=self.colors['secondary'], fg='white',
                             relief='flat', padx=20, pady=8, cursor='hand2')
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 第二行按钮
        row2 = tk.Frame(btn_frame, bg=self.colors['surface'])
        row2.pack(fill=tk.X)
        
        self.up_btn = tk.Button(row2, text=self.get_text('move_up'), command=self.move_up,
                          font=('Microsoft YaHei UI', 9),
                          bg=self.colors['secondary'], fg='white',
                          relief='flat', padx=15, pady=6, cursor='hand2')
        self.up_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.down_btn = tk.Button(row2, text=self.get_text('move_down'), command=self.move_down,
                            font=('Microsoft YaHei UI', 9),
                            bg=self.colors['secondary'], fg='white',
                            relief='flat', padx=15, pady=6, cursor='hand2')
        self.down_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.remove_btn = tk.Button(row2, text=self.get_text('remove_selected'), command=self.remove_selected,
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['error'], fg='white',
                              relief='flat', padx=15, pady=6, cursor='hand2')
        self.remove_btn.pack(side=tk.LEFT)
        
    def create_output_section(self, parent):
        """创建输出设置区域（右侧）"""
        card = tk.Frame(parent, bg=self.colors['surface'],
                       relief='flat', bd=1, highlightthickness=1,
                       highlightbackground='#e2e8f0')
        card.grid(row=1, column=1, sticky='nsew', padx=(10, 0))
        
        # 配置卡片内部网格权重
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)
        
        header = tk.Frame(card, bg=self.colors['surface'])
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=15)
        
        self.output_section_title = tk.Label(header, text=self.get_text('output_section'),
                        font=('Microsoft YaHei UI', 14, 'bold'),
                        fg=self.colors['text'], bg=self.colors['surface'])
        self.output_section_title.pack(side=tk.LEFT)
        
        content = tk.Frame(card, bg=self.colors['surface'])
        content.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 15))
        
        # 配置内容框架的网格权重
        content.columnconfigure(0, weight=1)
        
        # 输出文件名设置
        self.output_label = tk.Label(content, text=self.get_text('output_filename'),
                               font=('Microsoft YaHei UI', 10, 'bold'),
                               fg=self.colors['text'], bg=self.colors['surface'])
        self.output_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        input_frame = tk.Frame(content, bg=self.colors['surface'])
        input_frame.grid(row=1, column=0, sticky='ew')
        
        # 配置输入框架的网格权重
        input_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar(value="merged.epub")
        self.output_entry = tk.Entry(input_frame, textvariable=self.output_var,
                                    font=('Microsoft YaHei UI', 10),
                                    relief='flat', bd=1,
                                    highlightthickness=1,
                                    highlightcolor=self.colors['primary'])
        self.output_entry.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        
        self.browse_btn = tk.Button(input_frame, text=self.get_text('select_location'),
                              command=self.select_output,
                              font=('Microsoft YaHei UI', 9),
                              bg=self.colors['secondary'], fg='white',
                              relief='flat', padx=15, pady=6, cursor='hand2')
        self.browse_btn.grid(row=0, column=1)
        
        # 语言选择设置
        self.language_label = tk.Label(content, text=self.get_text('language_setting'),
                                 font=('Microsoft YaHei UI', 10, 'bold'),
                                 fg=self.colors['text'], bg=self.colors['surface'])
        self.language_label.grid(row=2, column=0, sticky='w', pady=(15, 5))
        
        # 语言选项
        self.language_options = [
            ('中文 (简体)', 'zh-CN'),
            ('中文 (繁体)', 'zh-TW'),
            ('English (US)', 'en-US'),
            ('English (UK)', 'en-GB'),
            ('日本語', 'ja-JP'),
            ('한국어', 'ko-KR'),
            ('Français', 'fr-FR'),
            ('Deutsch', 'de-DE'),
            ('Español', 'es-ES'),
            ('Italiano', 'it-IT'),
            ('Português', 'pt-BR'),
            ('Русский', 'ru-RU')
        ]
        
        self.language_var = tk.StringVar(value='zh-CN')
        self.language_combo = ttk.Combobox(content, textvariable=self.language_var,
                                          values=[option[0] for option in self.language_options],
                                          font=('Microsoft YaHei UI', 10),
                                          state='readonly')
        self.language_combo.grid(row=3, column=0, sticky='ew', pady=(0, 5))
        self.language_combo.set('中文 (简体)')
        
        # 语言代码显示
        self.language_code_var = tk.StringVar(value='zh-CN')
        language_code_label = tk.Label(content, textvariable=self.language_code_var,
                                      font=('Microsoft YaHei UI', 8),
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['surface'])
        language_code_label.grid(row=4, column=0, sticky='w')
        
        # 绑定语言选择事件
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
    def create_action_section(self, parent):
        """创建操作按钮区域"""
        action_frame = tk.Frame(parent, bg=self.colors['background'])
        action_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(20, 20))
        
        self.merge_button = tk.Button(action_frame, text=self.get_text('start_merge'),
                                     command=self.start_merge,
                                     font=('Microsoft YaHei UI', 14, 'bold'),
                                     bg=self.colors['success'], fg='white',
                                     relief='flat', padx=40, pady=15,
                                     cursor='hand2')
        self.merge_button.pack()
        
        # 悬停效果
        self.merge_button.bind('<Enter>', lambda e: self.merge_button.config(bg='#047857'))
        self.merge_button.bind('<Leave>', lambda e: self.merge_button.config(bg=self.colors['success']))
        
    def create_progress_section(self, parent):
        """创建进度区域"""
        card = tk.Frame(parent, bg=self.colors['surface'],
                       relief='flat', bd=1, highlightthickness=1,
                       highlightbackground='#e2e8f0')
        card.grid(row=3, column=0, columnspan=2, sticky='ew')
        
        # 配置卡片内部网格权重
        card.columnconfigure(0, weight=1)
        
        header = tk.Frame(card, bg=self.colors['surface'])
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=15)
        
        self.status_section_title = tk.Label(header, text=self.get_text('status_section'),
                        font=('Microsoft YaHei UI', 14, 'bold'),
                        fg=self.colors['text'], bg=self.colors['surface'])
        self.status_section_title.pack(side=tk.LEFT)
        
        content = tk.Frame(card, bg=self.colors['surface'])
        content.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # 配置内容框架的网格权重
        content.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value=self.get_text('ready'))
        status_label = tk.Label(content, textvariable=self.status_var,
                               font=('Microsoft YaHei UI', 10),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['surface'])
        status_label.grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(content, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky='ew', pady=(0, 5))
        
        self.timestamp_var = tk.StringVar()
        timestamp_label = tk.Label(content, textvariable=self.timestamp_var,
                                  font=('Microsoft YaHei UI', 8),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['surface'])
        timestamp_label.grid(row=2, column=0, sticky='w')
        
    def add_files(self):
        """添加EPUB文件"""
        files = filedialog.askopenfilenames(
            title=self.get_text('select_epub_files'),
            filetypes=[(self.get_text('epub_files'), "*.epub"), (self.get_text('all_files'), "*.*")]
        )
        
        for file in files:
            if file not in self.epub_files:
                self.epub_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status()
        
    def clear_files(self):
        """清空文件列表"""
        self.epub_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status()
        
    def remove_selected(self):
        """删除选中的文件"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            self.epub_files.pop(index)
            self.update_status()
            
    def move_up(self):
        """上移选中的文件"""
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            self.epub_files[index], self.epub_files[index-1] = self.epub_files[index-1], self.epub_files[index]
            self.refresh_file_list()
            self.file_listbox.selection_set(index-1)
            
    def move_down(self):
        """下移选中的文件"""
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.epub_files) - 1:
            index = selection[0]
            self.epub_files[index], self.epub_files[index+1] = self.epub_files[index+1], self.epub_files[index]
            self.refresh_file_list()
            self.file_listbox.selection_set(index+1)
            
    def refresh_file_list(self):
        """刷新文件列表显示"""
        self.file_listbox.delete(0, tk.END)
        for file in self.epub_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
            
    def select_output(self):
        """选择输出文件位置"""
        output_file = filedialog.asksaveasfilename(
            title=self.get_text('select_output_location'),
            defaultextension=".epub",
            filetypes=[(self.get_text('epub_files'), "*.epub"), (self.get_text('all_files'), "*.*")]
        )
        if output_file:
            self.output_var.set(output_file)
            
    def update_status(self):
        """更新状态显示"""
        count = len(self.epub_files)
        self.file_count_label.config(text=self.get_text('files_count').format(count))
        
        if count == 0:
            self.status_var.set(self.get_text('select_files'))
        else:
            self.status_var.set(self.get_text('files_selected').format(count))
            
    def update_timestamp(self):
        """更新时间戳"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_var.set(self.get_text('last_update').format(timestamp))
        
    def start_merge(self):
        """开始合并"""
        if not self.epub_files:
            messagebox.showwarning(self.get_text('warning'), self.get_text('select_files_warning'))
            return
            
        output_path = self.output_var.get()
        if not output_path:
            messagebox.showwarning(self.get_text('warning'), self.get_text('output_warning'))
            return
            
        # 禁用界面
        self.merge_button.config(state='disabled', text=self.get_text('merging'))
        self.progress_bar.start()
        self.status_var.set(self.get_text('processing'))
        self.update_timestamp()
        
        # 在新线程中执行合并
        thread = threading.Thread(target=self.merge_in_thread, args=(output_path,))
        thread.daemon = True
        thread.start()
        
    def merge_in_thread(self, output_path):
        """在线程中执行合并"""
        try:
            # 获取选择的语言代码
            selected_index = self.language_combo.current()
            language_code = self.language_options[selected_index][1] if selected_index >= 0 else 'zh-CN'
            
            merger = EpubMerger(language=language_code)
            merger.merge_epub(self.epub_files, output_path)
            
            # 在主线程中更新UI
            self.root.after(0, self.merge_completed, True, output_path)
        except Exception as e:
            # 在主线程中更新UI
            self.root.after(0, self.merge_completed, False, str(e))
            
    def merge_completed(self, success, result):
        """合并完成后的处理"""
        self.progress_bar.stop()
        self.merge_button.config(state='normal', text=self.get_text('start_merge'))
        self.update_timestamp()
        
        if success:
            self.status_var.set(self.get_text('merge_complete'))
            messagebox.showinfo(self.get_text('success'), self.get_text('merge_success').format(result))
        else:
            self.status_var.set(self.get_text('merge_failed'))
            messagebox.showerror(self.get_text('error'), self.get_text('merge_error').format(result))

    def on_language_change(self, event=None):
        """语言选择改变时的处理"""
        selected_index = self.language_combo.current()
        if selected_index >= 0:
            language_code = self.language_options[selected_index][1]
            self.language_code_var.set(self.get_text('language_code').format(language_code))

    def on_interface_language_change(self, event=None):
        """界面语言选择改变时的处理"""
        selected_index = self.interface_language_combo.current()
        if selected_index >= 0:
            language_codes = list(self.languages.keys())
            language_code = language_codes[selected_index]
            self.change_language(language_code)

def main():
    root = tk.Tk()
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = ModernEpubMergerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 