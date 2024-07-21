from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from apps.crawler import crawler

scheduler = BackgroundScheduler()
scheduler.start()

JOB_ID = "FUTURE_DEMAND"


def job() -> None:
	"""Job for APScheduler"""
	crawler(mode="all", page=None)


scheduler.add_job(
	job,
	trigger=IntervalTrigger(minutes=1),
	id=JOB_ID,
)


sj = lambda: scheduler.get_job(JOB_ID)  # noqa: E731


def crawler_runner(
	mode: str = "all",
	page: str | None = None,
) -> list[str] | bool:
	"""Crawler runner for instant crawls"""
	return crawler(mode=mode, page=page)


def get_job_interval() -> int | None:
	"""Returns job execution interval hours"""
	if sj():
		return int(sj().trigger.interval.total_seconds() / 3600)
	return None


def decrease_job_interval() -> int | None:
	"""Decreases the job execution interval hours by one"""
	old_interval = get_job_interval()
	if old_interval is not None:
		scheduler.reschedule_job(
			JOB_ID,
			trigger=IntervalTrigger(hours=old_interval - 1),
		)
		return old_interval - 1
	return None


def increase_job_interval() -> int | None:
	"""Increases the job execution interval hours by one"""
	old_interval = get_job_interval()
	if old_interval is not None:
		scheduler.reschedule_job(
			JOB_ID,
			trigger=IntervalTrigger(hours=old_interval + 1),
		)
		return old_interval + 1
	return None


def reschedule_job(hours: int) -> bool:
	"""Reschedules the running job if found"""
	if sj():
		scheduler.reschedule_job(
			JOB_ID,
			trigger=IntervalTrigger(hours=hours),
		)
		return True
	return False


def enable_job() -> bool:
	"""Resumes disabled job if found"""
	if sj():
		scheduler.resume_job(JOB_ID)
		return True
	return False


def disable_job() -> bool:
	"""Disables running job if found"""
	if sj():
		scheduler.pause_job(JOB_ID)
		return True
	return False
