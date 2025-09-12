
"""
YouTube MP3 Downloader for Windows
Searches YouTube for videos based on keywords and downloads them as MP3 files.

SETUP INSTRUCTIONS:
1. Install required package:
   pip install yt-dlp
   
2. Install FFmpeg:
   Download from https://www.gyan.dev/ffmpeg/builds/ and add to PATH
"""

import os
import sys
import subprocess
from typing import List, Dict

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("=== Checking Dependencies ===")
    
    # Check Python packages
    try:
        import yt_dlp
        print("yt-dlp found")
    except ImportError:
        print("yt-dlp not found")
        print("Install with: pip install yt-dlp")
        return False

    print("Using yt-dlp for search (no additional search package needed)")
    
    # Check FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("FFmpeg found")
            return True
        else:
            print("FFmpeg not working properly")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("FFmpeg not found")
        print("Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/")
        print("Add ffmpeg/bin folder to your Windows PATH")
        return False
    
    return True

def search_youtube(query: str, limit: int = 10) -> List[Dict]:
    """Search YouTube for videos based on query using yt-dlp"""
    import yt_dlp
    
    try:
        # Use yt-dlp to search YouTube directly
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Only get metadata, don't download
        }
        
        search_query = f"ytsearch{limit}:{query}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(search_query, download=False)
        
        videos = []
        if search_results and 'entries' in search_results:
            for video in search_results['entries']:
                if video:  # Sometimes entries can be None
                    videos.append({
                        'title': video.get('title', 'Unknown Title'),
                        'url': f"https://www.youtube.com/watch?v={video.get('id', '')}",
                        'duration': video.get('duration_string', 'Unknown'),
                        'channel': video.get('uploader', 'Unknown Channel'),
                    })
        
        return videos
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def download_as_mp3(video_url: str, output_dir: str = "downloads") -> bool:
    """Download a YouTube video as MP3"""
    import yt_dlp
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # yt-dlp options for MP3 extraction
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'extractaudio': True,
            'audioformat': 'mp3',
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def get_user_subjects() -> List[Dict[str, int]]:
    """Get subjects and video counts from user input"""
    subjects = []
    
    print("\n=== YouTube MP3 Downloader ===")
    print("Enter subjects/keywords you want to search for.")
    print("For each subject, specify how many videos to download.")
    print("Press Enter with empty subject to finish.\n")
    
    while True:
        subject = input("Enter subject/keywords (or press Enter to finish): ").strip()
        if not subject:
            break
            
        while True:
            try:
                count = int(input(f"How many videos for '{subject}'? "))
                if count > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        subjects.append({
            'subject': subject,
            'count': count
        })
        
        print(f"Added: {subject} ({count} videos)\n")
    
    return subjects

def main():
    """Main function"""
    print("YouTube MP3 Downloader for Windows - FIXED VERSION")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        input("Press Enter to exit...")
        return
    
    print("All dependencies found!\n")
    
    # Get subjects from user
    subjects = get_user_subjects()
    
    if not subjects:
        print("No subjects specified. Exiting.")
        input("Press Enter to exit...")
        return
    
    # Create main downloads directory
    downloads_dir = "YouTube_Downloads"
    try:
        os.makedirs(downloads_dir, exist_ok=True)
        print(f"Downloads will be saved to: {os.path.abspath(downloads_dir)}\n")
    except Exception as e:
        print(f"Error creating downloads directory: {e}")
        input("Press Enter to exit...")
        return
    
    total_downloaded = 0
    total_failed = 0
    
    print("=== Starting Downloads ===\n")
    
    for subject_info in subjects:
        subject = subject_info['subject']
        count = subject_info['count']
        
        print(f"Processing: '{subject}' ({count} videos)")
        
        # Create subdirectory for this subject
        safe_name = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).strip()
        subject_dir = os.path.join(downloads_dir, safe_name.replace(" ", "_"))
        
        # Search YouTube
        videos = search_youtube(subject, count)
        
        if not videos:
            print(f"  No videos found for '{subject}'\n")
            continue
        
        print(f"  Found {len(videos)} videos")
        
        # Download each video
        for i, video in enumerate(videos[:count], 1):
            title = video['title'][:50] + ("..." if len(video['title']) > 50 else "")
            print(f"  [{i}/{count}] {title}")
            
            if download_as_mp3(video['url'], subject_dir):
                print(f"    ✓ Downloaded successfully")
                total_downloaded += 1
            else:
                print(f"    ✗ Download failed")
                total_failed += 1
        
        print(f"  Completed '{subject}'\n")
    
    # Summary
    print("=" * 40)
    print("DOWNLOAD SUMMARY")
    print("=" * 40)
    print(f"Successfully downloaded: {total_downloaded} videos")
    print(f"Failed downloads: {total_failed}")
    print(f"Files saved in: {os.path.abspath(downloads_dir)}")
    
    if total_downloaded > 0:
        print(f"\nYour MP3 files are ready!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()