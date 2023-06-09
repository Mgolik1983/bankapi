"""create user table

Revision ID: a1251dc97d21
Revises: ef3f61977dbc
Create Date: 2023-03-15 14:28:48.159889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1251dc97d21'
down_revision = 'ef3f61977dbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.VARCHAR(length=128), nullable=False))
    op.add_column('post', sa.Column('body', sa.TEXT(), nullable=False))
    op.add_column('post', sa.Column('date_created', sa.TIMESTAMP(), nullable=True))
    op.create_unique_constraint(None, 'post', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='unique')
    op.drop_column('post', 'date_created')
    op.drop_column('post', 'body')
    op.drop_column('post', 'title')
    # ### end Alembic commands ###
