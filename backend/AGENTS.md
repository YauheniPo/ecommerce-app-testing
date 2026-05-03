# Backend Agent Guide

## Overview
**Purpose:** FastAPI backend for the e-commerce demo  
**Stack:** Python 3.13+, FastAPI, SQLModel, SQLite, Alembic  
**Architecture:** Feature-based structure with dependency injection via FastAPI Depends()

## Cursor / terminal workflow

From the **repository root**, use **`just`** (see root [AGENTS.md](../AGENTS.md) and [justfile](../justfile)). Typical backend tasks:

- **Lint + mypy:** `just check`.
- **Format:** `just format` (formats backend and frontend).
- **Full CI:** `just ci`.

## Essential Commands

**Development:**
- `uv run python main.py` - Start development server (localhost:8001)
- `uv run fastapi dev main.py` - Start with hot-reload
- `uv sync` - Install/update dependencies

**Database:**
- `uv run alembic revision --autogenerate -m "message"` - Create migration
- `uv run alembic upgrade head` - Apply migrations
- `uv run alembic downgrade -1` - Rollback one migration
- `uv run python -m app.seed` - Seed database with sample data

**Quality Checks:**
- From repo root: `just check` (ruff + mypy), `just format`, `just ci`

## Code Style & Architecture

### Type Safety Requirements
- **Type hints:** Required for ALL functions, methods, and variables
- **SQLModel:** For database models and Pydantic validation
- **Strict mypy:** No `Any` types allowed. NEVER use `# type: ignore` comments - fix the underlying type issue instead

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    name: str = Field(max_length=100)
    price: float = Field(gt=0)
    category: str
    description: Optional[str] = None
    in_stock: bool = True

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
```

### FastAPI Patterns

**Dependency Injection:**
```python
from fastapi import Depends
from sqlmodel import Session

def get_session() -> Session:
    with engine.begin() as session:
        yield session

@app.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
) -> ProductResponse:
    # implementation
```

**Error Handling:**
```python
from fastapi import HTTPException
from typing import Union

def get_product_or_404(product_id: int, session: Session) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with id {product_id} not found"
        )
    return product
```

## Directory Structure

```
backend/
├── app/
│   ├── models/           # SQLModel database models
│   ├── schemas/          # Pydantic request/response models
│   ├── routers/          # FastAPI route handlers
│   ├── services/         # Business logic layer
│   ├── repositories/     # Database access layer
│   ├── dependencies.py   # FastAPI dependencies
│   └── database.py       # Database connection setup
├── alembic/
│   └── versions/         # Database migrations
└── main.py               # FastAPI application entry point
```

## Database Guidelines

### Migration Workflow
1. Modify SQLModel models
2. Generate migration: `uv run alembic revision --autogenerate -m "add_product_table"`
3. Review generated migration file
4. Apply: `uv run alembic upgrade head`

### Model Relationships
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str = Field(unique=True)
    
    orders: list["Order"] = Relationship(back_populates="user")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
    user: User = Relationship(back_populates="orders")
```

## API Design Standards

### RESTful Conventions
- `GET /products` - List products
- `POST /products` - Create product
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product (full)
- `PATCH /products/{id}` - Partial update
- `DELETE /products/{id}` - Delete product

### Response Format
```python
# Success responses
{"data": {...}, "message": "Product created successfully"}

# Error responses  
{"error": "Product not found", "code": "PRODUCT_NOT_FOUND"}

# List responses with pagination
{
    "data": [...],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 100,
        "pages": 5
    }
}
```

## Security Practices

- **Input Validation:** All inputs validated with Pydantic models
- **SQL Injection Prevention:** Use SQLModel, never raw SQL
- **Authentication:** JWT tokens via Authorization header
- **Environment Variables:** All secrets in `.env`, never committed
- **CORS:** Configure properly for frontend origin

## Performance Considerations

- **Database Queries:** Use select/joinload for relationships
- **Pagination:** Always paginate list endpoints
- **Caching:** Consider Redis for frequently accessed data
- **Async Operations:** Use async/await for I/O operations

