import pytest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.scheduler import schedule_test, start


def test_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(schedule_test, "interval", seconds=1)
    scheduler.start()
    assert scheduler.running
    scheduler.shutdown()
