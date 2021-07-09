"""Make email_confirmed not nullable

Revision ID: 8ddb55ebf927
Revises: 9dcfaaf830fc
Create Date: 2021-01-26 00:38:48.495926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ddb55ebf927'
down_revision = '9dcfaaf830fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email_confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email_confirmed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
