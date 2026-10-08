# Database Migrations (Alembic)

This directory stores versioned database schema migration scripts.

## Usage
To generate a new migration after modifying SQLAlchemy models:
```bash
alembic revision --autogenerate -m "Add new field to scans table"
```

To apply migrations to the target database:
```bash
alembic upgrade head
```
