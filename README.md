# YouTube MP3 Downloader - Complete Setup Guide

## Prerequisites

Before installing, make sure you have:
- **Python**: Version 3.7 or higher




## Installation Guide

### 1: Install Python Package

Open your terminal/command prompt and install the required package:

```bash
pip install yt-dlp
```

### 2: Install FFmpeg

FFmpeg is required for audio conversion to MP3 format.

#### Windows Installation

**Option A: Direct Download (Recommended)**
1. Go to [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Click **"release builds"**
3. Download **"ffmpeg-release-essentials.zip"**
4. Extract to `C:\ffmpeg`
5. Add `C:\ffmpeg\bin` to Windows PATH:
   - Press `Win + X` → Select **"System"**
   - Click **"Advanced system settings"**
   - Click **"Environment Variables"**
   - Under **"System Variables"**, find **"Path"** → Click **"Edit"**
   - Click **"New"** → Add: `C:\ffmpeg\bin`
   - Click **"OK"** on all dialogs
   - **Restart Command Prompt**


**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

### Running Script
1. ```python YTMP3SubjectDownloader.py```
2. Enter phrase for content desired
3. Enter how many number of those videos wanted
4. Enter (to exit) if not continue steps 2-3 
5. Folder will create in file