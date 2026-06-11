#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def download_youtube_music(url, output_dir="downloads"):
    """
    Скачивает видео с YouTube и конвертирует в MP3
    
    Использование:
        python3 youtube_downloader.py "https://www.youtube.com/watch?v=..."
    """
    
    Path(output_dir).mkdir(exist_ok=True)
    
    print("🎵 YouTube Music Downloader")
    print("=" * 50)
    print(f"URL: {url}")
    print()
    
    try:
        print("📥 Downloading and converting to MP3...")
        
        cmd = [
            'yt-dlp',
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', '192',
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        
        print("✅ Download complete!")
        print(f"📁 Saved to: {output_dir}/")
        
        files = list(Path(output_dir).glob('*.mp3'))
        if files:
            print(f"📊 Files created:")
            for f in files[-1:]:
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"   • {f.name} ({size_mb:.1f} MB)")
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: yt-dlp not installed")
        print("   Install: pip install yt-dlp --break-system-packages")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_downloader.py 'YOUTUBE_URL'")
        sys.exit(1)
    
    url = sys.argv[1]
    success = download_youtube_music(url)
    sys.exit(0 if success else 1)
