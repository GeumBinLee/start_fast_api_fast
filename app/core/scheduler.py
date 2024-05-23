from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger


async def schedule_test():
    """
    스케줄러 테스트 함수입니다.
    """
    logger.debug("schedule_test")


def start():
    """
    스케줄러를 시작하고 예제 작업을 추가합니다.
    """
    scheduler = AsyncIOScheduler()
    # 스케줄 예제
    # scheduler.add_job(schedule_test, trigger="interval", seconds=60*60)  # 1시간 마다
    # scheduler.add_job(schedule_test, trigger="cron", hour=0, minute=0)  # 매일 0시 0분 마다
    scheduler.start()
