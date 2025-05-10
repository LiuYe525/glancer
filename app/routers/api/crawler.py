from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.internal.crawlers import age as age_crawler
from app.internal.crawlers import bilibili as bilibili_crawler

router = APIRouter(prefix="/api/crawler")


@router.get("/age/daily-update-videos")
@cache(namespace="crawler/age", expire=60 * 60 * 24)
async def get_age_daily_update():
    result = await age_crawler.daily_update_videos()
    return result


@router.get("/bilibili/daily-popular")
@cache(namespace="crawler/bilibili", expire=60 * 30)
async def get_bilibili_daily_popular():
    result = await bilibili_crawler.popular()
    return result
