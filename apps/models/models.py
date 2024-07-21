from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, relationship

db = SQLAlchemy()


class Article(db.Model):
	__tablename__ = "articles"
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String, unique=True, nullable=False)
	headline = db.Column(db.String, nullable=False)
	sub_headline = db.Column(db.String, nullable=True)
	full_text = db.Column(db.Text, nullable=False)
	last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	versions = relationship("ArticleVersion", back_populates="article")


class ArticleVersion(db.Model):
	__tablename__ = "article_versions"
	id = db.Column(db.Integer, primary_key=True)
	article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
	version = db.Column(db.Integer, nullable=False)
	headline = db.Column(db.String, nullable=False)
	sub_headline = db.Column(db.String, nullable=True)
	full_text = db.Column(db.Text, nullable=False)
	last_update = db.Column(db.DateTime, nullable=False)
	crawled_at = db.Column(db.DateTime, default=datetime.utcnow)
	article = relationship("Article", back_populates="versions")


Base = declarative_base()
