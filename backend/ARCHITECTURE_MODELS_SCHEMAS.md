# Models vs Schemas: Business Purpose and Usage

## Overview

In FastAPI/SQLAlchemy architecture:
- **Models** (SQLAlchemy) = Internal backend, database entities
- **Schemas** (Pydantic) = External API, frontend communication

---

## Models (SQLAlchemy) - Internal Backend

### Purpose
- **Database representation** - Define database tables and relationships
- **Internal business logic** - Core data entities
- **Backend-only** - Never sent directly to frontend

### Location
```
backend/app/models/
├── __init__.py
├── user.py          # User database model
├── trip.py            # Trip database model
├── activity.py       # Activity database model
└── expense.py        # Expense database model
```

### Example

```python
# app/models/trip.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trip(Base):  # SQLAlchemy model
    """Trip database model - INTERNAL backend representation."""
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    group_size = Column(Integer, default=1)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships (internal)
    created_by = relationship("User", back_populates="trips")
    activities = relationship("Activity", back_populates="trip")
    expenses = relationship("Expense", back_populates="trip")
```

### Characteristics
- ✅ **Database tables** - Maps to SQL tables
- ✅ **Relationships** - Foreign keys, joins
- ✅ **Backend-only** - Never exposed to frontend directly
- ✅ **Internal structure** - Can have internal fields (passwords, IDs, etc.)

---

## Schemas (Pydantic) - External API

### Purpose
- **API contracts** - Define request/response formats
- **Frontend communication** - What frontend sends/receives
- **Validation** - Validate incoming data
- **Serialization** - Convert to/from JSON

### Location
```
backend/app/schemas/
├── __init__.py
├── trip_parser.py    # Trip parser API schemas
├── trip.py          # Trip API schemas
├── user.py          # User API schemas
└── activity.py      # Activity API schemas
```

### Example

```python
# app/schemas/trip.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TripCreate(BaseModel):  # Pydantic schema
    """Trip creation request - FROM frontend."""
    name: str = Field(..., min_length=1, max_length=100)
    destination: str
    start_date: date
    end_date: Optional[date] = None
    group_size: int = Field(..., ge=1, le=50)
    # Note: No 'id', 'created_by_id' - frontend doesn't send these

class TripResponse(BaseModel):  # Pydantic schema
    """Trip response - TO frontend."""
    id: int
    name: str
    destination: str
    start_date: date
    end_date: Optional[date]
    group_size: int
    # Note: Only fields frontend needs (no internal fields)

class TripUpdate(BaseModel):  # Pydantic schema
    """Trip update request - FROM frontend."""
    name: Optional[str] = None
    destination: Optional[str] = None
    # Note: Only fields that can be updated
```

### Characteristics
- ✅ **API contracts** - Define what frontend can send/receive
- ✅ **Validation** - Validate data before processing
- ✅ **Public interface** - What external clients see
- ✅ **JSON serializable** - Converts to/from JSON automatically

---

## Data Flow

```
┌─────────────┐
│  Frontend   │
│  (React)    │
└──────┬──────┘
       │
       │ HTTP Request (JSON)
       │ { "name": "Trip", "destination": "Melbourne" }
       ↓
┌─────────────────────────────────────────────────────┐
│  API Endpoint (FastAPI)                             │
│                                                      │
│  1. Receives Pydantic Schema (TripCreate)          │
│     - Validates data                                │
│     - Converts JSON → Pydantic object               │
│                                                      │
│  2. Converts to SQLAlchemy Model (Trip)            │
│     - Pydantic → SQLAlchemy                         │
│     - Business logic                                │
│                                                      │
│  3. Saves to Database                               │
│     - SQLAlchemy model → Database                   │
│                                                      │
│  4. Converts back to Pydantic Schema (TripResponse)│
│     - SQLAlchemy → Pydantic                         │
│     - Filters internal fields                       │
│                                                      │
│  5. Returns Pydantic Schema (JSON)                 │
│     - Converts to JSON                             │
└──────┬──────────────────────────────────────────────┘
       │
       │ HTTP Response (JSON)
       │ { "id": 1, "name": "Trip", "destination": "Melbourne" }
       ↓
┌─────────────┐
│  Frontend   │
│  (React)    │
└─────────────┘
```

---

## Key Differences

| Aspect | Models (SQLAlchemy) | Schemas (Pydantic) |
|--------|-------------------|-------------------|
| **Purpose** | Database entities | API contracts |
| **Used by** | Backend only | Frontend ↔ Backend |
| **Location** | `app/models/` | `app/schemas/` |
| **Base class** | `Base` (SQLAlchemy) | `BaseModel` (Pydantic) |
| **Database** | Maps to tables | Not in database |
| **Relationships** | Foreign keys, joins | Nested objects |
| **Validation** | Database constraints | Pydantic validators |
| **Serialization** | Manual conversion | Automatic JSON |
| **Internal fields** | Can have passwords, IDs | Only public fields |

---

## When to Use Which

### Use Models (SQLAlchemy) when:
- ✅ Defining database tables
- ✅ Storing data in database
- ✅ Internal business logic
- ✅ Database relationships
- ✅ Backend-only operations

### Use Schemas (Pydantic) when:
- ✅ API request/response
- ✅ Frontend communication
- ✅ Data validation
- ✅ API documentation (FastAPI auto-generates)
- ✅ External interfaces

---

## Example: Complete Flow

### 1. Frontend sends request:
```typescript
// Frontend (TypeScript)
const trip = await api.post('/api/trips', {
  name: "Melbourne Trip",
  destination: "Melbourne",
  start_date: "2025-11-24",
  group_size: 8
});
```

### 2. Backend receives (Pydantic Schema):
```python
# app/schemas/trip.py
class TripCreate(BaseModel):
    name: str
    destination: str
    start_date: date
    group_size: int
```

### 3. Convert to Model (SQLAlchemy):
```python
# app/api/trips.py
@router.post("/trips", response_model=TripResponse)
async def create_trip(trip: TripCreate, current_user: User):
    # Convert Pydantic schema → SQLAlchemy model
    db_trip = Trip(
        name=trip.name,
        destination=trip.destination,
        start_date=trip.start_date,
        group_size=trip.group_size,
        created_by_id=current_user.id  # Internal field, not in schema
    )

    # Save to database
    db.add(db_trip)
    db.commit()

    # Convert SQLAlchemy model → Pydantic schema
    return TripResponse.from_orm(db_trip)
```

### 4. Backend returns (Pydantic Schema):
```python
# app/schemas/trip.py
class TripResponse(BaseModel):
    id: int
    name: str
    destination: str
    start_date: date
    group_size: int
    # Note: No 'created_by_id' - internal field
```

### 5. Frontend receives response:
```typescript
// Frontend receives
{
  id: 1,
  name: "Melbourne Trip",
  destination: "Melbourne",
  start_date: "2025-11-24",
  group_size: 8
}
```

---

## Best Practices

### 1. Never expose Models directly
```python
#  BAD - Don't return model directly
@router.get("/trips/{id}")
async def get_trip(id: int):
    trip = db.query(Trip).filter(Trip.id == id).first()
    return trip  #  Exposes internal fields!

#  GOOD - Use schema
@router.get("/trips/{id}", response_model=TripResponse)
async def get_trip(id: int):
    trip = db.query(Trip).filter(Trip.id == id).first()
    return TripResponse.from_orm(trip)  # Only public fields
```

### 2. Separate create/update/response schemas
```python
#  GOOD - Different schemas for different operations
class TripCreate(BaseModel):    # What frontend sends
    name: str
    destination: str

class TripUpdate(BaseModel):    # What frontend sends for updates
    name: Optional[str] = None
    destination: Optional[str] = None

class TripResponse(BaseModel):  # What frontend receives
    id: int
    name: str
    destination: str
```

### 3. Use schemas for validation
```python
#  Pydantic automatically validates
class TripCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    group_size: int = Field(..., ge=1, le=50)  # 1-50 people

# If invalid, FastAPI returns 422 error automatically
```

---

## Summary

### Models (SQLAlchemy)
- **Purpose**: Database entities, internal backend
- **Location**: `app/models/`
- **Used by**: Backend only
- **Never**: Sent to frontend directly

### Schemas (Pydantic)
- **Purpose**: API contracts, frontend communication
- **Location**: `app/schemas/`
- **Used by**: Frontend ↔ Backend
- **Always**: Used for API requests/responses

### Data Flow
```
Frontend → Pydantic Schema → SQLAlchemy Model → Database
Database → SQLAlchemy Model → Pydantic Schema → Frontend
```

---

## Your Current Project

### Current State
- **Models**: Empty (no database models yet)
- **Schemas**: `trip_parser.py` (API schemas for trip parsing)

### Next Steps
1. **Create Models** when you add database tables
2. **Create Schemas** for each API endpoint
3. **Convert** between models and schemas in API endpoints

Example structure:
```
app/
├── models/
│   ├── user.py      # User database model
│   ├── trip.py      # Trip database model
│   └── activity.py  # Activity database model
├── schemas/
│   ├── user.py      # User API schemas
│   ├── trip.py      # Trip API schemas
│   └── activity.py  # Activity API schemas
└── api/
    ├── trips.py     # Trip API endpoints (uses both)
    └── users.py     # User API endpoints (uses both)
```

