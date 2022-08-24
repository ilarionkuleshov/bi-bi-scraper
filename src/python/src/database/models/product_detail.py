# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, FLOAT, BIGINT

from .base import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin


class ProductDetail(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "product_details"

    url = Column("url", VARCHAR(768), unique=True, nullable=False)
    external_id = Column("external_id", BIGINT(unsigned=True), nullable=True)
    brand = Column("brand", VARCHAR(768), index=True, nullable=False)
    model = Column("model", VARCHAR(768), index=True, nullable=False)
    category = Column("category", VARCHAR(768), index=True, nullable=False)
    name = Column("name", VARCHAR(768), index=True, nullable=True)
    images = Column("images", TEXT(), nullable=True)
    price = Column("price", FLOAT(), index=True, nullable=True)
    parameters = Column("parameters", TEXT(), nullable=True)
    description = Column("description", TEXT(), nullable=True)
    exception = Column("exception", TEXT(), nullable=True)
