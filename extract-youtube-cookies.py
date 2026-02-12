#!/usr/bin/env python3
"""
Extract only YouTube and Google cookies from cookies.txt
This creates a clean, minimal cookies file for yt-dlp
"""

import os

def extract_youtube_cookies():
    input_file = "cookies.txt"
    output_file = "cookies-youtube-only.txt"
    
    if not os.path.exists(input_file):
        print(f"❌ {input_file} not found!")
        return
    
    # Domains we need for YouTube
    youtube_domains = [
        ".youtube.com",
        "youtube.com",
        ".google.com",
        "google.com",
        ".google.co.in",
        "google.co.in",
        "accounts.google.com",
        ".doubleclick.net"
    ]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Keep header and YouTube-related cookies
    youtube_lines = []
    for line in lines:
        # Keep comments and headers
        if line.startswith('#'):
            youtube_lines.append(line)
            continue
        
        # Skip empty lines
        if not line.strip():
            continue
        
        # Check if line contains YouTube/Google domain
        parts = line.split('\t')
        if len(parts) >= 1:
            domain = parts[0]
            if any(yt_domain in domain for yt_domain in youtube_domains):
                youtube_lines.append(line)
    
    # Write clean cookies file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(youtube_lines)
    
    original_size = len(lines)
    new_size = len([l for l in youtube_lines if not l.startswith('#')])
    
    print(f"✅ Extracted YouTube cookies!")
    print(f"📊 Original: {original_size} lines")
    print(f"📊 YouTube-only: {new_size} cookies")
    print(f"📁 Saved to: {output_file}")
    print(f"\n🔥 File size reduced by {100 - (new_size * 100 // original_size)}%")
    print(f"\n📝 Next steps:")
    print(f"1. Replace cookies.txt with cookies-youtube-only.txt")
    print(f"2. Push to GitHub")
    print(f"3. Railway will auto-deploy")

if __name__ == "__main__":
    extract_youtube_cookies()
