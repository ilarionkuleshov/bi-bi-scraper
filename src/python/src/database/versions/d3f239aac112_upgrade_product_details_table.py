"""upgrade product_details table

Revision ID: d3f239aac112
Revises: 826b025a94fc
Create Date: 2022-08-25 19:41:32.845047

"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from alembic import op


# revision identifiers, used by Alembic.
revision = 'd3f239aac112'
down_revision = '826b025a94fc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("product_details", Column("original_number", VARCHAR(768), nullable=True))
    op.add_column("product_details", Column("condition", VARCHAR(768), index=True, nullable=True))
    op.add_column("product_details", Column("amount", BIGINT(unsigned=True), nullable=True))
    op.add_column("product_details", Column("manufacturer", VARCHAR(768), index=True, nullable=True))


def downgrade():
    op.drop_column("product_details", "original_number")
    op.drop_column("product_details", "condition")
    op.drop_column("product_details", "amount")
    op.drop_column("product_details", "manufacturer")
