import requests
import re

# AtomSporTV
START_URL = "https://url24.link/AtomSporTV"
OUTPUT_FILE = "atom.m3u"

GREEN = "\033[92m"
RESET = "\033[0m"

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'tr-TR,tr;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://url24.link/'
}

def get_base_domain():
    try:
        response = requests.get(START_URL, headers=headers, allow_redirects=False, timeout=10)
        
        if 'location' in response.headers:
            location1 = response.headers['location']
            response2 = requests.get(location1, headers=headers, allow_redirects=False, timeout=10)
            
            if 'location' in response2.headers:
                base_domain = response2.headers['location'].strip().rstrip('/')
                print(f"Ana Domain: {base_domain}")
                return base_domain
        
        return "https://www.atomsportv480.top"
        
    except Exception as e:
        print(f"Domain hatası: {e}")
        return "https://www.atomsportv480.top"

def get_channel_m3u8(channel_id, base_domain):
    try:
        matches_url = f"{base_domain}/matches?id={channel_id}"
        response = requests.get(matches_url, headers=headers, timeout=10)
        html = response.text
        
        fetch_match = re.search(r'fetch\("(.*?)"', html)
        if not fetch_match:
            fetch_match = re.search(r'fetch\(\s*["\'](.*?)["\']', html)
        
        if fetch_match:
            fetch_url = fetch_match.group(1).strip()
            
            custom_headers = headers.copy()
            custom_headers['Origin'] = base_domain
            custom_headers['Referer'] = base_domain
            
            if not fetch_url.endswith(channel_id):
                fetch_url = fetch_url + channel_id
            
            response2 = requests.get(fetch_url, headers=custom_headers, timeout=10)
            fetch_data = response2.text
            
            m3u8_match = re.search(r'"deismackanal":"(.*?)"', fetch_data)
            if m3u8_match:
                return m3u8_match.group(1).replace('\\', '')
            
            m3u8_match = re.search(r'"(?:stream|url|source)":\s*"(.*?\.m3u8)"', fetch_data)
            if m3u8_match:
                return m3u8_match.group(1).replace('\\', '')
        
        return None
        
    except:
        return None

def get_all_possible_channels():
    channels = []

    tv_channels = [
        ("bein-sports-1", "BEIN SPORTS 1"),
        ("bein-sports-2", "BEIN SPORTS 2"),
        ("bein-sports-3", "BEIN SPORTS 3"),
        ("bein-sports-4", "BEIN SPORTS 4"),
        ("bein-sports-5", "BEIN SPORTS 5"),
        ("bein-sports-max-1", "BEIN SPORTS MAX 1"),
        ("bein-sports-max-2", "BEIN SPORTS MAX 2"),
        ("s-sport", "S SPORT"),
        ("s-sport-2", "S SPORT 2"),
    ]
    
    for channel_id, name in tv_channels:
        channels.append({
            'id': channel_id,
            'name': name,
            'group': 'WEB SPOR'
        })
    
    return channels

def test_channels(channels, base_domain):
    working_channels = []
    
    for channel in channels:
        m3u8_url = get_channel_m3u8(channel["id"], base_domain)
        
        if m3u8_url:
            channel['url'] = m3u8_url
            working_channels.append(channel)
            print(f"{GREEN}✓ {channel['name']}{RESET}")
        else:
            print(f"✗ {channel['name']}")
    
    return working_channels

def create_m3u(working_channels, base_domain):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        # Dinamik bulunan kanallar
        for channel in working_channels:
            f.write(f'#EXTINF:-1 tvg-id="{channel["id"]}" tvg-name="{channel["name"]}" group-title="TV Kanalları",{channel["name"]}\n')
            f.write(f'#EXTVLCOPT:http-referrer={base_domain}\n')
            f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
            f.write(channel["url"] + "\n")

        # ===============================
        # SABİT TABII KANALLARI (EN SONA)
        # ===============================

        f.write('\n#EXTINF:-1 group-title="TABII",Tabii\n')
        f.write('https://beert7sqimrk0bfdupfgn6qew.medya.trt.com.tr/master_1080p.m3u8\n')

        f.write('#EXTINF:-1 group-title="TABII",Tabii 1\n')
        f.write('https://iaqzu4szhtzeqd0edpsayinle.medya.trt.com.tr/master_1080p.m3u8\n')

        f.write('#EXTINF:-1 group-title="TABII",Tabii 2\n')
        f.write('https://klublsslubcgyiz7zqt5bz8il.medya.trt.com.tr/master_1080p.m3u8\n')

        f.write('#EXTINF:-1 group-title="TABII",Tabii 3\n')
        f.write('https://ujnf69op16x2fiiywxcnx41q8.medya.trt.com.tr/master_1080p.m3u8\n')

    print(f"\n{GREEN}[✓] M3U dosyası oluşturuldu: {OUTPUT_FILE}{RESET}")

def main():
    print(f"{GREEN}AtomSporTV M3U Oluşturucu{RESET}")
    print("=" * 50)

    base_domain = get_base_domain()
    channels = get_all_possible_channels()
    working_channels = test_channels(channels, base_domain)

    if not working_channels:
        print("Çalışan kanal bulunamadı.")
        return

    create_m3u(working_channels, base_domain)

if __name__ == "__main__":
    main()
