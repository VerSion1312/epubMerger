# EPUB File Merger Tool

English | [中文](README.md)

A Python tool for merging multiple EPUB files into a single file in sequence. This tool preserves original images and text content while maintaining the original order and positioning.

## Features

- ✅ Merge multiple EPUB files in sequence
- ✅ Preserve original images and text content
- ✅ Maintain original reading order and positioning
- ✅ Support both command-line and graphical interface usage
- ✅ Modern and beautiful GUI design
- ✅ Automatic EPUB internal structure handling
- ✅ Support for Chinese paths and filenames
- ✅ Real-time progress display and status feedback
- ✅ Support for multiple language settings

## Interface Features

### Modern Design
- 🎨 Modern flat design style
- 🌈 Carefully matched color scheme
- 📱 Responsive layout with window scaling support
- 🎯 Intuitive icons and visual feedback
- 💫 Smooth interaction experience

### User-Friendly
- 📁 Drag-and-drop file selection
- 🔄 Real-time file list management
- ⚡ Real-time progress display
- 📊 Detailed status information
- 🕒 Timestamp recording
- 🌍 Interface multi-language switching support

### Multi-Language Interface
- 🎯 Support for 5 interface languages: Simplified Chinese, Traditional Chinese, English, Japanese, Korean
- 🔄 Real-time language switching without program restart
- 📝 Complete interface text localization
- 🎨 Consistent visual design style across languages

## File Description

- `epub_merger.py` - Core merging functionality module
- `epub_merger_gui.py` - Modern graphical interface version
- `README.md` - Chinese usage documentation
- `README_EN.md` - English usage documentation
- `一键启动.bat` - Windows one-click startup script

## Installation Requirements

This program uses Python standard library and requires no additional dependency packages. Supports Python 3.6 and above.

## Usage

### Method 1: Modern Graphical Interface (Recommended)

1. **Start the program**:
   ```bash
   python epub_merger_gui.py
   ```
   Or double-click the `一键启动.bat` file

2. **Using the interface**:
   - 🖱️ Click "➕ Add Files" to select EPUB files to merge
   - 📋 Use "⬆️ Move Up" and "⬇️ Move Down" buttons to adjust file order
   - 🗑️ Use "❌ Delete Selected" to remove unwanted files
   - 💾 Set output filename and location
   - 🌍 Select language setting
   - 🚀 Click "Start Merge" to execute the merge operation

### Method 2: Command Line

1. **Basic usage**:
   ```bash
   python epub_merger.py file1.epub file2.epub file3.epub -o merged.epub
   ```

2. **Specify language**:
   ```bash
   python epub_merger.py file1.epub file2.epub -o merged.epub -l en-US
   ```

3. **View help**:
   ```bash
   python epub_merger.py -h
   ```

## Language Settings

The program supports multiple language settings and allows you to specify the output EPUB language during merging:

### Supported Languages

- **Chinese (Simplified)** - `zh-CN` (default)
- **Chinese (Traditional)** - `zh-TW`
- **English (US)** - `en-US`
- **English (UK)** - `en-GB`
- **日本語** - `ja-JP`
- **한국어** - `ko-KR`
- **Français** - `fr-FR`
- **Deutsch** - `de-DE`
- **Español** - `es-ES`
- **Italiano** - `it-IT`
- **Português** - `pt-BR`
- **Русский** - `ru-RU`

### GUI Interface Settings

In the GUI interface, language selection is located in the "Output Settings" area on the right:
1. Select the desired language from the "Language Settings" dropdown
2. The interface displays the corresponding language code in real-time
3. The selected language setting is automatically applied during merging

### Command Line Settings

Use the `-l` or `--language` parameter to specify the language:

```bash
# Merge as English version
python epub_merger.py chapter1.epub chapter2.epub -o english_book.epub -l en-US

# Merge as Japanese version
python epub_merger.py part1.epub part2.epub -o japanese_book.epub -l ja-JP

# Merge as Traditional Chinese version
python epub_merger.py book1.epub book2.epub -o traditional_book.epub -l zh-TW
```

## Interface Preview
![1751275847231.png](https://version-pic-bed.oss-cn-hangzhou.aliyuncs.com/images/1751275847231.png)

### Main Functional Areas

1. **📁 File Selection Area**
   - File list display
   - File count statistics
   - File operation buttons (add, delete, sort)

2. **💾 Output Settings Area**
   - Output filename setting
   - File location selection
   - Language setting dropdown

3. **⚡ Processing Status Area**
   - Real-time status display
   - Progress bar animation
   - Timestamp recording

4. **🚀 Operation Button Area**
   - Prominent merge button
   - Hover effect feedback

## Usage Examples

### GUI Usage Steps

1. **Start the program**: Double-click to run `epub_merger_gui.py` or run in command line
2. **Select interface language**: Choose the desired interface display language from the "🌍 Interface Language" dropdown at the top
3. **Add files**: Click the "➕ Add Files" button to select EPUB files to merge
4. **Adjust order**: Use "⬆️ Move Up" and "⬇️ Move Down" buttons to adjust file merge order
5. **Set output**: Enter the merged filename in the output filename box
6. **Select output language**: Choose the output EPUB language from the "Language Setting" dropdown on the right
7. **Start merge**: Click the "🚀 Start Merge" button and wait for processing to complete

### Command Line Examples

```bash
# Merge two EPUB files
python epub_merger.py chapter1.epub chapter2.epub -o complete_book.epub

# Merge multiple files
python epub_merger.py part1.epub part2.epub part3.epub part4.epub -o full_novel.epub

# Merge as English version
python epub_merger.py chapter1.epub chapter2.epub -o english_book.epub -l en-US

# Merge as Japanese version
python epub_merger.py part1.epub part2.epub -o japanese_book.epub -l ja-JP

# Merge as Traditional Chinese version
python epub_merger.py book1.epub book2.epub -o traditional_book.epub -l zh-TW
```

## Design Philosophy

### Modern UI Design
- **Flat Design**: Remove excessive decorative elements, emphasize functionality
- **Card-based Layout**: Clear information grouping and hierarchical structure
- **Consistent Color System**: Unified visual language and brand recognition
- **Responsive Interaction**: Smooth animations and state feedback

### User Experience Optimization
- **Intuitive Operation Flow**: Operation paths that conform to user habits
- **Clear Status Feedback**: Real-time progress and status information
- **Friendly Error Handling**: Detailed error prompts and solution suggestions
- **Accessibility Design**: Support for keyboard navigation and screen readers

## Important Notes

1. **File Order**: Merged content will be arranged according to the file order you select
2. **File Format**: Ensure input EPUB files are correctly formatted and not corrupted
3. **Output Location**: Ensure sufficient disk space to store the merged file
4. **Chinese Support**: The program fully supports Chinese paths and filenames
5. **Interface Scaling**: Supports window size adjustment with minimum size of 700x600

## Technical Principles

How the program works:

1. **Extract EPUB**: Extract each EPUB file to a temporary directory
2. **Parse Structure**: Read container.xml and content.opf files
3. **Extract Content**: Extract all content files according to spine order
4. **Merge Resources**: Merge all images, CSS, and other resource files
5. **Rebuild Structure**: Create new content.opf and container.xml
6. **Package Files**: Repackage all content into EPUB format

## Troubleshooting

### Common Issues

1. **"Cannot find container.xml file" error**
   - Cause: EPUB file may be corrupted or incorrectly formatted
   - Solution: Check if the EPUB file is complete, try opening with other EPUB readers

2. **"Merge failed" error**
   - Cause: May be file permission issues or insufficient disk space
   - Solution: Check file permissions and disk space

3. **GUI interface unresponsive**
   - Cause: Interface may be temporarily unresponsive when processing large files
   - Solution: Wait for processing to complete, this is normal

4. **Interface display abnormalities**
   - Cause: May be font or display setting issues
   - Solution: Ensure Microsoft YaHei UI font is installed on the system

### Log Information

The program displays detailed processing logs, including:
- File processing progress
- Resource copying information
- Error details

## Update Log

### v2.2.0 - Interface Multi-Language Version
- 🌍 Added interface multi-language switching feature
- 🎯 Support for 5 interface languages: Simplified Chinese, Traditional Chinese, English, Japanese, Korean
- 🔄 Real-time language switching without program restart
- 📝 Complete interface text localization
- 🎨 Consistent visual design style across languages

### v2.1.0 - Language Selection Feature Version
- 🌍 Added multiple language setting selection feature
- 🎯 Support for 12 common language codes
- 🖥️ GUI interface integrated language selection dropdown
- ⌨️ Command line support for -l parameter to specify language
- 📝 Comprehensive usage documentation and examples

### v2.0.0 - Modern Interface Version
- 🎨 Brand new modern GUI interface design
- 🌈 Optimized color scheme and visual experience
- 📱 Responsive layout and window scaling support
- 🎯 Intuitive icons and interaction feedback
- ⚡ Real-time progress display and status updates

### v1.0.0 - Basic Version
- Support for basic EPUB merging functionality
- Support for both command line and basic GUI usage methods
- Complete error handling and logging

## License

This program is open source software and can be freely used and modified.

## Contributing

Welcome to submit issue reports and feature suggestions! 