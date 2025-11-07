# Collaborative Group Travel Planning Platform

A unified platform for planning, coordinating, and documenting group trips with intelligent scheduling, expense tracking, and AI-powered features.

---

## Table of Contents

- [Background](#background)
- [Problem Statement](#problem-statement)
- [User Needs](#user-needs)
- [Project Constraints](#project-constraints)
- [Solution Overview](#solution-overview)
- [Architecture](#architecture)
- [MVP Features](#mvp-features)
- [Data Models](#data-models)
- [Technology Stack](#technology-stack)
- [API Structure](#api-structure)

---

## Background

Planning group trips involves coordinating multiple people with different schedules, preferences, and budgets. Traditional tools like Google Sheets, WhatsApp groups, and separate expense apps create a fragmented experience where information gets lost and coordination becomes chaotic.

### Personal Context

Planning a 2-week Australia trip for 8 family members with remote work schedules, different city preferences, and varying budgets exposed gaps in existing solutions. This project addresses those real pain points.

---

## Problem Statement

- **Scattered information** across multiple platforms (messages, spreadsheets, expense trackers)
- **No efficient way** to handle conflicting schedules and availability
- **Difficult to optimize routes** across multiple cities with time and budget constraints
- **Poor photo organization** - hard to search memories later
- **Manual expense splitting** and settlement calculations

---

## User Needs

- Single platform for planning, during-trip coordination, and post-trip memories
- Track contact details of accommodations (email, phone number)
- Track open and close times of places users want to visit and use that information to plan accordingly; raise alerts if users plan activities that conflict with open or closing times
- Smart scheduling that respects individual constraints
- Natural language search for photos and information
- Real-time collaboration without conflicts
- Person-in-charge assignment for activities
- Automated expense tracking and splitting

---

## Project Constraints

### Timeline

- **Week 1-4**: MVP with core features in Python/TypeScript
- **Week 5**: Performance optimization (C++/Rust integration) - tentative
- **Week 6**: Testing, deployment, documentation

### Budget (Minimal Cloud Costs)

- **Target**: Under $20/month for development
- **AWS Free Tier**: RDS, S3, Lambda
- **OpenAI API**
- **Photo storage optimization** to reduce S3 costs

### Technical Resources

- Focus on demonstrable technical depth over feature breadth
- Use existing libraries where appropriate

---

## Solution Overview

### Core Value Propositions

#### 1. Unified Platform
- Single source of truth for all trip data
- Real-time collaboration with conflict resolution
- Persistent memory with natural language search

#### 2. Intelligent Planning
- AI-powered itinerary generation
- Route optimization (genetic algorithms)
- Smart scheduling with availability checking
- Budget-aware suggestions

#### 3. Practical During-Trip Features
- Real-time chat for trip coordination
- Real-time location sharing
- Receipt OCR and expense splitting
- Offline-capable PWA
- Quick search and information retrieval

#### 4. Post-Trip Value
- Photo organization with AI tagging
- Natural language search ("beach photos in Sydney")
- Shareable trip summaries
- Budget analysis and reports

### Technical Differentiation

**Multi-Language Architecture:**
- **Python**: Rapid development, AI integration, business logic
- **TypeScript**: Type-safe frontend, component reusability
- **C++**: Performance-critical operations (route optimization, image processing)
- **Rust**: Security-critical services (authentication, payments)

**Why This Matters:**
- Make use of algorithms (TSP, genetic algorithms)
- Study performance-related processes in backend and cloud deployment


---

## Architecture

### System Overview

```
Frontend (TypeScript/React PWA)
    ↓ REST API / WebSocket
Backend (Python/FastAPI)
    ├─ Business Logic (95% of code)
    ├─ C++ Services (5% - performance critical)
    │   ├─ Route Optimizer (genetic algorithm)
    │   └─ Image Processor (compression, thumbnails)
    └─ Rust Services (3% - security critical)
        └─ Auth Service (JWT validation)
    ↓
Databases
    ├─ PostgreSQL (structured data)
    ├─ Redis (cache, sessions, real-time)
    └─ S3 (photos, receipts)
```

---

## MVP Features

### 1. User Management
- Registration and authentication (JWT)
- User profiles with preferences
- Invitation system for trips

### 2. Trip Planning
- Create trip with basic details
- Invite members via email
- Add/edit/delete activities
- Simple schedule timeline
- Use AI to recommend activities, places and simple drag-and-drop UI into trip timetable

### 3. Real-time Chat
- Trip-based chat rooms via WebSocket
- Real-time message delivery
- Message history persistence
- User presence indicators (online/offline)
- Typing indicators
- Message read receipts

### 4. Collaborative Scheduling
- Drag-and-drop interface for activities
- Real-time updates via WebSocket
- User availability tracking
- Basic conflict detection

### 5. Expense Tracking
- Manual expense entry
- Simple equal splitting
- Running total display
- Settlement calculation

### 6. Photo Management
- Upload photos with GPS data
- Basic tagging and organization
- Photo gallery view
- Simple search by location/date

### 7. Search (Basic)
- Text search for activities
- Filter by category, date, cost
- Location-based search

---

## Data Models

### Core Entities

- **Users** (authentication, preferences)
- **Trips** (destination, dates, budget)
- **Activities** (location, cost, duration, category)
- **Expenses** (amount, category, splits)
- **Photos** (location, timestamp, tags)
- **Schedule Blocks** (time slots, assignments)
- **Messages** (content, timestamp, read status)

### Relationships

- Trip has many Members (users)
- Trip has many Activities
- Trip has many Expenses
- Trip has many Messages
- Activity has many Photos
- Expense has many Splits
- Schedule has many Blocks
- User has many Messages (sent messages)

---

## Technology Stack

### Frontend

- React 18 with TypeScript
- Tailwind CSS for styling
- React Query for server state
- Socket.IO client for real-time
- Mapbox GL for maps
- IndexedDB for offline support

### Backend

- Python 3.11+ with FastAPI
- SQLAlchemy ORM
- Pydantic for validation
- Celery for background tasks
- Socket.IO for WebSocket

### Infrastructure

- Docker for containerization
- AWS RDS (PostgreSQL)
- AWS ElastiCache (Redis)
- AWS S3 for media storage
- AWS ECS for deployment
- GitHub Actions for CI/CD

---

## API Structure

### REST Endpoints

#### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
```

#### Trips
```

```

#### Activities
```

```

#### Schedule
```

```

#### Expenses
```

```

#### Photos
```

```

#### Messages
```

```

#### Search
```
```

### WebSocket Events

#### Client → Server
- `join_trip`
- `update_schedule`


#### Server → Client
- `schedule_updated`
- `member_joined`
- `location_updated`


---

## Future Enhancements

_To be documented as the project evolves._
