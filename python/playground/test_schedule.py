import asyncio
import datetime
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def turn_off_moment():
    print("Schedule task was ran ")


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    #scheduler.add_job(turn_off_moment, 'interval', seconds=10) #  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10))\
    scheduler.add_job(turn_off_moment, next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=5))
    scheduler.start()
    asyncio.get_event_loop().run_forever()

