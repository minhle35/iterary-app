# Database Models Summary

## Overview

All database models have been created for the Iterary App. These models define the database structure and relationships.

## Models Created

### 1. User (`app/models/user.py`)
- **Table**: `users`**
- **Fields**: id, email, username, hashed_password, full_name, timezone, currency, language, is_active, is_verified, created_at
- **Relationships**:
  - Has many trips (through TripMember)
  - Has many created trips
  - Has many expense splits
  - Has many messages (sent)
  - Has many photos (uploaded)

### 2. Trip (`app/models/trip.py`)
- **Tables**: `trips`, `trip_members`
- **Trip Fields**: id, name, description, destination, start_date, end_date, group_size, budget, currency, status, created_by_id, created_at, updated_at
- **TripMember Fields**: id, trip_id, user_id, role, status, joined_at, created_at
- **Relationships**:
  - Belongs to User (created_by)
  - Has many members (through TripMember)
  - Has many activities
  - Has many expenses
  - Has many messages
  - Has many schedule blocks

### 3. Activity (`app/models/activity.py`)
- **Table**: `activities`
- **Fields**: id, trip_id, name, description, category, location, address, latitude, longitude, date, start_time, end_time, duration_minutes, cost, currency, cost_per_person, assigned_to_id, status, notes, contact_info, opening_hours, created_at, updated_at
- **Relationships**:
  - Belongs to Trip
  - Belongs to User (assigned_to)
  - Has many photos

### 4. Expense (`app/models/expense.py`)


### 5. Photo (`app/models/photo.py`)


### 6. ScheduleBlock (`app/models/schedule.py`)


### 7. Message (`app/models/message.py`)


## Database Relationships

### Many-to-Many Relationships

1. **User ↔ Trip** (through TripMember)
   - A user can be a member of many trips
   - A trip can have many members
   - TripMember tracks role and status

2. **Expense ↔ User** (through ExpenseSplit)
   - An expense can be split among many users
   - A user can be part of many expense splits
   - ExpenseSplit tracks amount owed and payment status

3. **Message ↔ User** (through MessageRead)
   - A message can be read by many users
   - A user can read many messages
   - MessageRead tracks read status

### One-to-Many Relationships

1. **User → Trip** (created_trips)
   - A user can create many trips

2. **Trip → Activity**
   - A trip can have many activities



### Foreign Key Relationships

- Trip.created_by_id → User.id
- TripMember.trip_id → Trip.id
- TripMember.user_id → User.id
- Activity.trip_id → Trip.id
- Activity.assigned_to_id → User.id


## Database Initialization

### Initialize Database

To create all tables in the database:

```bash
cd backend
uv run python -m app.core.db_init
```

Or using the database initialization script:

```bash
cd backend
uv run python app/core/db_init.py
```

### Drop Database (Development Only)

To drop all tables (use with caution):

```bash
cd backend
uv run python app/core/db_init.py drop
```

## Next Steps

1. **Create Pydantic Schemas** for each model (in `app/schemas/`)
2. **Create API Endpoints** for each model (in `app/api/`)
3. **Set up Alembic** for database migrations
4. **Add Authentication** middleware
5. **Create Services** for business logic

## Notes

- All timestamps use `DateTime(timezone=True)` for timezone-aware dates
- All relationships use `cascade="all, delete-orphan"` where appropriate
- Foreign keys are properly indexed for performance
- String fields that are frequently searched are indexed

