import os
import shutil
import time

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def freeiptv_enigma2_ready():

    # UC cache temizle
    cache = os.path.expanduser("~/.local/share/undetected_chromedriver")
    if os.path.exists(cache):
        shutil.rmtree(cache, ignore_errors=True)

    options = uc.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = None

    try:
        print("[*] Chrome baslatiliyor...")

        driver = uc.Chrome(
            version_main=148,
            options=options,
            use_subprocess=True
        )

        print("[*] Site aciliyor...")

        driver.get("https://freeiptv2023-d.ottc.xyz/index.php")

        print("[*] Baslik:", driver.title)

        with open("ilk_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[*] Buton bekleniyor...")

        wait = WebDriverWait(driver, 60)

        button = wait.until(
            EC.element_to_be_clickable((By.ID, "create-btn"))
        )

        print("[+] Buton bulundu")

        button.click()

        print("[*] Sonuc bekleniyor...")
        time.sleep(15)

        with open("son_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[+] son_sayfa.html kaydedildi")

        links = driver.find_elements(By.TAG_NAME, "a")

        with open("linkler.txt", "w", encoding="utf-8") as f:
            for link in links:
                href = link.get_attribute("href")
                if href:
                    f.write(href + "\n")

        print(f"[+] {len(links)} link bulundu")

    except Exception as e:

        print("[!] HATA:")
        print(e)

        try:
            if driver:
                with open("hata_sayfasi.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
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
