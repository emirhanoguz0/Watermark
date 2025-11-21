# Quick Watermark Tool

A simple and user-friendly application for adding watermarks to MP4 videos.

## Features

- **Easy to Use**: Simple drag-and-drop video selection
- **Customizable Watermark**: Text, font, and size selection
- **Output Control**: Save to any directory you choose
- **Real-time Progress**: Track processing status
- **Threading**: Video processing without UI freezing
- **Single File**: No installation required

## Usage

1. **Watermark Text**: Enter your watermark text
2. **Input Video**: Select video file (using Browse button)
3. **Output Directory**: Choose output folder
4. **Font & Size**: Select font and size
5. **Process Video**: Start processing

## Technical Details

- **Python**: 3.12
- **GUI**: Tkinter
- **Video Processing**: MoviePy
- **Font Processing**: Pillow (PIL)
- **Build Tool**: PyInstaller

## Requirements

- Windows 10/11
- FFmpeg (automatically downloaded on first run)

## Installation

### Developer Setup
```bash
git clone https://github.com/emirhanoguz0/Watermark
cd Watermark
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python adwwafwgv.py
```

### End User
Run `dist/Watermark.exe`. No installation required.

## Supported Formats

- **Input**: MP4
- **Output**: MP4 (H.264/AAC)

## License

This project is licensed under the MIT License.
