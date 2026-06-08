import undetected_chromedriver as uc
import time
import re
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        
        # 1. Bekleme: Sayfanın tamamen yüklenmesi ve 5 saniyenin geçmesi
        print("[*] 10 saniye bekleniyor (Butonun açılması için)...")
        time.sleep(10)

        # 2. Butonu Garantili Bulma: 
        # Buton aktifleşene kadar bekle (WebDriverWait kullanımı)
        wait = WebDriverWait(driver, 20)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create')]")))
        
        print("[*] Buton aktifleşti, tıklanıyor...")
        driver.execute_script("arguments[0].click();", btn)
        
        print("[*] Tıklandı! 15 saniye verilerin gelmesi bekleniyor...")
        time.sleep(15)

        source = driver.page_source
        
        # ... (Regex ve dosya yazma işlemleri aynı) ...
        # (Eğer yine bulunamazsa, debug için source'u kaydettiriyoruz)
        with open("son_sayfa.html", "w", encoding="utf-8") as f: f.write(source)
        
        # ... (Regex kontrolü) ...

    except Exception as e: 
        print(f"[!] Hata: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
