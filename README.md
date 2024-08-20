# Audio File Converter

This Python script allows you to convert audio files from one format to another using `pydub` and `tinytag`. It supports recursive directory scanning to find and convert files within subdirectories.

## Features

- Convert audio files from one format to another (e.g., `.flac` to `.mp3`).
- Preserve metadata such as artist, title, album, and genre during conversion.
- Recursively scan directories to find and convert audio files.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- `pydub` library
- `tinytag` library
- `ffmpeg` (required by `pydub` for audio processing)

Make sure to add the bin directory of ffmpeg to your system's PATH if you are on windows.

### Installing Python Dependencies

To install the required Python libraries, you can use `pip`:

```bash
pip install pydub tinytag
```

### Running the file
```bash
python converter.py
```
