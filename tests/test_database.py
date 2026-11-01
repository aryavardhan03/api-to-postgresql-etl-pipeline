
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL


@pytest.fixture
def db_engine():
    """Create a connection to the local PostgreSQL database."""

    load_dotenv()

    required_variables = [
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME"
    ]

    missing = [
        variable for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        pytest.fail(f"Missing database configuration: {missing}")

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(connection_url)

    yield engine

    engine.dispose()


def test_database_connection(db_engine):

    with db_engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_products_table_exists(db_engine):

    inspector = inspect(db_engine)

    assert inspector.has_table("products", schema="public")


def test_products_table_has_required_columns(db_engine):

    inspector = inspect(db_engine)

    columns = {
        column["name"]
        for column in inspector.get_columns(
            "products",
            schema="public"
        )
    }

    expected_columns = {
        "id",
        "title",
        "description",
        "category",
        "price",
        "discount_percentage",
        "rating",
        "stock",
        "brand",
        "thumbnail"
    }

    assert expected_columns.issubset(columns)


def test_products_can_be_queried(db_engine):

    with db_engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM products")
        )

        count = result.scalar()

        assert count >= 0
