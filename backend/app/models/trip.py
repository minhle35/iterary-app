"""
Trip database model.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    DateTime,
    ForeignKey,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import TripStatus, TripMemberRole, TripMemberStatus


class Trip(Base):
    """Trip database model."""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    destination = Column(String, nullable=False, index=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    group_size = Column(Integer, default=1)
    budget = Column(Numeric(10, 2), nullable=True)
    currency = Column(String, default="AUD")

    # Status
    status = Column(
        Enum(TripStatus, native_enum=False, length=50), default=TripStatus.PLANNED
    )

    # Metadata
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    created_by_user = relationship(
        "User", back_populates="created_trips", foreign_keys=[created_by_id]
    )
    members = relationship(
        "TripMember", back_populates="trip", cascade="all, delete-orphan"
    )
    activities = relationship(
        "Activity", back_populates="trip", cascade="all, delete-orphan"
    )


class TripMember(Base):
    """Trip member (many-to-many relationship between User and Trip)."""

    __tablename__ = "trip_members"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(
        Enum(TripMemberRole, native_enum=False, length=50),
        default=TripMemberRole.MEMBER,
    )
    status = Column(
        Enum(TripMemberStatus, native_enum=False, length=50),
        default=TripMemberStatus.INVITED,
    )

    # Timestamps
    joined_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    trip = relationship("Trip", back_populates="members")
    user = relationship("User", back_populates="trips")
