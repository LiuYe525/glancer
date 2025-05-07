from playwright.sync_api import sync_playwright


def daily_update_videos():
    result = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.agefans.la/update")
        page.wait_for_load_state("networkidle")
        elements = page.query_selector_all("#recent_update_video_wrapper > div")
        for element in elements:
            date = element.query_selector("div.position-relative.my-4 > button")
            daily_videos = {"date": date.text_content(), "videos": []}
            videos = element.query_selector_all(
                "div.video_list_box--bd > div > div > div"
            )
            for video in videos:
                img = video.query_selector(
                    "div.video_item--image.position-relative > img"
                )
                section = video.query_selector(
                    "div.video_item--image.position-relative > span"
                )
                title = video.query_selector(
                    "div.video_item-title.text-truncate.text-center.py-2 > a"
                )
                daily_videos["videos"].append(
                    {
                        "title": title.text_content(),
                        "href": title.get_attribute("href"),
                        "cover": img.get_attribute("src"),
                        "section": section.text_content(),
                    }
                )
            result.append(daily_videos)
    return result


if __name__ == "__main__":
    print(daily_update_videos())
