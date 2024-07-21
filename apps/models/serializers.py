from marshmallow import fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .models import Article, ArticleVersion

# ruff: noqa: D106, FBT001, ARG002


class ArticleVersionSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = ArticleVersion
		include_fk = True


class ArticleSchema(SQLAlchemyAutoSchema):
	versions = fields.Nested(ArticleVersionSchema, many=True)
	version_count = fields.Method("get_version_count", dump_only=True)

	class Meta:
		model = Article

	def get_version_count(self, data: Article) -> float:
		"""Get the count of versions"""
		return len(data.versions)

	@post_dump
	def remove_versions(
		self,
		data: Article | list[Article],
		many: bool,
		**kwargs: dict,
	) -> dict:
		"""Optionally remove versions from articles"""
		with_versions = self.context.get("with_versions", True)

		if with_versions is False:
			data.pop("versions")

		return data
