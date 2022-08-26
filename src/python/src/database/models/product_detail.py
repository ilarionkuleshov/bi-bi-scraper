# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, FLOAT, BIGINT

from .base import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin


class ProductDetail(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "product_details"

    url = Column("url", VARCHAR(768), unique=True, nullable=False)
    external_id = Column("external_id", BIGINT(unsigned=True), nullable=False)
    brand = Column("brand", VARCHAR(768), index=True, nullable=False)
    model = Column("model", VARCHAR(768), index=True, nullable=False)
    category = Column("category", VARCHAR(768), index=True, nullable=False)
    subcategory = Column("subcategory", VARCHAR(768), index=True, nullable=True)
    name = Column("name", VARCHAR(768), index=True, nullable=True)
    first_image = Column("first_image", TEXT(), nullable=True)
    images = Column("images", TEXT(), nullable=True)
    price = Column("price", FLOAT(), index=True, nullable=True)
    parameters = Column("parameters", TEXT(), nullable=True)
    description = Column("description", TEXT(), nullable=True)
    original_number = Column("original_number", VARCHAR(768), nullable=True)
    substitute_number = Column("substitute_number", VARCHAR(768), nullable=True)
    condition = Column("condition", VARCHAR(768), index=True, nullable=True)
    amount = Column("amount", BIGINT(unsigned=True), nullable=True)
    manufacturer = Column("manufacturer", VARCHAR(768), index=True, nullable=True)
    exception = Column("exception", TEXT(), nullable=True)
