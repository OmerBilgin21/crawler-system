from apps.scheduler.scheduler import (
	decrease_job_interval,
	disable_job,
	enable_job,
	get_job_interval,
	increase_job_interval,
)
from apps.tests.utils import create_job, remove_job, reset_hours

# ruff: noqa: ANN201, D103, S101, PLR2004


def test_increase_job_interval():
	reset_hours()
	res = increase_job_interval()
	assert isinstance(res, int)
	assert res == 2


def test_decrease_job_interval():
	reset_hours()
	increase_job_interval()
	res = decrease_job_interval()
	assert isinstance(res, int)
	assert res == 1


def test_disable_job():
	res = disable_job()
	assert res is True

	remove_job()

	res = disable_job()
	assert res is False

	create_job()


def test_enable_job():
	res = enable_job()
	assert res is True

	remove_job()

	res = enable_job()
	assert res is False

	create_job()


def test_get_job_interval():
	res = get_job_interval()
	assert isinstance(res, int)

	remove_job()

	res = get_job_interval()
	assert res is None

	create_job()
