# Enum Types Usage Guide

## Overview

All category and status fields in the database models now use defined enum types for type safety and data consistency.

## Enums Created

### 1. ActivityCategory (`app/models/enums.py`)
**Used in**: `Activity.category`

**Values**:
- `SIGHTSEEING` - Sightseeing activities
- `RESTAURANT` - Restaurants and dining
- `HOTEL` - Hotels and accommodation
- `TRANSPORT` - Transportation
- `SHOPPING` - Shopping
- `ENTERTAINMENT` - Entertainment
- `OUTDOOR` - Outdoor activities
- `CULTURE` - Cultural activities
- `NIGHTLIFE` - Nightlife
- `BEACH` - Beach activities
- `MOUNTAIN` - Mountain activities
- `MUSEUM` - Museums
- `PARK` - Parks
- `THEATER` - Theaters
- `SPORTS` - Sports activities
- `SPA` - Spa and wellness
- `OTHER` - Other activities

**Example**:
```python
from app.models.enums import ActivityCategory

activity.category = ActivityCategory.RESTAURANT
# Stored as "restaurant" in database
```

### 2. ExpenseCategory (`app/models/enums.py`)
**Used in**: `Expense.category`

**Values**:
- `FOOD` - Food expenses
- `TRANSPORT` - Transportation expenses
- `ACCOMMODATION` - Accommodation expenses
- `SHOPPING` - Shopping expenses
- `ENTERTAINMENT` - Entertainment expenses
- `ACTIVITIES` - Activity expenses
- `DRINKS` - Drinks expenses
- `TIPS` - Tips
- `TAXES` - Taxes
- `INSURANCE` - Insurance
- `VISA` - Visa fees
- `HEALTHCARE` - Healthcare expenses
- `EMERGENCY` - Emergency expenses
- `OTHER` - Other expenses

**Example**:
```python
from app.models.enums import ExpenseCategory

expense.category = ExpenseCategory.FOOD
# Stored as "food" in database
```

### 3. TripStatus (`app/models/enums.py`)
**Used in**: `Trip.status`

**Values**:
- `PLANNED` - Trip is planned
- `ONGOING` - Trip is ongoing
- `COMPLETED` - Trip is completed
- `CANCELLED` - Trip is cancelled

**Example**:
```python
from app.models.enums import TripStatus

trip.status = TripStatus.ONGOING
# Stored as "ongoing" in database
```

### 4. TripMemberRole (`app/models/enums.py`)
**Used in**: `TripMember.role`

**Values**:
- `OWNER` - Trip owner
- `ADMIN` - Trip admin
- `MEMBER` - Trip member

**Example**:
```python
from app.models.enums import TripMemberRole

trip_member.role = TripMemberRole.ADMIN
# Stored as "admin" in database
```

### 5. TripMemberStatus (`app/models/enums.py`)
**Used in**: `TripMember.status`

**Values**:
- `INVITED` - Member is invited
- `ACCEPTED` - Member has accepted
- `DECLINED` - Member has declined

**Example**:
```python
from app.models.enums import TripMemberStatus

trip_member.status = TripMemberStatus.ACCEPTED
# Stored as "accepted" in database
```

### 6. ActivityStatus (`app/models/enums.py`)
**Used in**: `Activity.status`

**Values**:
- `PLANNED` - Activity is planned
- `CONFIRMED` - Activity is confirmed
- `COMPLETED` - Activity is completed
- `CANCELLED` - Activity is cancelled

**Example**:
```python
from app.models.enums import ActivityStatus

activity.status = ActivityStatus.CONFIRMED
# Stored as "confirmed" in database
```

### 7. ScheduleBlockStatus (`app/models/enums.py`)
**Used in**: `ScheduleBlock.status`

**Values**:
- `SCHEDULED` - Block is scheduled
- `CONFIRMED` - Block is confirmed
- `CANCELLED` - Block is cancelled

**Example**:
```python
from app.models.enums import ScheduleBlockStatus

schedule_block.status = ScheduleBlockStatus.CONFIRMED
# Stored as "confirmed" in database
```

### 8. MessageType (`app/models/enums.py`)
**Used in**: `Message.message_type`

**Values**:
- `TEXT` - Text message
- `IMAGE` - Image message
- `FILE` - File message
- `LOCATION` - Location message
- `SYSTEM` - System message

**Example**:
```python
from app.models.enums import MessageType

message.message_type = MessageType.IMAGE
# Stored as "image" in database
```

### 9. PaymentMethod (`app/models/enums.py`)
**Used in**: `Expense.payment_method`

**Values**:
- `CASH` - Cash payment
- `CARD` - Card payment
- `CREDIT_CARD` - Credit card payment
- `DEBIT_CARD` - Debit card payment
- `PAYPAL` - PayPal payment
- `VENMO` - Venmo payment
- `BANK_TRANSFER` - Bank transfer payment
- `OTHER` - Other payment method

**Example**:
```python
from app.models.enums import PaymentMethod

expense.payment_method = PaymentMethod.CARD
# Stored as "card" in database
```

## Database Implementation

All enums are stored as **VARCHAR(50)** in the database using `native_enum=False`. This ensures:
- **Portability** - Works across different databases
- **Flexibility** - Easy to add new values without database migrations
- **Performance** - Indexed for fast queries
- **Type Safety** - Python enums provide type checking

## Usage in Models

### Example: Activity Model
```python
from sqlalchemy import Column, Enum
from app.models.enums import ActivityCategory, ActivityStatus

class Activity(Base):
    category = Column(Enum(ActivityCategory, native_enum=False, length=50), nullable=True, index=True)
    status = Column(Enum(ActivityStatus, native_enum=False, length=50), default=ActivityStatus.PLANNED)
```

### Example: Expense Model
```python
from sqlalchemy import Column, Enum
from app.models.enums import ExpenseCategory, PaymentMethod

class Expense(Base):
    category = Column(Enum(ExpenseCategory, native_enum=False, length=50), nullable=True, index=True)
    payment_method = Column(Enum(PaymentMethod, native_enum=False, length=50), nullable=True)
```

## Usage in Code

### Creating Records
```python
from app.models.enums import ActivityCategory, ActivityStatus

activity = Activity(
    name="Eiffel Tower",
    category=ActivityCategory.SIGHTSEEING,
    status=ActivityStatus.PLANNED
)
```

### Querying Records
```python
from app.models.enums import ActivityCategory

# Filter by category
activities = db.query(Activity).filter(
    Activity.category == ActivityCategory.RESTAURANT
).all()

# Filter by status
planned_activities = db.query(Activity).filter(
    Activity.status == ActivityStatus.PLANNED
).all()
```

### Updating Records
```python
from app.models.enums import ActivityStatus

activity.status = ActivityStatus.CONFIRMED
db.commit()
```

## Benefits

1. **Type Safety** - IDE autocomplete and type checking
2. **Data Consistency** - Only valid values can be stored
3. **Documentation** - Clear list of valid values
4. **Refactoring** - Easy to rename values across codebase
5. **Validation** - Invalid values raise errors at runtime

## Migration Notes

When adding new enum values:
1. Add the value to the enum class in `app/models/enums.py`
2. No database migration needed (VARCHAR supports any string)
3. Update API documentation if needed
4. Update frontend if needed

## Examples

### Activity Categories
```python
# Valid
activity.category = ActivityCategory.RESTAURANT
activity.category = ActivityCategory.SIGHTSEEING
activity.category = ActivityCategory.OTHER

# Invalid (will raise error)
activity.category = "invalid_category"  # ❌ Not an enum value
```

### Trip Status
```python
# Valid
trip.status = TripStatus.PLANNED
trip.status = TripStatus.ONGOING
trip.status = TripStatus.COMPLETED
trip.status = TripStatus.CANCELLED

# Invalid (will raise error)
trip.status = "invalid_status"  # ❌ Not an enum value
```

## Summary

All category and status fields now use defined enum types:
- ✅ **ActivityCategory** - Activity categories
- ✅ **ExpenseCategory** - Expense categories
- ✅ **TripStatus** - Trip status
- ✅ **TripMemberRole** - Trip member roles
- ✅ **TripMemberStatus** - Trip member status
- ✅ **ActivityStatus** - Activity status
- ✅ **ScheduleBlockStatus** - Schedule block status
- ✅ **MessageType** - Message types
- ✅ **PaymentMethod** - Payment methods

These enums provide type safety, data consistency, and better code maintainability.

