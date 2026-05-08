import asyncio
import os
from playwright.async_api import async_playwright

async def linki_sok_al():
    async with async_playwright() as p:
        # headless=True kalsın, GitHub Actions için şart
        browser = await p.chromium.launch(headless=True)
        # Daha gerçekçi bir tarayıcı profili
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        found_m3u8 = []
        # Link yakalayıcı
        page.on("request", lambda req: found_m3u8.append(req.url) if ".m3u8" in req.url and "token=" in req.url else None)

        print("Siteye gidiliyor...")
        try:
            # networkidle: Ağ trafiği durana kadar bekle demek
            await page.goto("https://ntv.cx/channel-cdnlive/beIN-SPORTS-1?code=tr", wait_until="networkidle", timeout=60000)
            
            # Ekstra bekleme süresi (Oynatıcı JS'yi çalıştırsın)
            for i in range(20):
                if found_m3u8:
                    print(f"Link yakalandı! Deneme: {i}")
                    break
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")
        finally:
            await browser.close()

        if found_m3u8:
            m3u_link = found_m3u8[0]
            m3u_content = f'#EXTM3U\n#EXTINF:-1 group-title="SPOR",beIN SPORTS 1\n{m3u_link}'
            with open("live.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("live.m3u dosyası başarıyla yazıldı.")
        else:
            print("MAALESEF LİNK BULUNAMADI.")

if __name__ == "__main__":
    asyncio.run(linki_sok_al())
