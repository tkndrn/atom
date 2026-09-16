import asyncio
from playwright.async_api import async_playwright

async def tek_kanal_coz(hedef_url):
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

        page.on("request", handle_request)
        
        try:
            await page.goto(hedef_url, timeout=30000)
            await asyncio.sleep(6)
        except Exception:
            pass
        finally:
            await browser.close()
            
        return yakalanan_link

def extract_stream_without_logs():
    kanal_urleri = [
        "https://beyazelma78.com/api/embed?u=UEsNIJ06uXbHrsROfQlACapvK5Da4ul3BxgoXvo9Kbc7uMHeMiqgdwbeGTR1j-TOl_YzU67mirvoPXvuA0wmvBFEo32ww1SZtVCCC42RFmj-bfw",
        "https://beyazelma78.com/api/embed?u=Pgooj3tsDLX31-TOP2HomNTqCovjmoIfDItvCFpV0c9t8W5sg0AWKB5aF2lsxzQAeuiZ-zdd_fnf96YdEtDM1_J24pfjMMS6BdpO9WjJoSTdJiE"
    ]
    
    async def run():
        tum_linkler = []
        for url in kanal_urleri:
            link = await tek_kanal_coz(url)
            if link:
                tum_linkler.append(link)
        
        if tum_linkler:
            with open("stream.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(tum_linkler) + "\n")

    asyncio.run(run())

if __name__ == "__main__":
    extract_stream_without_logs()
