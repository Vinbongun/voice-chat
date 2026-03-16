"""Initial schema: chat_sessions, chat_messages, employees, message_feedback, audit_logs

Revision ID: 000
Revises:
Create Date: 2026-03-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET

revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'chat_sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_chat_sessions_user_id', 'chat_sessions', ['user_id'])

    op.create_table(
        'chat_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('session_id', UUID(as_uuid=True), sa.ForeignKey('chat_sessions.id'), nullable=True),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('metadata_', JSONB),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_chat_messages_session_created', 'chat_messages', ['session_id', 'created_at'])

    op.create_table(
        'employees',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('position', sa.String(255)),
        sa.Column('department', sa.String(255)),
        sa.Column('phone', sa.String(50)),
        sa.Column('email', sa.String(255)),
        sa.Column('photo_url', sa.Text),
        sa.Column('city', sa.String(100)),
        sa.Column('bitrix_id', sa.String(100)),
        sa.Column('synced_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.execute("""
        CREATE INDEX ix_employees_fts ON employees
        USING gin(to_tsvector('russian',
            name || ' ' || COALESCE(position, '') || ' ' || COALESCE(department, '')))
    """)

    op.create_table(
        'message_feedback',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('message_id', UUID(as_uuid=True), sa.ForeignKey('chat_messages.id'), nullable=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('rating', sa.SmallInteger, nullable=False),
        sa.Column('comment', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('user_name', sa.String(255)),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100)),
        sa.Column('resource_id', sa.String(255)),
        sa.Column('ip_address', INET),
        sa.Column('request_summary', sa.Text),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_audit_logs_user_created', 'audit_logs', ['user_id', 'created_at'])
    op.create_index('ix_audit_logs_action_created', 'audit_logs', ['action', 'created_at'])


def downgrade() -> None:
    op.drop_index('ix_audit_logs_action_created')
    op.drop_index('ix_audit_logs_user_created')
    op.drop_table('audit_logs')
    op.drop_table('message_feedback')
    op.drop_index('ix_employees_fts')
    op.drop_table('employees')
    op.drop_index('ix_chat_messages_session_created')
    op.drop_table('chat_messages')
    op.drop_index('ix_chat_sessions_user_id')
    op.drop_table('chat_sessions')
