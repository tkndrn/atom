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
        driver.get(url)
        time.sleep(30) 

        # Butona basma
        driver.execute_script("if(document.getElementById('create-btn')) document.getElementById('create-btn').click();")
        print("[*] Butona basıldı, veriler bekleniyor...")
        time.sleep(25) 

        source = driver.page_source

        # ÇOK GENİŞLETİLMİŞ REGEX: 
        # 1. Hem düz metin içindeki sayıları arar
        # 2. Hem de input kutularının 'value' değerlerini arar
        user_pattern = r'(?:Username|User).*?(?:value=["\']|[:>]\s*)(\d{9,})'
        pwd_pattern = r'(?:Password|Pass).*?(?:value=["\']|[:>]\s*)(\d{9,})'
        
        u_match = re.search(user_pattern, source, re.IGNORECASE | re.DOTALL)
        p_match = re.search(pwd_pattern, source, re.IGNORECASE | re.DOTALL)

        if u_match and p_match:
            user = u_match.group(1)
            pwd = p_match.group(1)
            host = "http://freeiptv.ottc.xyz:80" # Host genellikle sabittir

            with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,Free IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts")
            print(f"[+] BAŞARILI! User: {user} | Pass: {pwd}")
        else:
            with open("son_sayfa.html", "w", encoding="utf-8") as f: f.write(source)
            print("[-] Hata: Veri bulunamadı. son_sayfa.html dosyasını kontrol et.")

    except Exception as e: print(f"[!] Hata: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
