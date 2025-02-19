#Tsports Cookie Updater Script (Modified)
#By JESHAN AKAND
#Date 16/12/23

import requests
import json
import os

# Environment Variables
api_live_matches = os.getenv("api_live_matches", "")  # Set default empty string to avoid KeyError

def update_time():
    from datetime import datetime
    import pytz

    IST = pytz.timezone('Asia/Dhaka')   
    today_date = datetime.now(IST).strftime("%d-%m-%Y")  # Current Date
    curr_time = datetime.now(IST).strftime("%I:%M:%S %p")  # Current Time with AM/PM
    return curr_time, today_date

def update_live_event_info():
    headers = {
        "Host": "mapi-cdn.tsports.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }
    
    try:
        req = requests.get(api_live_matches, headers=headers, verify=True)
        decode = req.json()  # Assume API returns JSON directly
    except Exception as e:
        print(f"Error fetching live matches: {e}")
        return []
    
    all_data = []
    
    if "data" in decode and "contents" in decode["data"]:
        for event in decode["data"]["contents"]:
            name = event.get("contentName", "Unknown")
            categoryname = event.get("categoryName", "Unknown")
            logo = event.get("mobileLogo", "")
            
            if event.get("playingMetaData"):
                for link_data in event["playingMetaData"]:
                    if link_data.get("isActive") == 1:
                        link = link_data.get("mediaUrl", "")
                        cookie = link_data.get("signedCookie", "")
                        
                        data = {
                            "category_name": categoryname,
                            "name": name,
                            "logo": logo,
                            "link": link,
                            "headers": {
                                "Cookie": cookie,
                                "Host": "live-cdn.tsports.com",
                                "User-Agent": "https://github.com/byte-capsule (Linux;Android 14)"
                            }
                        }
                        all_data.append(data)
    
    return all_data

def json_formatter(name, output_file_name, data):
    date_time = update_time()
    metadata = {
        "name": name,
        "owner": "Byte Capsule \nTelegram: https://t.me/J_9X_H_9X_N\nGithub:https://github.com/byte-capsule",
        "channels_amount": len(data),
        "updated_on": f"{date_time[1]} on {date_time[0]}",
        "channels": data
    }
    
    with open(output_file_name, "w") as w:
        json.dump(metadata, w, indent=2)

def ns_player_playlist_converter(output_file_name, json_data):
    all_data_ns = []
    for data in json_data:
        formatted_data = {
            "name": data["name"],
            "link": data["link"],
            "logo": data["logo"],
            "origin": "https://" + data["headers"]["Host"],
            "referrer": "https://" + data["headers"]["Host"],
            "userAgent": "Tsports (Linux; Telegram:https://t.me/J_9X_H_9X_N) Github:https://github.com/byte-capsule AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
            "cookie": data["headers"]["Cookie"],
            "drmScheme": "",
            "drmLicense": ""
        }
        all_data_ns.append(formatted_data)
        
    with open(output_file_name, "w") as w:
        json.dump(all_data_ns, w, indent=2)

def ott_navigator_playlist_converter(output_file_name, json_data):
    final_text = ""
    for content in json_data:
        final_text += f'#EXTINF:-1 group-title="{content["category_name"]}" tvg-logo="{content["logo"]}", {content["name"]}\n'
        final_text += f'#EXTVLCOPT:http-user-agent={content["headers"]["User-Agent"]}\n'
        final_text += f'#EXTHTTP:{{"cookie":"{content["headers"]["Cookie"]}"}}\n'
        final_text += f'{content["link"]}\n'
    
    with open(output_file_name, "w") as w:
        w.write(final_text)
        
if __name__ == "__main__":
    # Update Live Event Data
    data = update_live_event_info()
    
    # Convert to JSON Format
    json_formatter("TSports App All Live Matches Data", "TSports_m3u8_headers.Json", data)
    
    # Convert to NS Player Playlist
    ns_player_playlist_converter("NS_Player_Tsports_live.m3u", data)
    
    # Convert to OTT Navigator Playlist
    ott_navigator_playlist_converter("OTT_Navigator_Tsports_live.m3u", data)
    
    print("Playlist files generated successfully!")
