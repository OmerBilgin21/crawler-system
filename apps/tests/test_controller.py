from apps.controller.app import app
from apps.tests.utils import create_job, irs, irus, parse_data, remove_job

# ruff: noqa: ANN201, D103, S101, PLR2004, E731

client = app.test_client()


def test_get_pages():
	res = client.get("/crawler/pages")
	irs(res)

	data = parse_data(res)

	assert isinstance(data, list)

	for page in data:
		assert isinstance(page, str)


def test_instant_page():
	res = client.post("/crawler/instant/asdasd")
	irus(res)

	res = client.post("/crawler/instant/wirtschaft*boersenkurse*")
	irs(res)


def test_instant_overview():
	res = client.post("/crawler/instant")
	irs(res)


def test_increase_interval_by_one():
	url = "/job/increase"

	res = client.post(url)
	irs(res)

	remove_job()

	res = client.post(url)
	irus(res)

	create_job()


def test_decrease_interval_by_one():
	url = "/job/decrease"

	res = client.post(url)
	irs(res)

	remove_job()

	res = client.post(url)
	irus(res)

	create_job()


def test_reschedule_crawler():
	base = "/job/reschedule/"

	res = client.post(base + "asdasd")
	irus(res)

	res = client.post(base + "0")
	irus(res)

	remove_job()
	res = client.post(base + "3")
	irus(res)
	create_job()

	res = client.post(base + "3")
	irs(res)


def test_enable_crawler():
	url = "/job/enable"

	remove_job()
	res = client.post(url)
	irus(res)
	create_job()

	res = client.post(url)
	irs(res)


def test_disable_crawler():
	url = "/job/disable"

	remove_job()
	res = client.post(url)
	irus(res)
	create_job()

	res = client.post(url)
	irs(res)
