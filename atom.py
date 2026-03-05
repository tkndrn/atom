import requests
import re

# -----------------------
# Ayarlar
# -----------------------
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

START_URL = "https://url24.link/AtomSporTV"

# -----------------------
# 1️⃣ Base domain bulma
# -----------------------
def get_base_domain():
    try:
        response = requests.get(START_URL, headers=headers, allow_redirects=False, timeout=10)
        if 'location' in response.headers:
            loc1 = response.headers['location']
            response2 = requests.get(loc1, headers=headers, allow_redirects=False, timeout=10)
            if 'location' in response2.headers:
                return response2.headers['location'].strip().rstrip('/')
        return "https://www.atomsportv480.top"
    except:
        return "https://www.atomsportv480.top"

# -----------------------
# 2️⃣ Atom kanallarını çek
# -----------------------
def get_channel_m3u8(channel_id, base_domain):
    try:
        matches_url = f"{base_domain}/matches?id={channel_id}"
        response = requests.get(matches_url, headers=headers, timeout=10)
        html = response.text
        
        fetch_match = re.search(r'fetch\(["\'](.*?)["\']', html)
        if fetch_match:
            fetch_url = fetch_match.group(1).strip()
            custom_headers = headers.copy()
            custom_headers['Origin'] = base_domain
            custom_headers['Referer'] = base_domain
            
            if not fetch_url.endswith(channel_id):
                fetch_url += channel_id
                
            response2 = requests.get(fetch_url, headers=custom_headers, timeout=10)
            data = response2.text
            
            m3u8_match = re.search(r'"deismackanal":"(.*?)"', data)
            if m3u8_match:
                return m3u8_match.group(1).replace('\\','')
            
            m3u8_match = re.search(r'"(?:stream|url|source)":\s*"(.*?\.m3u8)"', data)
            if m3u8_match:
                return m3u8_match.group(1).replace('\\','')
        return None
    except:
        return None

def get_all_possible_channels():
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
    channels = []
    for cid, name in tv_channels:
        channels.append({'id': cid, 'name': name, 'group': 'WEB SPOR'})
    return channels

def test_channels(channels, base_domain):
    working = []
    for c in channels:
        url = get_channel_m3u8(c["id"], base_domain)
        if url:
            c['url'] = url
            working.append(c)
            print(f"{GREEN}✓ {c['name']}{RESET}")
        else:
            print(f"✗ {c['name']}")
    return working

# -----------------------
# 3️⃣ M3U oluştur
# -----------------------
def create_m3u(base_domain, working_channels):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        
        # ---- Senin özel linklerin ----
        custom_links = [
            ("Bien B1", "https://api.codetabs.com/v1/proxy/?quest=https://andro.226503.xyz/checklist/androstreamlivebiraz1.m3u8"),
            ("Bien 1", "https://cdn-albert.mobiligtv.com/test2f4649e5/wVYKseQKxM/streams/bein-sports-1/playlist.m3u8")
        ]
        
        for name, url in custom_links:
            f.write(f"#EXTINF:-1,{name}\n")
            f.write(url + "\n\n")
        
        # ---- AtomSporTV kanalları ----
        for c in working_channels:
            f.write(f'#EXTINF:-1 tvg-id="{c["id"]}" tvg-name="{c["name"]}" group-title="TV Kanalları",{c["name"]}\n')
            f.write(f'#EXTVLCOPT:http-referrer={base_domain}\n')
            f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
            f.write(c["url"] + "\n\n")
        
        # ---- Tabii kanalları ----
        tabii = [
            "https://beert7sqimrk0bfdupfgn6qew.medya.trt.com.tr/master_1080p.m3u8",
            "https://iaqzu4szhtzeqd0edpsayinle.medya.trt.com.tr/master_1080p.m3u8",
            "https://klublsslubcgyiz7zqt5bz8il.medya.trt.com.tr/master_1080p.m3u8",
            "https://ujnf69op16x2fiiywxcnx41q8.medya.trt.com.tr/master_1080p.m3u8",
            "https://bfxy3jgeydpbphtk8qfqwm3hr.medya.trt.com.tr/master_1080p.m3u8",
            "https://z3mmimwz148csv0vaxtphqspf.medya.trt.com.tr/master_1080p.m3u8",
            "https://vbtob9hyq58eiophct5qctxr2.medya.trt.com.tr/master_1080p.m3u8",
        ]
        for i, url in enumerate(tabii):
            f.write(f'#EXTINF:-1 group-title="TABII",Tabii {i}\n')
            f.write(url + "\n\n")
        
    print(f"\n{GREEN}[✓] M3U dosyası oluşturuldu: {OUTPUT_FILE}{RESET}")

# -----------------------
# Main
# -----------------------
def main():
    print(f"{GREEN}AtomSporTV + Özel Link + Tabii M3U Oluşturucu{RESET}")
    base_domain = get_base_domain()
    channels = get_all_possible_channels()
    working = test_channels(channels, base_domain)
    create_m3u(base_domain, working)

if __name__ == "__main__":
    main()
