"""add serp_pages table

Revision ID: 073398b083fb
Revises: 1fbd664440eb
Create Date: 2022-08-23 22:07:30.949335

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, MEDIUMINT, BIGINT, TIMESTAMP, TEXT

from alembic import op


# revision identifiers, used by Alembic.
revision = '073398b083fb'
down_revision = '1fbd664440eb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "serp_pages",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("url", VARCHAR(768), unique=True, nullable=False),
        Column("brand", VARCHAR(768), index=True, nullable=False),
        Column("model", VARCHAR(768), index=True, nullable=False),
        Column("category", VARCHAR(768), index=True, nullable=False),
        Column("exception", TEXT(), nullable=True),
        Column("status", MEDIUMINT(unsigned=True), index=True, server_default=text("0"), nullable=False),
        Column("created_at", TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", TIMESTAMP, nullable=False, index=True, unique=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        )
    )


def downgrade():
    op.drop_table("serp_pages")
