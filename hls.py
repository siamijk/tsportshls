import requests
from bs4 import BeautifulSoup
import re

# Function to extract HLS m3u8 URLs from tsports.com
def get_hls_urls():
    page_url = "https://tsports.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Fetch the webpage content
    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve webpage.")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all script tags to look for m3u8 links (sometimes they are in JavaScript variables)
    m3u8_urls = []
    for script in soup.find_all('script'):
        if script.string:
            urls = re.findall(r'https?://[^\s"]+\.m3u8', script.string)
            m3u8_urls.extend(urls)

    return m3u8_urls

# Function to generate M3U playlist
def generate_m3u_playlist(m3u8_urls):
    m3u_playlist = "#EXTM3U\n"

    for index, url in enumerate(m3u8_urls):
        m3u_playlist += f"#EXTINF:-1, T-Sports Stream {index + 1}\n{url}\n"

    return m3u_playlist

# Main execution
m3u8_urls = get_hls_urls()

if m3u8_urls:
    playlist = generate_m3u_playlist(m3u8_urls)
    with open('playlist.m3u', 'w') as file:
        file.write(playlist)
    print("M3U Playlist generated successfully!")
else:
    print("No streams found.")