"""add product_details table

Revision ID: 826b025a94fc
Revises: 073398b083fb
Create Date: 2022-08-24 13:24:18.730879

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, FLOAT, BIGINT, MEDIUMINT, TIMESTAMP

from alembic import op


# revision identifiers, used by Alembic.
revision = '826b025a94fc'
down_revision = '073398b083fb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product_details",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("url", VARCHAR(768), unique=True, nullable=False),
        Column("external_id", BIGINT(unsigned=True), nullable=True),
        Column("brand", VARCHAR(768), index=True, nullable=False),
        Column("model", VARCHAR(768), index=True, nullable=False),
        Column("category", VARCHAR(768), index=True, nullable=False),
        Column("name", VARCHAR(768), index=True, nullable=True),
        Column("images", TEXT(), nullable=True),
        Column("price", FLOAT(), index=True, nullable=True),
        Column("parameters", TEXT(), nullable=True),
        Column("description", TEXT(), nullable=True),
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
