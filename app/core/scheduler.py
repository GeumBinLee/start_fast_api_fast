from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger


async def schedule_test():
    logger.debug("schedule_test")


def start():
    scheduler = AsyncIOScheduler()
    # 스케줄 예제
    # scheduler.add_job(schedule_test, trigger="interval", seconds=60*60)  # 1시간 마다
    # scheduler.add_job(schedule_test, trigger="cron", hour=0, minute=0)  # 매일 0시 0분 마다
    scheduler.start()
