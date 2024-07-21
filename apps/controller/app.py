from flask import Flask, Response

from apps.scheduler.scheduler import (
	crawler_runner,
	decrease_job_interval,
	disable_job,
	enable_job,
	increase_job_interval,
	reschedule_job,
)

app = Flask(__name__)


@app.get("/crawler/pages")
def get_pages() -> list[str]:
	"""Get a list of pages.

	Returns:
		Response: Response status and message
	"""
	return crawler_runner(mode="return-pages")


@app.post("/crawler/instant/<page>")
def instant_page(page: str) -> Response:
	"""Crawl a page.

	Returns:
		Response: Response status and message
	"""
	res = crawler_runner(mode="single", page=page)
	if res is False:
		return Response(status=400, response="Page not found!")
	return Response(status=200, response=f"{page.replace('*','/')} crawled!")


@app.post("/crawler/instant")
def instant_overview() -> Response:
	"""Crawl overview page.

	Returns:
		Response: Response status and message
	"""
	crawler_runner(mode="overview")
	return Response(status=200, response="Overview crawled!")


@app.post("/job/increase")
def increase_interval_by_one() -> Response:
	"""Increases the interval of job execution by one hour

	Returns:
		Response: Response status and message
	"""
	res = increase_job_interval()
	if res is None:
		return Response(response="Job not found!", status=400)

	return Response(
		response=f"Execution interval is increased by one, \
		new interval is {res} hours.",
		status=200,
	)


@app.post("/job/decrease")
def decrease_interval_by_one() -> Response:
	"""Decreases the interval of job execution by one hour

	Returns:
		Response: Response status and message
	"""
	res = decrease_job_interval()
	if res is None:
		return Response(response="Job not found!", status=400)

	return Response(
		response=f"Execution interval is decreased by one, \
		new interval is {res} hours.",
		status=200,
	)


@app.post("/job/reschedule/<hour>")
def reschedule_crawler(hour: str) -> Response:
	"""Reschedules the crawler job if found

	Args:
		hour (float): Hour to reschedule

	Returns:
		Response: Response status and message
	"""
	try:
		hour = int(hour)
	except ValueError:
		return Response(
			response=f'Hour can not be "{hour}", it must be an integer!',
			status=400,
		)

	if hour == 0:
		return Response(
			response="Interval hour can not be set to 0. \
			To disable the jobs, please use /job/disable endpoint!",
			status=400,
		)

	res = reschedule_job(hours=hour)
	if res is False:
		return Response(response="Job not found!", status=400)

	return Response(
		response=f"Execution interval has been modified to {hour} hours",
		status=200,
	)


@app.post("/job/enable")
def enable_crawler() -> Response:
	"""Enables crawler job if found

	Returns:
		Response: Response status and message
	"""
	res = enable_job()
	if res is False:
		return Response(response="Job not found!", status=400)
	return Response(response="Job has been enabled!", status=200)


@app.post("/job/disable")
def disable_crawler() -> Response:
	"""Disables crawler job if found

	Returns:
		Response: Response status and message
	"""
	res = disable_job()
	if res is False:
		return Response(status=400, response="Job not found!")
	return Response(status=200, response="Job has been disabled!")
