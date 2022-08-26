# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT

from .base import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin


class SerpPage(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "serp_pages"

    url = Column("url", VARCHAR(768), unique=True, nullable=False)
    brand = Column("brand", VARCHAR(768), index=True, nullable=False)
    model = Column("model", VARCHAR(768), index=True, nullable=False)
    category = Column("category", VARCHAR(768), index=True, nullable=False)
    subcategory = Column("subcategory", VARCHAR(768), index=True, nullable=True)
    exception = Column("exception", TEXT(), nullable=True)
