import asyncio
from typing import List

from playwright.async_api import async_playwright
from dataclasses import dataclass


@dataclass
class AgeVideo:
    title: str
    href: str
    cover: str
    section: str


@dataclass
class AgeDailyUpdateVideos:
    date: str
    videos: List[AgeVideo]


async def daily_update_videos():
    result: List[AgeDailyUpdateVideos] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.agefans.la/update", wait_until="networkidle")
        elements = await page.query_selector_all("#recent_update_video_wrapper > div")
        for element in elements:
            date = await element.query_selector("div.position-relative.my-4 > button")
            daily_videos: AgeDailyUpdateVideos = AgeDailyUpdateVideos(
                date=await date.text_content(), videos=[]
            )
            videos = await element.query_selector_all(
                "div.video_list_box--bd > div > div > div"
            )
            for video in videos:
                img = await video.query_selector(
                    "div.video_item--image.position-relative > img"
                )
                section = await video.query_selector(
                    "div.video_item--image.position-relative > span"
                )
                title = await video.query_selector(
                    "div.video_item-title.text-truncate.text-center.py-2 > a"
                )
                daily_videos.videos.append(
                    AgeVideo(
                        title=await title.text_content(),
                        href=await title.get_attribute("href"),
                        cover=await img.get_attribute("src"),
                        section=await section.text_content(),
                    )
                )
            result.append(daily_videos)
    return result


if __name__ == "__main__":
    print(asyncio.run(daily_update_videos()))
