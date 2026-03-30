import datetime
from typing import Dict


class ScheduleService:
    @staticmethod
    def within_working_hours(timestamp: datetime.datetime = None) -> bool:
        timestamp = timestamp or datetime.datetime.now()
        return 9 <= timestamp.hour < 18

    @staticmethod
    def next_execution_window() -> Dict[str, str]:
        now = datetime.datetime.now()
        if ScheduleService.within_working_hours(now):
            return {"next_run": now.isoformat()}
        start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now.hour >= 18:
            start += datetime.timedelta(days=1)
        return {"next_run": start.isoformat()}
