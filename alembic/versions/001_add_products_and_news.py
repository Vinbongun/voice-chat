"""Add products, product_prices, news tables

Revision ID: 001
Revises:
Create Date: 2026-03-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('brand', sa.String(255)),
        sa.Column('description', sa.Text),
        sa.Column('photo_url', sa.Text),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'product_prices',
        sa.Column('product_id', sa.String(255), sa.ForeignKey('products.id'), primary_key=True),
        sa.Column('branch_id', sa.String(100), primary_key=True),
        sa.Column('branch_name', sa.String(255)),
        sa.Column('price', sa.Numeric(10, 2)),
        sa.Column('qty', sa.Integer, default=0),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'news',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('published_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    # Full-text search index on news
    op.execute("""
        CREATE INDEX ix_news_fts ON news
        USING gin(to_tsvector('russian', title || ' ' || content))
    """)


def downgrade() -> None:
    op.drop_index('ix_news_fts', table_name='news')
    op.drop_table('news')
    op.drop_table('product_prices')
    op.drop_table('products')
