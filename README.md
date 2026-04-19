# FastAPI Repository Structure

This repository demonstrates a scalable way to structure a FastAPI application using a three-tiered architecture.

<p align="center">
  <img src="docs/diagram.drawio.png">
</p>

## Core Concepts

### Separation of Concerns in Three Layers

Each layer has a clearly defined responsibility.

The **router** layer defines API endpoints, performs request validation via Pydantic, invokes functions from the business logic layer, and formats HTTP responses.

The **business logic** layer contains the core application logic. This layer orchestrates workflows, enforces rules, and invokes functions from the data access layer to retrieve application data.

The **data access** layer is responsible for interacting with the database. This layer executes database queries and maps raw data to structured models via Pydantic.

### Domain-First Directory Structure

REST API's often expose endpoints for multiple business **domains**. A domain is simply a functional area of the API. (In this repository, the two domains are `items` and `orders`.)

It is common in FastAPI projects to place data models in their own top-level directory at the root of the project. Do a quick Google search for "how to structure FastAPI project" and you'll see many examples that look something like this:

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

This repository takes a different approach by colocating data models with the code that uses them, rather than placing them in a separate, centralized directory.

Within each layer, domains serve as the primary organizational unit. All related code—including models and errors—lives within the corresponding domain directory for that layer.

Consider, for example, the `data_access` directory:

```
├── data_access
│   ├── errors                 <- Global errors used by all domains
│   │   ├── database_error.py
│   ├── items                  <- Items domain directory
│   │   ├── errors             <- Items domain errors
│   │   │   ├── __init__.py
│   │   │   ├── item_not_found.py
│   │   ├── get_item_by_id.py  <- Items data access logic
│   │   ├── __init__.py
│   │   ├── models             <- Items data access models
│   │   │   ├── get_item_by_id.py
│   │   │   ├── __init__.py
│   └── orders                 <- Orders domain directory
│       ├── errors
│       │   ├── __init__.py
│       │   ├── order_not_found.py
│       ├── get_order_by_id.py
│       ├── __init__.py
│       ├── models
│       │   ├── get_order_by_id.py
│       │   ├── __init__.py
```

## Running a Test Server

Start the test server using the following command:

```sh
uv run fastapi dev src/main.py
```

## Testing Strategy

To run the tests:

```sh
uv run pytest
```

## TODO List:

- [ ] Document how to handle dependencies
- [ ] Create a database wrapper object using Protocols to enable multiple database implementations
- [ ] Better test documentation