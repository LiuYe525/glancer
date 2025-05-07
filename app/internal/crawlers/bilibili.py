from playwright.sync_api import sync_playwright


def popular():
    result = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.bilibili.com/v/popular/all")
        page.wait_for_load_state("networkidle")
        videos = page.query_selector_all(
            "#app > div > div.popular-video-container.popular-list > div.flow-loader > ul > div"
        )
        for video in videos:
            cover = video.query_selector("div.video-card__content > a > img")
            info = video.query_selector("div.video-card__info")
            title = info.query_selector("p")
            creator = info.query_selector("div > span.up-name > span")
            play_times = info.query_selector("div > p > span.play-text")
            comment_times = info.query_selector("div > p > span.like-text")
            result.append(
                {
                    "cover": "https:" + cover.get_attribute("src").strip(),
                    "title": title.text_content().strip(),
                    "creator": creator.text_content().strip(),
                    "play_times": play_times.text_content().strip(),
                    "comment_times": comment_times.text_content().strip(),
                }
            )
    return result


if __name__ == "__main__":
    print(popular())
