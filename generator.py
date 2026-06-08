import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def freeiptv_enigma2_ready():
    options = uc.ChromeOptions()

    # GitHub Actions / Linux için gerekli
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = None

    try:
        print("[*] Chrome baslatiliyor...")

        driver = uc.Chrome(
            options=options,
            use_subprocess=True
        )

        print("[*] Site aciliyor...")

        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")

        print("[*] Baslik:", driver.title)

        # İlk sayfanın kaydı
        with open("ilk_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[*] Cloudflare / buton kontrolu bekleniyor...")

        wait = WebDriverWait(driver, 60)

        wait.until(
            EC.element_to_be_clickable((By.ID, "create-btn"))
        )

        print("[+] Buton aktif!")

        btn = driver.find_element(By.ID, "create-btn")
        btn.click()

        print("[*] Tiklandi, sonuc bekleniyor...")
        time.sleep(10)

        with open("son_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[+] son_sayfa.html kaydedildi")

        # Eğer M3U linkleri oluşmuşsa görmek için
        links = driver.find_elements(By.TAG_NAME, "a")

        with open("linkler.txt", "w", encoding="utf-8") as f:
            for link in links:
                href = link.get_attribute("href")
                if href:
                    f.write(href + "\n")

        print(f"[+] {len(links)} adet link bulundu")

    except Exception as e:
        print("[!] HATA:")
        print(str(e))

        try:
            if driver:
                with open("hata_sayfasi.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("[*] hata_sayfasi.html kaydedildi")
        except:
            pass

        raise

    finally:
        try:
            if driver:
                driver.quit()
        except:
            pass


if __name__ == "__main__":
    freeiptv_enigma2_ready()
