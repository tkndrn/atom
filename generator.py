import os
import shutil
import time

import undetected_chromedriver as uc


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
        print("[*] URL:", driver.current_url)

        with open("ilk_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[+] ilk_sayfa.html kaydedildi")

        time.sleep(5)

        print("[*] Buton zorla aktif ediliyor...")

        driver.execute_script("""
            var btn = document.getElementById('create-btn');
            if(btn){
                btn.disabled = false;
            }
        """)

        time.sleep(2)

        print("[*] Form submit ediliyor...")

        driver.execute_script("""
            document.querySelector('form').submit();
        """)

        time.sleep(10)

        print("[*] Son durum kaydediliyor...")

        with open("son_sayfa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        with open("tum_html.txt", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print("[+] son_sayfa.html kaydedildi")
        print("[*] Son URL:", driver.current_url)
        print("[*] Son Baslik:", driver.title)

        print("\n========== HTML ILK 5000 KARAKTER ==========\n")
        print(driver.page_source[:5000])

    except Exception as e:

        print("[!] HATA:")
        print(str(e))

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
