import requests

def fetch_m3u8_content(m3u8_url):
    """
    Fetch the content of an .m3u8 file from a given URL.
    """
    try:
        response = requests.get(m3u8_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching .m3u8 content: {e}")
        return None

def parse_m3u8(content):
    """
    Parse an .m3u8 file and extract .ts file URLs or variant playlist URLs.
    """
    lines = content.splitlines()
    ts_urls = []
    for line in lines:
        if line.endswith('.ts') or line.endswith('.m3u8'):
            ts_urls.append(line)
    return ts_urls

def generate_custom_playlist(ts_urls, output_file='custom_playlist.m3u8'):
    """
    Generate a custom .m3u8 playlist from a list of .ts or .m3u8 URLs.
    """
    try:
        with open(output_file, 'w') as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-VERSION:3\n")
            f.write("#EXT-X-TARGETDURATION:10\n")
            f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
            
            for url in ts_urls:
                if url.endswith('.ts'):
                    f.write(f"#EXTINF:10.0,\n")
                f.write(f"{url}\n")
            
            f.write("#EXT-X-ENDLIST\n")
        print(f"Custom playlist generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating custom playlist: {e}")

def main():
    # Replace with the actual .m3u8 URL from live.tsports.com
    m3u8_url = "https://live.tsports.com/path/to/stream.m3u8"  # Update this URL
    
    # Fetch the .m3u8 content
    m3u8_content = fetch_m3u8_content(m3u8_url)
    
    if m3u8_content:
        # Parse the .m3u8 content to extract .ts or variant playlist URLs
        ts_urls = parse_m3u8(m3u8_content)
        
        if ts_urls:
            # Generate a custom .m3u8 playlist
            generate_custom_playlist(ts_urls)
        else:
            print("No .ts or .m3u8 URLs found in the playlist.")
    else:
        print("Failed to fetch .m3u8 content.")

if name == "main":
    main()
