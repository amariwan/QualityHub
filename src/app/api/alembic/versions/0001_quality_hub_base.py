"""initial quality hub schema

Revision ID: 0001_quality_hub_base
Revises:
Create Date: 2026-02-22 00:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.core.db.base import Base
from app.services.quality_hub.infrastructure.models import tables as _tables  # noqa: F401

# revision identifiers, used by Alembic.
revision = "0001_quality_hub_base"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
