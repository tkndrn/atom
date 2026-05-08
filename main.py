import asyncio
import os
from playwright.async_api import async_playwright

async def linki_sok_al():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        found_m3u8 = []
        page.on("request", lambda req: found_m3u8.append(req.url) if ".m3u8" in req.url and "token=" in req.url else None)

        try:
            await page.goto("https://ntv.cx/channel-cdnlive/beIN-SPORTS-1?code=tr", timeout=60000)
            for _ in range(15):
                if found_m3u8: break
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Hata: {e}")
        finally:
            await browser.close()

        if found_m3u8:
            # M3U içeriğini oluştur
            m3u_content = f'#EXTM3U\n#EXTINF:-1 group-title="SPOR",beIN SPORTS 1\n{found_m3u8[0]}'
            with open("live.m3u", "w") as f:
                f.write(m3u_content)
            print("Link başarıyla live.m3u dosyasına yazıldı.")
        else:
            print("Link yakalanamadı.")

if __name__ == "__main__":
    asyncio.run(linki_sok_al())
