"""empty message

Revision ID: 647e21559128
Revises: abe42cc715f5
Create Date: 2018-06-27 20:20:58.479913

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '647e21559128'
down_revision = 'abe42cc715f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cm_user',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=225), nullable=False),
    sa.Column('nike_name', sa.String(length=20), nullable=True),
    sa.Column('invitation_code', sa.String(length=20), nullable=False),
    sa.Column('app_key', sa.String(length=225), nullable=False),
    sa.PrimaryKeyConstraint('u_id'),
    sa.UniqueConstraint('app_key'),
    sa.UniqueConstraint('nike_name'),
    sa.UniqueConstraint('u_id'),
    sa.UniqueConstraint('username')
    )
    op.drop_index('app_key', table_name='cm_users')
    op.drop_index('nike_name', table_name='cm_users')
    op.drop_index('u_id', table_name='cm_users')
    op.drop_index('username', table_name='cm_users')
    op.drop_table('cm_users')
    op.add_column('cm_cookie', sa.Column('u_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cm_cookie', 'cm_user', ['u_id'], ['u_id'])
    op.create_unique_constraint(None, 'cm_website', ['web_site_host'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cm_website', type_='unique')
    op.drop_constraint(None, 'cm_cookie', type_='foreignkey')
    op.drop_column('cm_cookie', 'u_id')
    op.create_table('cm_users',
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('update_time', mysql.DATETIME(), nullable=True),
    sa.Column('u_id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(collation='utf8_bin', length=20), nullable=True),
    sa.Column('password', mysql.VARCHAR(collation='utf8_bin', length=225), nullable=False),
    sa.Column('nike_name', mysql.VARCHAR(collation='utf8_bin', length=20), nullable=True),
    sa.Column('app_key', mysql.VARCHAR(collation='utf8_bin', length=225), nullable=False),
    sa.Column('invitation_code', mysql.VARCHAR(collation='utf8_bin', length=20), nullable=False),
    sa.PrimaryKeyConstraint('u_id'),
    mysql_collate='utf8_bin',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'cm_users', ['username'], unique=True)
    op.create_index('u_id', 'cm_users', ['u_id'], unique=True)
    op.create_index('nike_name', 'cm_users', ['nike_name'], unique=True)
    op.create_index('app_key', 'cm_users', ['app_key'], unique=True)
    op.drop_table('cm_user')
    # ### end Alembic commands ###
