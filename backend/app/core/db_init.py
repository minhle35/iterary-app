"""
Database initialization script.
Creates all tables in the database.
"""

from app.core.database import Base, engine
# Import all models to ensure all tables are created
from app.models import (
    User,
    Trip,
    TripMember,
    Activity,
    Expense,
    ExpenseSplit,
    Photo,
    ScheduleBlock,
    Message,
    MessageRead,
)


def init_db():
    """Initialize database by creating all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db():
    """Drop all database tables."""
    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_db()
    else:
        init_db()
