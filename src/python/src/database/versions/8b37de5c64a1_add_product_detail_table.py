"""add product_detail table

Revision ID: 8b37de5c64a1
Revises: af558af826bb
Create Date: 2022-08-26 13:20:58.310410

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, VARCHAR, TEXT, MEDIUMINT, FLOAT

from alembic import op



# revision identifiers, used by Alembic.
revision = '8b37de5c64a1'
down_revision = 'af558af826bb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product_details",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("url", VARCHAR(768), unique=True, nullable=False),
        Column("external_id", BIGINT(unsigned=True), nullable=False),
        Column("brand", VARCHAR(768), index=True, nullable=False),
        Column("model", VARCHAR(768), index=True, nullable=False),
        Column("category", VARCHAR(768), index=True, nullable=False),
        Column("subcategory", VARCHAR(768), index=True, nullable=True),
        Column("name", VARCHAR(768), index=True, nullable=True),
        Column("first_image", TEXT(), nullable=True),
        Column("images", TEXT(), nullable=True),
        Column("price", FLOAT(), index=True, nullable=True),
        Column("parameters", TEXT(), nullable=True),
        Column("description", TEXT(), nullable=True),
        Column("original_number", VARCHAR(768), nullable=True),
        Column("substitute_number", VARCHAR(768), nullable=True),
        Column("condition", VARCHAR(768), index=True, nullable=True),
        Column("amount", BIGINT(unsigned=True), nullable=True),
        Column("manufacturer", VARCHAR(768), index=True, nullable=True),
        Column("exception", TEXT(), nullable=True),
        Column("status", MEDIUMINT(unsigned=True), index=True, server_default=text("0"), nullable=False),
        Column("created_at", TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", TIMESTAMP, nullable=False, index=True, unique=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        )
    )


def downgrade():
    op.drop_table("product_details")
