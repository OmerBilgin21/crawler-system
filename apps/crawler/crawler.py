import time
from datetime import datetime, timezone
from urllib import robotparser

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps import db_connection_str
from apps.models import Article, ArticleVersion, db

engine = create_engine(db_connection_str)
Session = sessionmaker(bind=engine)
session = Session()
db.metadata.create_all(bind=engine)

URL = "https://www.tagesschau.de/"
NO_HEADLINE = "No headline found"
NO_SUB_HEADLINE = "No sub headline found"
ALLOWED_MODES = ("overview", "all", "return-pages", "single")


def is_crawl_allowed(url: str, user_agent: str = "*") -> bool:
	"""Check if tagesschau allows crawling for given page."""
	rp = robotparser.RobotFileParser()
	rp.set_url(url + "/robots.txt")
	rp.read()
	return rp.can_fetch(user_agent, url)


def get_preferred_delay(url: str, user_agent: str = "*") -> float | None:
	"""Get the preferred delay amount if specified

	Args:
		url (str): url of page
		user_agent (str, optional): User agent
			Defaults to "*"

	Returns:
		float | None: Amount of seconds to delay if specified
	"""
	rp = robotparser.RobotFileParser()
	rp.set_url(url + "/robots.txt")
	rp.read()
	return rp.crawl_delay(user_agent)


def includes_string(search_str: str) -> bool:
	"""Returns a function that checks if the given string is in a class."""

	def check_class(cls: str) -> bool:
		return cls is not None and search_str in cls

	return check_class


def insert_to_db(link: str, headline: str, sub_headline: str, full_text: str) -> None:
	"""Inserts crawled information to db"""
	# As far as I saw, there are no exceptions on the news pages
	# They all have headlines, toplines and some explanatory text
	# If they're absent, likely that's a page we do not want to keep as news
	if headline == NO_HEADLINE or sub_headline == NO_SUB_HEADLINE or full_text == " ":
		return

	last_update = datetime.now(tz=timezone.utc)

	article = session.query(Article).filter_by(url=link).first()
	if article:
		if (
			article.headline != headline
			or article.sub_headline != sub_headline
			or article.full_text != full_text
		):
			version = (
				session.query(ArticleVersion).filter_by(article_id=article.id).count()
			)

			print(
				"Changes detected for: ",
				link,
				f"\nNew version ({version + 1}) is inserted.",
			)

			new_version = ArticleVersion(
				article_id=article.id,
				version=version + 1,
				headline=headline,
				sub_headline=sub_headline,
				full_text=full_text,
				last_update=last_update,
			)
			session.add(new_version)

			# Keep the most recent version as the Article
			article.headline = headline
			article.sub_headline = sub_headline
			article.full_text = full_text
			article.last_update = last_update

		else:
			print("Page hasn't changed: ", link)
	else:
		article = Article(
			url=link,
			headline=headline,
			sub_headline=sub_headline,
			full_text=full_text,
			last_update=last_update,
		)

		session.add(article)
		session.flush()

		article_version = ArticleVersion(
			article_id=article.id,
			version=1,
			headline=headline,
			sub_headline=sub_headline,
			full_text=full_text,
			last_update=last_update,
		)
		session.add(article_version)

	session.commit()


def crawl_data(link: str) -> None:
	"""__"""
	res = requests.get(url=link, timeout=10000)
	soup = BeautifulSoup(
		res.content,
		"html.parser",
	)

	# at tagesschau, they always use headline or topline as the class if there are any
	headline_elements = soup.find_all(class_=includes_string("headline"))
	sub_headline_elements = soup.find_all(class_=includes_string("topline"))

	headline = (
		headline_elements[0].get_text().strip()
		if len(headline_elements) > 0
		else NO_HEADLINE
	)
	sub_headline = (
		sub_headline_elements[0].get_text().strip()
		if len(sub_headline_elements) > 0
		else NO_SUB_HEADLINE
	)
	# all p tags
	full_text = " ".join(
		[p.text.strip() for p in soup.find_all("p") if isinstance(p.text, str)],
	)

	insert_to_db(
		link=link,
		headline=headline,
		sub_headline=sub_headline,
		full_text=full_text,
	)


def crawler(mode: str, page: str | None = None) -> list[str] | bool:
	"""__"""
	response = requests.get(url=URL, timeout=10000)
	soup = BeautifulSoup(response.content, "html.parser")

	if mode not in ALLOWED_MODES:
		return False

	returnable_urls = lambda: [  # noqa: E731
		a["href"].replace(URL, "").replace("/", "*")
		for a in soup.find_all("a", href=True)
		if URL in a["href"]
	]

	if mode == "overview":
		links = [URL]
	elif mode == "all":
		links = [a["href"] for a in soup.find_all("a", href=True) if URL in a["href"]]
		links.insert(0, URL)
	elif mode == "return-pages":
		return returnable_urls()
	elif mode == "single" and isinstance(page, str) and page in returnable_urls():
		links = [f"{URL}{page.replace('*', '/')}"]
	else:
		return False

	for link in links:
		if is_crawl_allowed(url=link) is False:
			continue

		# to be respectful, won't bombard their servers
		delay = get_preferred_delay(url=link)
		time.sleep(delay if delay else 1)
		print("Crawling:", link)
		crawl_data(link=link)

	return True
