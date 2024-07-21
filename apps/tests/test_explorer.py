import os
from datetime import datetime, timezone

from apps.explorer.app import app, db
from apps.models import Article, ArticleSchema, ArticleVersion, ArticleVersionSchema
from apps.tests.utils import irs, parse_data

# ruff: noqa: ANN201, D103, S101, PLR2004, E731, PTH107, PTH109, PTH110, PTH118

client = app.test_client()

# Correctly constructing the database URI
db_path = os.path.join(os.getcwd(), "mock.sqlite")
db_uri = f"sqlite:///{db_path}"

# Configure the app to use the test database URI
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

with app.app_context():
	db.drop_all()
	db.create_all()

	session = db.session

	headline = "headline fake"
	sub_headline = "sub_headline fake"
	full_text = "full_text fake"
	url = "link fake"
	now = datetime.now(tz=timezone.utc)

	article = Article(
		headline=headline,
		sub_headline=sub_headline,
		full_text=full_text,
		url=url,
		last_update=now,
	)

	session.add(article)
	session.flush()
	for i in range(3):
		article_version = ArticleVersion(
			article_id=article.id,
			version=i + 1,
			headline=headline + str(i),
			sub_headline=sub_headline,
			full_text=full_text,
			last_update=now,
		)

		session.add(article_version)
	session.commit()


def test_get_articles():
	res = client.get("/articles")
	irs(res)
	data = parse_data(res)

	assert isinstance(data, list)
	schema = ArticleSchema(many=False, context={"with_versions": False})
	with app.app_context():
		for d in data:
			d.pop("version_count")
			assert schema.load(d, session=db.session)


def test_get_articles_with_versions():
	res = client.get("/articles-with-versions")
	irs(res)
	data = parse_data(res)

	assert isinstance(data, list)
	schema = ArticleSchema(many=False, context={"with_versions": True})
	with app.app_context():
		for d in data:
			d.pop("version_count")
			assert schema.load(d, session=db.session)


def test_search_in_articles():
	res = client.get("/articles/die")
	irs(res)
	data = parse_data(res)

	assert isinstance(data, list)
	schema = ArticleSchema(many=False, context={"with_versions": True})
	with app.app_context():
		for d in data:
			d.pop("version_count")
			assert schema.load(d, session=db.session)


def test_get_article_versions():
	res = client.get("/article/1/versions")
	irs(res)
	data = parse_data(res)

	assert isinstance(data, list)
	schema = ArticleVersionSchema(many=False)
	with app.app_context():
		for d in data:
			assert schema.load(d, session=db.session)
