# FastAPI Project Template

> [!NOTE]
> See companion blog post [here](https://noahhefner.github.io/website/posts/fastapi-template/).

This repository presents a flexible, scalable way to structure a RESTful FastAPI application.

## Overview

REST APIs often expose endpoints for multiple business **domains**. A domain is a functional area of the API (in this repository, the two example domains are `items` and `orders`).

In many FastAPI templates, the repository separates code by "type" into four primary areas:

- **Routers**: Handling HTTP requests and mapping business logic errors to HTTP status codes.
- **Models/Schemas**: Validating request and response data shapes.
- **Services**: Business logic.
- **Tests**: Unit and integration tests.

The result is a repository structured something like this:

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── internal/
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── db/
│       ├── __init__.py
│       ├── database.py
│       └── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_users.py
│   ├── test_items.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run.sh
```

While this works for small projects, as the API grows, developers often have to keep track of multiple parallel directory structures to work on a single feature.

This repository argues for a different approach: **domains** serve as the primary organizational unit. All logic for a given domain is encapsulated within its own directory:

```plaintext
├── domains
│   ├── __init__.py
│   ├── items
│   │   ├── get_all_items
│   │   │   ├── __init__.py
│   │   │   └── test_get_all_items.py
│   │   ├── get_item_by_id
│   │   │   ├── __init__.py
│   │   │   └── test_get_item_by_id.py
│   │   └── __init__.py
│   └── orders
│       ├── get_all_orders
│       │   ├── __init__.py
│       │   └── test_get_all_orders.py
│       ├── get_order_by_id
│       │   ├── __init__.py
│       │   ├── errors.py
│       │   ├── get_order_by_id.py
│       │   ├── models.py
│       │   └── test_get_order_by_id.py
│       └── __init__.py
```

By encapsulating each endpoint in its own directory, you gain two primary benefits:

1. **Colocated Related Code**: By placing data models, business logic, unit tests, and HTTP handling in the same directory, developers no longer need to jump between distant folders to make a single functional change.
2. **Flexible Complexity**: Not every endpoint is complex. Some might simply execute a short SQL query and return a response (ex. `items` endpoints). Others might involve dynamic query building, third-party APIs, or complex authorization. This structure allows simple endpoints to exist in a single file, while complex ones can be broken down into separate files for models, business logic, and errors within the same directory (ex. `get_order_by_id`).

## When To Use This Structure (And When Not To)

I created this template repository because I was frustrated with the poor developer ergonomics of the FastAPI “best-practice” layouts found online, especially in larger codebases. This layout provides a practical balance between developer experience and organizational rigidity.

If you are building a quick proof-of-concept or a single-domain API, this structure may be overkill. However, if your API has many domains, is expected to scale, or you simply prefer that related code stay grouped together, this structure is an excellent choice.

## Testing

[Pytest](https://docs.pytest.org/en/stable/) is used for testing the API endpoints. Following the same philosophy as the rest of the repository, test case files are colocated with the code they cover.

A shared `conftest.py` overrides the `get_db` dependency, ensuring each test runs against a fresh database instance.

To run the tests:

```sh
uv run pytest
```

## Running the HTTP Server

Start the server using the following command:

```sh
uv run fastapi dev
```

## Docker

A `Dockerfile` is provided to demonstrate how to containerize this application.

```dockerfile
# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.14-alpine3.23 AS builder

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-cache --no-group dev --no-install-project

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.14-alpine3.23 AS runner

WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code with correct ownership
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup pyproject.toml ./

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

# Document exposed port
EXPOSE 8000

# Run with uvicorn
ENTRYPOINT ["uvicorn"]
CMD ["fastapi_template.main:app", "--host", "0.0.0.0", "--port", "8000"]
```