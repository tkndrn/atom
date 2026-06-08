import undetected_chromedriver as uc
import time
import re
import os
import shutil
from selenium.webdriver.common.by import By

def freeiptv_enigma2_ready():
    print("[*] FreeIPTV - Başlatılıyor...")

    # Önbellek temizliği
    cache_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'undetected_chromedriver')
    if os.path.exists(cache_path):
        try:
            shutil.rmtree(cache_path)
        except:
            pass

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Proxy ayarı
    proxy = "https://ronaldo.magnitude.workers.dev/?url="
    options.add_argument(f"--proxy-server={proxy}")

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=148)

        # IP kontrolü (Proxy çalışıyor mu?)
        driver.get("https://api.ipify.org")
        print(f"[*] Bağlanılan IP: {driver.find_element(By.TAG_NAME, 'body').text}")

        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Sayfa açıldı, bekleniyor...")
        time.sleep(20)

        driver.execute_script("""
            let btn = document.getElementById('create-btn');
            if (btn) {
                btn.scrollIntoView();
                btn.click();
            }
        """)

        print("[*] Butona basıldı, 15 saniye bekleniyor...")
        time.sleep(15)

        source = driver.page_source

        username_match = re.search(r'Username.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        password_match = re.search(r'Password.*?(\d{9,})', source, re.IGNORECASE | re.DOTALL)
        host_match = re.search(r'(http[s]?://[^\s"\'<>]+)', source)

        if username_match and password_match:
            user = username_match.group(1)
            pwd = password_match.group(1)
            host = host_match.group(1).rstrip('/') if host_match else "http://freeiptv.ottc.xyz:80"

            print(f"✅ BAŞARILI! Kullanıcı: {user}")

            m3u_content = f"#EXTM3U\n#EXTINF:-1,Free IPTV\n{host}/get.php?username={user}&password={pwd}&type=m3u_plus&output=ts"
            
            with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("[+] M3U dosyası oluşturuldu: iptv_listem.m3u")
        else:
            print("[-] Credential bulunamadı, sayfa içeriği kaydediliyor.")
            with open("son_sayfa.html", "w", encoding="utf-8") as f:
                f.write(source)

    except Exception as e:
        print(f"[!] Kritik Hata: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
