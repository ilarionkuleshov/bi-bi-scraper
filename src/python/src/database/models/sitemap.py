# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT

from .base import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin


class Sitemap(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "sitemaps"

    url = Column("url", VARCHAR(768), unique=True, nullable=False)
    exception = Column("exception", TEXT(), nullable=True)
