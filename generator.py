import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def freeiptv_enigma2_ready():
    options = uc.ChromeOptions()
    # Headless modunu KESİNLİKLE KAPAT (Cloudflare'i tetikler)
    # options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    
    driver = uc.Chrome(options=options, version_main=148)
    
    try:
        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")
        print("[*] Site açıldı. Cloudflare testi bekleniyor...")
        
        # Cloudflare'in çözülmesi için bekle
        # Butonun 'disabled' özelliğinin gitmesini 30 saniye boyunca bekle
        wait = WebDriverWait(driver, 30)
        btn = wait.until(lambda d: d.find_element(By.ID, "create-btn").is_enabled())
        
        print("[*] Buton aktifleşti! Tıklanıyor...")
        driver.find_element(By.ID, "create-btn").click()
        
        time.sleep(10)
        
        # Verileri al
        with open("son_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[+] İşlem tamam, sayfa kaydedildi.")

    except Exception as e:
        print(f"[!] Hata: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    freeiptv_enigma2_ready()
