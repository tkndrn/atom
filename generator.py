import undetected_chromedriver as uc
import time
import re
import os
import shutil
from selenium.webdriver.common.by import By

def freeiptv_enigma2_ready():
    print("[*] FreeIPTV - Proxy'siz Başlatılıyor...")

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
        
        # Proxy yok, doğrudan siteye gidiyoruz
        target_url = "https://freeiptv2023-d.ottc.xyz/index.php"
        print(f"[*] Bağlanılıyor: {target_url}")
        driver.get(target_url)
        
        print("[*] 10 saniye bekleniyor...")
        time.sleep(10)

        # "Create" metnini içeren butonu bul ve tıkla
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Create')]")
        if buttons:
            print("[*] Buton bulundu, tıklanıyor...")
            buttons[0].click()
            time.sleep(15) 
        else:
            print("[!] Buton bulunamadı!")

        source = driver.page_source

        # Regex ile verileri çek
        user_pattern = r'(?:Username|User).*?(?:value=["\']|[:>]\s*)(\d{9,})'
        pwd_pattern = r'(?:Password|Pass).*?(?:value=["\']|[:>]\s*)(\d{9,})'
        
        u_match = re.search(user_pattern, source, re.IGNORECASE | re.DOTALL)
        p_match = re.search(pwd_pattern, source, re.IGNORECASE | re.DOTALL)

        if u_match and p_match:
            user = u_match.group(1)
            pwd = p_match.group(1)
            host = "http://freeiptv.ottc.xyz:80"

            with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,Free IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts")
            print(f"[+] BAŞARILI! User: {user}")
        else:
            with open("son_sayfa.html", "w", encoding="utf-8") as f: f.write(source)
            print("[-] Hata: Veri bulunamadı. son_sayfa.html dosyasını kontrol et.")

    except Exception as e: print(f"[!] Hata: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
