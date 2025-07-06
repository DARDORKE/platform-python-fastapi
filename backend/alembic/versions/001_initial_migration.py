"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types if they don't exist
    connection = op.get_bind()
    
    # Check and create userrole enum
    result = connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole')")).scalar()
    if not result:
        op.execute("CREATE TYPE userrole AS ENUM ('ADMIN', 'MANAGER', 'USER')")
    
    # Check and create projectstatus enum  
    result = connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'projectstatus')")).scalar()
    if not result:
        op.execute("CREATE TYPE projectstatus AS ENUM ('PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED')")
    
    # Check and create projectpriority enum
    result = connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'projectpriority')")).scalar()
    if not result:
        op.execute("CREATE TYPE projectpriority AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT')")
    
    # Check and create taskstatus enum
    result = connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus')")).scalar()
    if not result:
        op.execute("CREATE TYPE taskstatus AS ENUM ('TODO', 'IN_PROGRESS', 'REVIEW', 'DONE', 'CANCELLED')")
    
    # Check and create taskpriority enum
    result = connection.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskpriority')")).scalar()
    if not result:
        op.execute("CREATE TYPE taskpriority AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT')")

    # Create users table if it doesn't exist
    if not connection.dialect.has_table(connection, 'users'):
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('username', sa.String(length=100), nullable=False),
            sa.Column('full_name', sa.String(length=255), nullable=False),
            sa.Column('hashed_password', sa.String(length=255), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.Column('is_superuser', sa.Boolean(), nullable=True),
            sa.Column('role', postgresql.ENUM(name='userrole'), nullable=True),
            sa.Column('last_login', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        # Create indexes only if table was created
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
        op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create projects table if it doesn't exist
    if not connection.dialect.has_table(connection, 'projects'):
        op.create_table('projects',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('status', postgresql.ENUM(name='projectstatus'), nullable=True),
            sa.Column('priority', postgresql.ENUM(name='projectpriority'), nullable=True),
            sa.Column('start_date', sa.DateTime(), nullable=True),
            sa.Column('end_date', sa.DateTime(), nullable=True),
            sa.Column('budget', sa.Integer(), nullable=True),
            sa.Column('owner_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        # Create index only if table was created
        op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    # Create tasks table if it doesn't exist
    if not connection.dialect.has_table(connection, 'tasks'):
        op.create_table('tasks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('status', postgresql.ENUM(name='taskstatus'), nullable=True),
            sa.Column('priority', postgresql.ENUM(name='taskpriority'), nullable=True),
            sa.Column('due_date', sa.DateTime(), nullable=True),
            sa.Column('estimated_hours', sa.Integer(), nullable=True),
            sa.Column('actual_hours', sa.Integer(), nullable=True),
            sa.Column('is_completed', sa.Boolean(), nullable=True),
            sa.Column('completion_date', sa.DateTime(), nullable=True),
            sa.Column('owner_id', sa.Integer(), nullable=False),
            sa.Column('project_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        # Create index only if table was created
        op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS projectstatus')
    op.execute('DROP TYPE IF EXISTS projectpriority')
    op.execute('DROP TYPE IF EXISTS taskstatus')
    op.execute('DROP TYPE IF EXISTS taskpriority')