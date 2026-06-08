import undetected_chromedriver as uc
import time
import re
import os
import shutil
from selenium.webdriver.common.by import By

def freeiptv_enigma2_ready():
    print("[*] Başlatılıyor...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=148)
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Siteye girildi, 15 saniye bekleniyor...")
        time.sleep(15)

        # Hata olsa bile içeriği alabilmek için
        source = driver.page_source
        
        # Butona basma denemesi
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            found = False
            for btn in buttons:
                if "Create" in btn.text:
                    btn.click()
                    print("[*] Butona tıklandı!")
                    found = True
                    time.sleep(10)
                    source = driver.page_source
                    break
            if not found: print("[!] Buton bulunamadı, mevcut sayfa kaydediliyor.")
        except Exception as e:
            print(f"[!] Butona tıklarken hata: {e}")

        # Kayıt işlemi
        with open("son_sayfa.html", "w", encoding="utf-8") as f: f.write(source)
        
        # ... (Regex kısımlarını buraya ekle) ...
        # (Regex'i kodun sonuna ekledim)
        
    except Exception as e:
        print(f"[!] Kritik hata: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
