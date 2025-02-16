import requests
from bs4 import BeautifulSoup
import re

# Updated Website URL
PAGE_URL = "https://live.tsports.com/"

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Referer": PAGE_URL
}

# Function to fetch HLS stream URLs
def get_hls_urls():
    print(f"Fetching webpage: {PAGE_URL}")

    try:
        response = requests.get(PAGE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    print(f"Response Code: {response.status_code}")
    
    # Check if request is blocked (403 Forbidden)
    if response.status_code == 403:
        print("Access Forbidden! The website may be blocking requests.")
        return []
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find HLS URLs (handling possible obfuscation)
    m3u8_urls = set()
    
    for script in soup.find_all("script"):
        if script.string:
            found_urls = re.findall(r'https?://[^\s"]+\.m3u8[^\s"]*', script.string)
            m3u8_urls.update(found_urls)

    if not m3u8_urls:
        print("No HLS streams found.")
    else:
        print(f"Found {len(m3u8_urls)} HLS streams!")

    return list(m3u8_urls)

# Function to generate M3U playlist
def generate_m3u_playlist(m3u8_urls):
    if not m3u8_urls:
        print("No valid streams to write.")
        return None

    playlist_content = "#EXTM3U\n"
    for index, url in enumerate(m3u8_urls):
        playlist_content += f"#EXTINF:-1, T-Sports Stream {index + 1}\n{url}\n"

    with open("playlist.m3u", "w") as file:
        file.write(playlist_content)
    
    print("M3U Playlist generated successfully!")
    return "playlist.m3u"

# Main Execution
if name == "main":
    hls_urls = get_hls_urls()
    generate_m3u_playlist(hls_urls)
