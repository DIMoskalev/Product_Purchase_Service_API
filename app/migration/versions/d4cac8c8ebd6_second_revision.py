"""second revision

Revision ID: d4cac8c8ebd6
Revises: d5faedb8242b
Create Date: 2024-10-04 00:25:29.201784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd4cac8c8ebd6'
down_revision: Union[str, None] = 'd5faedb8242b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cartitems')
    op.add_column('carts', sa.Column('product_id', sa.Integer(), nullable=False))
    op.add_column('carts', sa.Column('quantity', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'carts', 'products', ['product_id'], ['id'])
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.drop_column('carts', 'quantity')
    op.drop_column('carts', 'product_id')
    op.create_table('cartitems',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('cart_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], name='cartitems_cart_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='cartitems_product_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='cartitems_pkey')
    )
    # ### end Alembic commands ###
