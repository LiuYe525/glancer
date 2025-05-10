import asyncio

from playwright.async_api import async_playwright


async def popular():
    result = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(
            "https://www.bilibili.com/v/popular/all", wait_until="networkidle"
        )
        videos = await page.query_selector_all(
            "#app > div > div.popular-video-container.popular-list > div.flow-loader > ul > div"
        )
        for video in videos:
            cover = await video.query_selector("div.video-card__content > a > img")
            info = await video.query_selector("div.video-card__info")
            title = await info.query_selector("p")
            creator = await info.query_selector("div > span.up-name > span")
            play_times = await info.query_selector("div > p > span.play-text")
            comment_times = await info.query_selector("div > p > span.like-text")
            result.append(
                {
                    "cover": "https:" + (await cover.get_attribute("src")).strip(),
                    "title": (await title.text_content()).strip(),
                    "creator": (await creator.text_content()).strip(),
                    "play_times": (await play_times.text_content()).strip(),
                    "comment_times": (await comment_times.text_content()).strip(),
                }
            )
    return result


if __name__ == "__main__":
    print(asyncio.run(popular()))
