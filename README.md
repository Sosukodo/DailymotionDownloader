# Dailymotion Video Downloader

A simple Python script to download videos from Dailymotion using their metadata API and ffmpeg.

## What it does

This tool fetches video metadata from Dailymotion's internal API, extracts the M3U8 stream URL, and downloads the video directly using ffmpeg. It's designed to be straightforward and reliable - no fancy UI, just gets the job done.

## Requirements

- Python 3.6+
- ffmpeg (must be installed and accessible in your PATH)
- `requests` library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/DailymotionDownloader.git
cd DailymotionDownloader
```

2. Install the required Python package:
```bash
pip install requests
```

3. Make sure ffmpeg is installed:
```bash
# On Ubuntu/Debian
sudo apt install ffmpeg

# On macOS with Homebrew
brew install ffmpeg

# On Windows, download from https://ffmpeg.org/download.html
```

## Usage

### Command line argument:
```bash
python cli.py "https://www.dailymotion.com/video/your-video-id"
```

### Interactive mode:
```bash
python cli.py
```
The script will ask you to enter the Dailymotion video URL.

## How it works

1. **Extracts video ID** from the Dailymotion URL
2. **Fetches metadata** using Dailymotion's player API
3. **Finds the M3U8 stream** from the metadata
4. **Downloads directly** using ffmpeg (no manual segment handling)
5. **Fallback encoding** if direct copy fails

## Features

- ✅ Direct M3U8 stream download
- ✅ Automatic fallback to re-encoding if needed
- ✅ Skip download if file already exists
- ✅ Clean error handling
- ✅ No manual segment stitching required

## Output

Videos are saved as `output_video.mp4` in the current directory. The script will skip downloading if the file already exists.

## Troubleshooting

**"Failed to fetch M3U8 file"**: The video might be geo-blocked or the URL format has changed.

**ffmpeg errors**: Make sure ffmpeg is properly installed and accessible from your command line.

**JSON decode errors**: The Dailymotion API might have changed or the video might not be available.

## Technical Notes

This script uses Dailymotion's internal metadata API endpoint. While this works well currently, keep in mind that internal APIs can change without notice. The script includes error handling for common issues, but you might need to update it if Dailymotion changes their API structure.

The download process uses ffmpeg's native HLS support, which handles stream discontinuities much better than manual segment downloading and joining.

## License

This project is for educational purposes. Please respect Dailymotion's terms of service and only download videos you have permission to download.

## Contributing

Feel free to submit issues or pull requests if you find bugs or want to improve the code!
