"""add sent_to_customer field

Revision ID: 4e0702bba5e3
Revises: 8b37de5c64a1
Create Date: 2022-08-29 16:39:12.169122

"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import DATE

from alembic import op



# revision identifiers, used by Alembic.
revision = '4e0702bba5e3'
down_revision = '8b37de5c64a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("product_details", Column("sent_to_customer", DATE(), default=None, nullable=True))


def downgrade():
    op.drop_column("product_details", "sent_to_customer")
