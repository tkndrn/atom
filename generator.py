import undetected_chromedriver as uc
import time
import re
import os
import shutil

def freeiptv_enigma2_ready():
    print("[*] FreeIPTV - Başlatılıyor...")

    cache_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'undetected_chromedriver')
    if os.path.exists(cache_path):
        try: shutil.rmtree(cache_path)
        except: pass

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=148)
        
        # Proxy üzerinden siteye giriş
        url = "https://ronaldo.magnitude.workers.dev/?url=https://freeiptv2023-d.ottc.xyz/index.php"
        print(f"[*] Bağlanılıyor: {url}")
        driver.get(url)
        time.sleep(30) # Sayfanın tam yüklenmesi için 30 sn

        # Butona basma
        driver.execute_script("if(document.getElementById('create-btn')) document.getElementById('create-btn').click();")
        print("[*] Butona basıldı, 20 sn bekleniyor...")
        time.sleep(20)

        source = driver.page_source
        print(f"[*] Sayfa uzunluğu: {len(source)}") # Debug için çok önemli

        # Çok yönlü Regex
        username_match = re.search(r'Username[:\s]*</strong>[:\s]*(\d{9,})|Username.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        password_match = re.search(r'Password[:\s]*</strong>[:\s]*(\d{9,})|Password.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        host_match = re.search(r'(http[s]?://[a-zA-Z0-9.-]+)', source)

        if username_match and password_match:
            user = username_match.group(1) or username_match.group(2)
            pwd = password_match.group(1) or password_match.group(2)
            host = host_match.group(1) if host_match else "http://freeiptv.ottc.xyz:80"

            with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,Free IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts")
            print("[+] BAŞARILI! Dosya oluşturuldu.")
        else:
            with open("son_sayfa.html", "w", encoding="utf-8") as f: f.write(source)
            print("[-] Hata: Credential bulunamadı. son_sayfa.html dosyasına bakın.")

    except Exception as e: print(f"[!] Hata: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
