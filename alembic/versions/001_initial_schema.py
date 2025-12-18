"""Initial schema: articles, crawl_logs, sources

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-12-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sources table
    op.create_table(
        'source',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('rate_limit', sa.Integer(), nullable=False),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('timeout', sa.Integer(), nullable=False),
        sa.Column('selectors', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('rss_url', sa.String(length=500), nullable=True),
        sa.Column('sitemap_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_source_name'), 'source', ['name'], unique=True)
    op.create_index(op.f('ix_source_enabled'), 'source', ['enabled'], unique=False)

    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('source_name', sa.String(length=100), nullable=False),
        sa.Column('author', sa.String(length=200), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('crawled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('image_url', sa.String(length=1000), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_url'), 'articles', ['url'], unique=True)
    op.create_index(op.f('ix_articles_title'), 'articles', ['title'], unique=False)
    op.create_index(op.f('ix_articles_source_name'), 'articles', ['source_name'], unique=False)
    op.create_index(op.f('ix_articles_published_at'), 'articles', ['published_at'], unique=False)
    op.create_index(op.f('ix_articles_category'), 'articles', ['category'], unique=False)
    op.create_index(op.f('ix_articles_status'), 'articles', ['status'], unique=False)

    # Create crawl_logs table
    op.create_table(
        'crawl_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_name', sa.String(length=100), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('articles_found', sa.Integer(), nullable=False),
        sa.Column('articles_new', sa.Integer(), nullable=False),
        sa.Column('articles_updated', sa.Integer(), nullable=False),
        sa.Column('errors', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('error_details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawl_logs_source_name'), 'crawl_logs', ['source_name'], unique=False)
    op.create_index(op.f('ix_crawl_logs_status'), 'crawl_logs', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_crawl_logs_status'), table_name='crawl_logs')
    op.drop_index(op.f('ix_crawl_logs_source_name'), table_name='crawl_logs')
    op.drop_table('crawl_logs')
    
    op.drop_index(op.f('ix_articles_status'), table_name='articles')
    op.drop_index(op.f('ix_articles_category'), table_name='articles')
    op.drop_index(op.f('ix_articles_published_at'), table_name='articles')
    op.drop_index(op.f('ix_articles_source_name'), table_name='articles')
    op.drop_index(op.f('ix_articles_title'), table_name='articles')
    op.drop_index(op.f('ix_articles_url'), table_name='articles')
    op.drop_table('articles')
    
    op.drop_index(op.f('ix_source_enabled'), table_name='source')
    op.drop_index(op.f('ix_source_name'), table_name='source')
    op.drop_table('source')

