"""empty message

Revision ID: 54630c5d30f1
Revises: 0cacc17e0fc3
Create Date: 2022-10-10 01:58:37.210467

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "54630c5d30f1"
down_revision = "0cacc17e0fc3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "uuid")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("uuid", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
