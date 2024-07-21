import pytest

from apps.crawler import crawler

# ruff: noqa: ANN201, D103, S101


def test_crawler():
	with pytest.raises(TypeError):
		crawler()

	res = crawler(mode="asdasd")
	assert res is False

	res = crawler(mode="single", page=None)
	assert res is False

	res = crawler(mode="single", page="asdasd")
	assert res is False

	res = crawler(mode="return-pages")
	assert isinstance(res, list)
	for page in res:
		assert isinstance(page, str)

	res = crawler(mode="single", page="wirtschaft*boersenkurse*")
	assert res is True

	res = crawler(mode="all")
	assert res is True
