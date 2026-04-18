# FastAPI - Router, Business Logic, Data Access Model

This repository demonstrates a clean, scalable way to structure a FastAPI application using a three-tiered architecture:

- Routers (API layer)
- Business Logic (service layer)
- Data Access (persistence layer)

The goal is to provide a structure that is:

- Easy to reason about
- Scalable as features grow
- Explicit about responsibilities
- Friendly to collaboration

<p align="center">
  <img src="docs/diagram.png">
</p>

## Core Concepts

### 1. Three-Tier Separation

Each layer has a clearly defined responsibility:

**Routers (src/routers)**

- Define API endpoints
- Handle request/response formatting
- Perform input validation (via Pydantic)
- Call into business logic

**Business Logic (src/business_logic)**

- Contains the core application logic
- Orchestrates workflows
- Enforces rules and validations
- Calls data access layer

**Data Access (src/data_access)**

- Responsible for interacting with the database
- Executes queries
- Maps raw data to structured models

### 2. Domain Driven Structure

Instead of organizing code by technical type (e.g., all routers together, all services together), this repository organizes code by **domain**.

A **domain** represents a functional area of the API.

Examples:

- `/api/items` -> `items` domain
- `/api/orders` -> `orders` domain

Each layer contains a `domains` directory, and each domain has its own isolated implementation per layer:

```
domains/
  items/
  orders/
```

This provides:

- Clear separation of features
- Easier navigation
- Better scalability as domains grow independently

### 3. Co-Located Models (No Global Schema Directory)

A key design choice in this repo is:

    Models live in the layer that owns them.

Instead of having a global `models/` or `schemas/` directory, each layer defines its own models:

```
business_logic/models
data_access/models
routers/response_models
```

**Why this matters:**

- **Encapsulation**: Each layer controls its own data structures
- **Decoupling**: Changes in one layer don't leak into others
- **Clarity**: Models are defined close to where they are used

**Examples:**

- Data Access models → represent database rows
- Business Logic models → represent domain concepts
- Router models → represent API contracts

These models may look similar, but they serve **different purposes** and should not be tightly coupled.

### 4. Layer-Specific Errors

Each layer also defines its own errors:

```
business_logic/errors
data_access/errors
```

This allows:

- Proper abstraction of failures
- Clean error translation between layers
- Avoiding leakage of low-level details (e.g., SQL errors reaching API responses)

## Repository Structure

```
src
├───business_logic
│   ├───domains
│   │   ├───items
│   │   └───orders
│   ├───errors
│   └───models
├───data_access
│   ├───domains
│   │   ├───items
│   │   └───orders
│   ├───errors
│   └───models
└───routers
    ├───domains
    │   ├───items
    │   └───orders
    └───response_models
```

## Request Flow

A typical request flows like this:

```
Client Request
    ↓
Router (validation + HTTP concerns)
    ↓
Business Logic (rules, orchestration)
    ↓
Data Access (database interaction)
    ↓
Business Logic (processing)
    ↓
Router (response formatting)
    ↓
Client Response
```

## Why This Approach?

This structure is designed to solve common problems in growing FastAPI projects:

**Without structure:**

- Business logic leaks into routers
- Database logic spreads everywhere
- Models become tightly coupled
- Code becomes hard to maintain

**With this structure:**

- Clear boundaries between concerns
- Easier testing (mock layers independently)
- Better long-term maintainability
- Scales cleanly with new domains

## When to Use This

This approach works best when:

- Your API has multiple domains (e.g., users, orders, payments)
- Business logic is non-trivial
- You expect the project to grow

For very small projects, this structure may feel heavy—but it becomes valuable quickly as complexity increases.

## Running a Test Server

Start the test server using the following command:

```sh
uv run fastapi dev src/main.py
```

## Testing Strategy

This repository uses pytest + FastAPI’s dependency injection system to enable clean, isolated testing.

To run the tests:

```sh
uv run pytest
```

The goal is:

- Each test runs against a fresh database
- No shared state between tests
- No reliance on application startup side-effects
- Tests remain fast and deterministic

This aligns with the overall architecture:

- Routers are tested via HTTP calls
- Business logic remains independent and testable in isolation
- Data access is exercised against a real (but temporary) database

Benefits:

- No mocking required for basic integration tests
- Realistic behavior (actual SQL execution)
- Fully isolated test environment
- Scales to other databases (PostgreSQL, etc.)
