"""add sitemaps table

Revision ID: 33e368300f47
Revises: 
Create Date: 2022-08-26 13:13:21.652884

"""
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, VARCHAR, TEXT, MEDIUMINT

from alembic import op



# revision identifiers, used by Alembic.
revision = '33e368300f47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sitemaps",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("url", VARCHAR(768), unique=True, nullable=False),
        Column("exception", TEXT(), nullable=True),
        Column("status", MEDIUMINT(unsigned=True), index=True, server_default=text("0"), nullable=False),
        Column("created_at", TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", TIMESTAMP, nullable=False, index=True, unique=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        )
    )


def downgrade():
    op.drop_table("sitemaps")
