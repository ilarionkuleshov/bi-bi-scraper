"""add serp_pages table

Revision ID: af558af826bb
Revises: 33e368300f47
Create Date: 2022-08-26 13:16:07.774953

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, VARCHAR, TEXT, MEDIUMINT

from alembic import op



# revision identifiers, used by Alembic.
revision = 'af558af826bb'
down_revision = '33e368300f47'
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
        Column("subcategory", VARCHAR(768), index=True, nullable=True),
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
