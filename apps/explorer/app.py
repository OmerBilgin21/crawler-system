from flask import Flask

from apps import db_connection_str
from apps.models.models import Article, ArticleVersion, db
from apps.models.serializers import ArticleSchema, ArticleVersionSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = db_connection_str
db.init_app(app)


with app.app_context():
	db.create_all()


@app.get("/articles")
def get_articles() -> list[ArticleSchema]:
	"""Get a list of articles

	Returns:
		ArticleSchema: _description_
	"""
	articles = Article.query.all()
	return ArticleSchema(many=True, context={"with_versions": False}).dump(articles)


@app.get("/articles-with-versions")
def get_articles_with_versions() -> list[ArticleSchema]:
	"""Get a list of articles with versions

	Returns:
		ArticleSchema: _description_
	"""
	articles = Article.query.all()
	return ArticleSchema(many=True, context={"with_versions": True}).dump(articles)


@app.get("/articles/<keyword>")
def search_in_articles(keyword: str) -> list[ArticleSchema]:
	"""Get a list of articles that contains a keyword

	Args:
		keyword (str): keyword to search for

	Returns:
		ArticleSchema: _description_
	"""
	# Conduct a search among the texts, sub_headlines and headlines of all articles
	articles = Article.query.filter(
		Article.full_text.ilike(f"%{keyword}%"),
		Article.headline.ilike(f"%{keyword}%"),
		Article.sub_headline.ilike(f"%{keyword}%"),
	).all()
	return ArticleSchema(many=True, context={"with_versions": False}).dump(articles)


@app.get("/article/<id_>/versions")
def get_article_versions(id_: str) -> list[ArticleVersionSchema]:
	"""Get all the different versions of an article

	Args:
		id_ (str): Article to check

	Returns:
		bool: State of changed
	"""
	versions = ArticleVersion.query.filter_by(article_id=id_).all()
	return ArticleVersionSchema(many=True).dump(versions)
