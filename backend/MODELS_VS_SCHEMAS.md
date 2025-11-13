# Models vs Schemas: Business Purpose Guide

## 🎯 Quick Answer

### Models (SQLAlchemy) - Internal Backend
- **Purpose**: Database entities, internal backend
- **Location**: `app/models/`
- **Used by**: Backend only (database operations)
- **Never**: Sent directly to frontend

### Schemas (Pydantic) - External API
- **Purpose**: API contracts, frontend communication
- **Location**: `app/schemas/`
- **Used by**: Frontend ↔ Backend (API requests/responses)
- **Always**: Used for API endpoints

---

## 📊 Visual Flow

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
│     ✅ FROM frontend                                │
│     ✅ Validates data                               │
│                                                      │
│  2. Converts to SQLAlchemy Model (Trip)            │
│     ✅ Internal backend                             │
│     ✅ Business logic                               │
│                                                      │
│  3. Saves to Database                               │
│     ✅ Model → Database                             │
│                                                      │
│  4. Converts back to Pydantic Schema (TripResponse)│
│     ✅ TO frontend                                  │
│     ✅ Filters internal fields                      │
│                                                      │
│  5. Returns JSON                                    │
│     ✅ Pydantic → JSON                              │
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

## 🔑 Key Differences

| Aspect | Models (SQLAlchemy) | Schemas (Pydantic) |
|--------|-------------------|-------------------|
| **Base Class** | `Base` (SQLAlchemy) | `BaseModel` (Pydantic) |
| **Purpose** | Database tables | API contracts |
| **Location** | `app/models/` | `app/schemas/` |
| **Used by** | Backend only | Frontend ↔ Backend |
| **Database** | Maps to SQL tables | Not in database |
| **Relationships** | Foreign keys, joins | Nested objects |
| **Validation** | Database constraints | Pydantic validators |
| **Serialization** | Manual conversion | Automatic JSON |
| **Internal Fields** | Can have passwords, IDs | Only public fields |

---

## 📝 Examples

### Model (SQLAlchemy) - Internal Backend

```python
# app/models/trip.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trip(Base):  # SQLAlchemy model
    """Trip database model - INTERNAL backend only."""
    __tablename__ = "trips"

    # Database columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    group_size = Column(Integer, default=1)

    # Internal fields (never sent to frontend)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships (internal)
    created_by = relationship("User", back_populates="trips")
    activities = relationship("Activity", back_populates="trip")
    expenses = relationship("Expense", back_populates="trip")
```

### Schema (Pydantic) - External API

```python
# app/schemas/trip.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TripCreate(BaseModel):  # FROM frontend
    """Trip creation request - what frontend sends."""
    name: str = Field(..., min_length=1, max_length=100)
    destination: str
    start_date: date
    end_date: Optional[date] = None
    group_size: int = Field(..., ge=1, le=50)
    # Note: No 'id', 'created_by_id' - internal fields

class TripResponse(BaseModel):  # TO frontend
    """Trip response - what frontend receives."""
    id: int
    name: str
    destination: str
    start_date: date
    end_date: Optional[date]
    group_size: int
    # Note: No 'created_by_id', 'created_at' - internal fields
```

### API Endpoint (Uses Both)

```python
# app/api/trips.py
from app.models.trip import Trip  # SQLAlchemy model
from app.schemas.trip import TripCreate, TripResponse  # Pydantic schemas

@router.post("/trips", response_model=TripResponse)
async def create_trip(
    trip: TripCreate,  # Pydantic schema (FROM frontend)
    current_user: User,
    db: Session = Depends(get_db)
):
    # Convert Pydantic schema → SQLAlchemy model
    db_trip = Trip(  # SQLAlchemy model
        name=trip.name,
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        group_size=trip.group_size,
        created_by_id=current_user.id  # Internal field (not in schema)
    )

    # Save to database (using model)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    # Convert SQLAlchemy model → Pydantic schema
    return TripResponse.from_orm(db_trip)  # TO frontend
```

---

## 🔄 Conversion Between Models and Schemas

### Schema → Model
```python
# Convert Pydantic schema to SQLAlchemy model
trip_create = TripCreate(name="Trip", destination="Melbourne")

db_trip = Trip(  # SQLAlchemy model
    **trip_create.dict(),  # Extract fields from schema
    created_by_id=current_user.id  # Add internal fields
)
```

### Model → Schema
```python
# Convert SQLAlchemy model to Pydantic schema
db_trip = db.query(Trip).filter(Trip.id == 1).first()

trip_response = TripResponse.from_orm(db_trip)  # Pydantic schema
# Only public fields are included (internal fields filtered out)
```

---

## 📁 Directory Structure

```
backend/app/
├── models/              # SQLAlchemy models (database)
│   ├── __init__.py
│   ├── user.py          # User database model
│   ├── trip.py          # Trip database model
│   ├── activity.py      # Activity database model
│   └── expense.py       # Expense database model
│
├── schemas/             # Pydantic schemas (API)
│   ├── __init__.py
│   ├── user.py          # User API schemas
│   ├── trip.py          # Trip API schemas
│   ├── activity.py      # Activity API schemas
│   └── trip_parser.py   # Trip parser API schemas
│
└── api/                 # API endpoints
    ├── trips.py         # Uses both models and schemas
    ├── users.py         # Uses both models and schemas
    └── trip_planner.py  # Uses schemas (no models yet)
```

---

## 🎯 When to Use Which

### Use Models (SQLAlchemy) when:
- ✅ Defining database tables
- ✅ Storing data in database
- ✅ Internal business logic
- ✅ Database relationships (foreign keys, joins)
- ✅ Backend-only operations
- ❌ **Never** for API requests/responses

### Use Schemas (Pydantic) when:
- ✅ API requests (what frontend sends)
- ✅ API responses (what frontend receives)
- ✅ Data validation
- ✅ API documentation (FastAPI auto-generates)
- ✅ Frontend communication
- ❌ **Never** for database operations

---

## 🚫 Common Mistakes

### ❌ Mistake 1: Returning Model Directly
```python
# ❌ BAD - Don't return model directly
@router.get("/trips/{id}")
async def get_trip(id: int):
    trip = db.query(Trip).filter(Trip.id == id).first()
    return trip  # ❌ Exposes internal fields (created_by_id, etc.)

# ✅ GOOD - Use schema
@router.get("/trips/{id}", response_model=TripResponse)
async def get_trip(id: int):
    trip = db.query(Trip).filter(Trip.id == id).first()
    return TripResponse.from_orm(trip)  # ✅ Only public fields
```

### ❌ Mistake 2: Using Schema for Database Operations
```python
# ❌ BAD - Don't use schema for database
trip = db.query(TripCreate).filter(...)  # ❌ TripCreate is a schema, not a model

# ✅ GOOD - Use model for database
trip = db.query(Trip).filter(...)  # ✅ Trip is a model
```

### ❌ Mistake 3: Exposing Internal Fields
```python
# ❌ BAD - Schema with internal fields
class TripResponse(BaseModel):
    id: int
    created_by_id: int  # ❌ Internal field, shouldn't be in schema
    password_hash: str  # ❌ Internal field, security issue!

# ✅ GOOD - Schema with only public fields
class TripResponse(BaseModel):
    id: int
    name: str
    destination: str
    # ✅ Only public fields
```

---

## 📋 Your Current Project

### Current State

**Schemas** (✅ Has):
- `app/schemas/trip_parser.py`
  - `TripParserRequest` - FROM frontend
  - `TripPlanResponse` - TO frontend
  - `Activity` - TO frontend

**Models** (⬜ Empty):
- `app/models/` - No database models yet (you'll add these later)

### Current Flow

```
Frontend → TripParserRequest (Schema) → trip_planner.py → POI Service → TripPlanResponse (Schema) → Frontend
```

### Future Flow (When You Add Database)

```
Frontend → TripCreate (Schema) → API → Trip (Model) → Database
Database → Trip (Model) → API → TripResponse (Schema) → Frontend
```

---

## 📚 Summary

### Models (SQLAlchemy)
- **Purpose**: Database entities
- **Location**: `app/models/`
- **Used by**: Backend only
- **Example**: `Trip` (database table)

### Schemas (Pydantic)
- **Purpose**: API contracts
- **Location**: `app/schemas/`
- **Used by**: Frontend ↔ Backend
- **Example**: `TripCreate` (API request)

### Data Flow
```
Frontend → Schema → Model → Database
Database → Model → Schema → Frontend
```

### Remember
- **Models** = Internal backend (database)
- **Schemas** = External API (frontend)
- **Never** expose models directly to frontend
- **Always** use schemas for API requests/responses

