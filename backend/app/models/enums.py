"""
Enum types for database models.
"""

import enum


class ActivityCategory(str, enum.Enum):
    """Activity category enum."""

    SIGHTSEEING = "sightseeing"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    OUTDOOR = "outdoor"
    CULTURE = "culture"
    NIGHTLIFE = "nightlife"
    BEACH = "beach"
    MOUNTAIN = "mountain"
    MUSEUM = "museum"
    PARK = "park"
    THEATER = "theater"
    SPORTS = "sports"
    SPA = "spa"
    OTHER = "other"


class ExpenseCategory(str, enum.Enum):
    """Expense category enum."""

    FOOD = "food"
    TRANSPORT = "transport"
    ACCOMMODATION = "accommodation"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    ACTIVITIES = "activities"
    DRINKS = "drinks"
    TIPS = "tips"
    TAXES = "taxes"
    INSURANCE = "insurance"
    VISA = "visa"
    HEALTHCARE = "healthcare"
    EMERGENCY = "emergency"
    OTHER = "other"


class TripStatus(str, enum.Enum):
    """Trip status enum."""

    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TripMemberRole(str, enum.Enum):
    """Trip member role enum."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class TripMemberStatus(str, enum.Enum):
    """Trip member status enum."""

    INVITED = "invited"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class ActivityStatus(str, enum.Enum):
    """Activity status enum."""

    PLANNED = "planned"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ScheduleBlockStatus(str, enum.Enum):
    """Schedule block status enum."""

    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class MessageType(str, enum.Enum):
    """Message type enum."""

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    LOCATION = "location"
    SYSTEM = "system"


class PaymentMethod(str, enum.Enum):
    """Payment method enum."""

    CASH = "cash"
    CARD = "card"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    VENMO = "venmo"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"

