"""empty message

Revision ID: 59e7d13c9a88
Revises: 6d1369edb6de
Create Date: 2022-10-09 04:27:03.388574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils.types.json

# revision identifiers, used by Alembic.
revision = "59e7d13c9a88"
down_revision = "6d1369edb6de"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "received_events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("value", sqlalchemy_utils.types.json.JSONType(), nullable=True),
        sa.Column("treated", sa.Boolean(), nullable=True),
        sa.Column("treated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_received_events_id"), "received_events", ["id"], unique=False
    )
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("password", postgresql.BYTEA(), autoincrement=False, nullable=True),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("email_validated", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.drop_index(op.f("ix_received_events_id"), table_name="received_events")
    op.drop_table("received_events")
    # ### end Alembic commands ###