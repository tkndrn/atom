import asyncio
from playwright.async_api import async_playwright

async def m3u8_bul_ve_kaydet():
    hedef_url = "https://beyazelma78.com/api/embed?u=UEsNIJ06uXbHrsROfQlACapvK5Da4ul3BxgoXvo9Kbc7uMHeMiqgdwbeGTR1j-TOl_YzU67mirvoPXvuA0wmvBFEo32ww1SZtVCCC42RFmj-bfw"
    
    print("[*] GitHub Actions üzerinde Playwright başlatılıyor...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            extra_http_headers={
                "Referer": "https://beyazelma78.com/"
            }
        )
        
        page = await context.new_page()
        yakalanan_link = None
        
        def handle_request(request):
            nonlocal yakalanan_link
            url = request.url
            if ".m3u8" in url.lower() or "format=.m3u8" in url.lower():
                yakalanan_link = url
                print(f"[+] Hedef Link Yakalandı: {url}")

        page.on("request", handle_request)
        
        try:
            await page.goto(hedef_url, timeout=30000)
            await asyncio.sleep(7) # Shaka player ve isteklerin tetiklenmesi için bekleme
            
            if yakalanan_link:
                with open("stream.txt", "w", encoding="utf-8") as f:
                    f.write(yakalanan_link)
                print("[+] Link 'stream.txt' dosyasına başarıyla kaydedildi.")
            else:
                print("[-] Link yakalanamadı!")
        except Exception as e:
            print(f"[-] Hata oluştu: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(m3u8_bul_ve_kaydet())
