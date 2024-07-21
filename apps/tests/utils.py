import json

from flask import Response

from apps.scheduler.scheduler import (
	JOB_ID,
	IntervalTrigger,
	job,
	reschedule_job,
	scheduler,
)

# ruff: noqa: D103, S101, PLR2004


def reset_hours() -> None:
	reschedule_job(hours=1)


def remove_job() -> None:
	scheduler.remove_all_jobs()


def create_job() -> None:
	scheduler.add_job(
		job,
		trigger=IntervalTrigger(hours=1),
		id=JOB_ID,
	)


def irs(res: Response) -> None:
	assert isinstance(res, Response)
	assert res.status_code == 200


def irus(res: Response) -> None:
	assert isinstance(res, Response)
	assert res.status_code == 400


def parse_data(res: Response) -> None:
	data = res.data.decode("utf-8")
	return json.loads(data)
