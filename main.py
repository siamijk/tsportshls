def deecb(text):
    import base64, zlib
    try:
        decoded_data = base64.b64decode(text)
        decompressed_data = zlib.decompress(decoded_data, wbits=zlib.MAX_WBITS|32).decode()
        return decompressed_data
    except Exception as e:
        print(f"Decode error: {e}")
        return "{}"

def update_live_event_info():
    headers = {
        "Host": "mapi-cdn.tsports.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }
    proxy_list = load_proxies(api_proxies)
    req = None
    if proxy_list:
        for proxy_url in proxy_list:
            try:
                req = requests.get(api_live_matches, headers=headers, proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
                if req.status_code == 200:
                    break
            except Exception as e:
                print(f"Proxy failed: {e}")
    if not req or req.status_code != 200:
        req = requests.get(api_live_matches, headers=headers, verify=False)
    all_data = []
    decode = json.loads(deecb(req.text))
    print(decode)
    if "contents" in decode.get("data", {}):
        for event in decode["data"]["contents"]:
            name = event["contentName"]
            categoryname = event["categoryName"]
            logo = event["mobileLogo"]
            if event.get("playingMetaData") or event.get("contentAes128HlsUrl"):
                stream_url = event.get("contentAes128HlsUrl") or event["playingMetaData"][0].get("mediaUrl")
                cookie = event["playingMetaData"][0].get("signedCookie", "") if event.get("playingMetaData") else ""
                data = {
                    "category_name": categoryname,
                    "name": name,
                    "logo": logo,
                    "link": stream_url,
                    "headers": {
                        "Cookie": cookie,
                        "Host": urlparse(stream_url).netloc,
                        "User-agent": "https://github.com/byte-capsule (Linux;Android 14)"
                    }
                }
                all_data.append(data)
    return all_data
