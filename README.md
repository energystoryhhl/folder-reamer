# Folder Renamer Tool

A PyQt5-based GUI application for batch renaming files in nested directory structures using regular expressions and custom naming patterns.

## Features

- **Directory Tree Navigation**: Browse and select folders using an intuitive file tree interface
- **Regex Pattern Matching**: Use regular expressions to match directory names and extract information
- **Custom Naming Rules**: Define flexible file naming patterns using placeholders
- **File Type Filtering**: Filter files by extension (e.g., mp4, mkv, avi)
- **Batch Processing**: Rename multiple files across multiple directories in one operation
- **Real-time Logging**: Monitor the renaming process with detailed log output
- **Safe Operations**: Comprehensive validation before renaming operations

## Screenshots

The application provides a clean, user-friendly interface with:
- File tree browser for directory selection
- Input fields for regex patterns and naming rules
- Real-time logging window
- Progress tracking

## Installation

### Prerequisites

- Python 3.6 or higher
- PyQt5

### Install Dependencies

```bash
pip install PyQt5
```

### Run from Source

```bash
python tool_main.py
```

### Build Executable

The project includes build scripts for creating standalone executables:

- **Windows**: Run `makeexe.bat`
- **Cross-platform**: Use the included Nuitka build configuration

## Usage

### Basic Workflow

1. **Launch the Application**: Run `tool_main.py`
2. **Select Directory**: Click on a folder in the tree view to select it
3. **Configure Patterns**:
   - Set the regex pattern for directory matching
   - Define the file naming rule using placeholders
   - Specify file type filters (optional)
4. **Start Renaming**: Click "开始转换" (Start Conversion) to begin

### Configuration Options

#### Directory Structure Requirements

The tool expects a specific directory structure:
```
Selected_Folder/
├── Level1_Directory/
│   ├── Level2_Directory/
│   │   ├── file1.mp4
│   │   ├── file2.mp4
│   │   └── ...
│   └── ...
└── ...
```

#### Regex Pattern

Configure the regex pattern to match the second-level directory names. Default pattern:
```
(.+)-(.+)-(.+)
```

This matches directory names like "Name1-Name2-Name3" and captures three groups.

#### Naming Rule Placeholders

Use these placeholders in your naming rule:

- `(DIR1)`, `(DIR2)`, `(DIR3)`: Directory names at different levels
- `(MATCH1)`, `(MATCH2)`, `(MATCH3)`: Regex capture groups
- `(ORDER)`: Sequential file number (zero-padded)

Example naming rule:
```
【常规】(MATCH2)-(DIR3)-(MATCH1)-(DIR1)-(ORDER)-(MATCH3)
```

#### File Type Filtering

Specify file extensions to process, separated by `|`:
```
mp4|mkv|avi|mov
```

### Example Configuration

For a directory structure like:
```
Videos/
├── 张三-视频-娱乐/
│   ├── 唱歌跳舞/
│   │   ├── video1.mp4
│   │   └── video2.mp4
└── 李四-音乐-学习/
    └── 钢琴教学/
        └── lesson1.mp4
```

With configuration:
- **Regex**: `(.+)-(.+)-(.+)`
- **Naming Rule**: `【常规】(MATCH2)-(DIR3)-(MATCH1)-(DIR1)-(ORDER)-(MATCH3)`
- **File Filter**: `mp4|mkv|avi`

Results in files renamed to:
- `【常规】视频-唱歌跳舞-张三-Videos-000-娱乐.mp4`
- `【常规】视频-唱歌跳舞-张三-Videos-001-娱乐.mp4`
- `【常规】音乐-钢琴教学-李四-Videos-002-学习.mp4`

## Project Structure

```
folder_renamer/
├── tool_main.py          # Main application entry point
├── tool.py              # Generated PyQt5 UI code
├── tool.ui              # Qt Designer UI file
├── rename_worker.py     # Core renaming logic and utilities
├── README.md           # This file
├── LICENSE             # License information
├── makeexe.bat         # Windows executable build script
├── genpy.bat           # UI generation script
└── build/              # Build artifacts and executables
```

## Core Components

### `tool_main.py`
- Main application window and UI logic
- Event handling for user interactions
- Threading for non-blocking operations
- Logging and status updates

### `rename_worker.py`
- Directory structure validation
- Regex pattern matching
- File renaming operations
- Path utilities

### `tool.py`
- Auto-generated PyQt5 UI code
- Window layout and widget definitions

## Special Features

### Smart Category Detection

The tool includes special logic for certain directory categories:
- Directories named "文件", "美化包", "三角洲", "吃鸡" automatically change "【常规】" to "【非】" in the output name

### Thread Safety

File operations run in separate threads to prevent UI freezing during batch operations.

### Error Handling

Comprehensive error handling with detailed logging for:
- Invalid directory structures
- Permission issues
- File system errors
- Pattern matching failures

## Building Executables

### Using Nuitka (Recommended)

The project includes Nuitka configuration for building optimized executables:

```bash
# Install Nuitka
pip install nuitka

# Build executable
python -m nuitka --standalone --onefile tool_main.py
```

### Build Scripts

- **Windows**: `makeexe.bat` - Automated build script for Windows
- **UI Generation**: `genpy.bat` - Regenerates Python UI code from Qt Designer files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with various directory structures
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Troubleshooting

### Common Issues

**"目录不包含足够的子目录"**
- Ensure your selected directory has the required nested structure (at least 3 levels)

**"二级目录名不符合正则规则"**
- Check that your regex pattern matches the second-level directory names
- Verify the directory naming convention

**"没有权限访问路径"**
- Run the application with appropriate file system permissions
- Check directory access rights

### Debug Mode

Enable detailed logging by checking the log output window in the application interface.

## Requirements

- Python 3.6+
- PyQt5
- Operating System: Windows, Linux, macOS
- File system with read/write permissions

---

For more information or support, please refer to the source code or create an issue in the project repository.