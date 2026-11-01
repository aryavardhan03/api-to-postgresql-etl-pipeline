
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def get_engine():

    load_dotenv()

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    return create_engine(connection_url)


def load_products(df):

    if df.empty:
        print("No data available to load.")
        return

    engine = get_engine()

    try:
        # Step 1: Load cleaned data into a temporary staging table
        df.to_sql(
            name="products_staging",
            con=engine,
            schema="public",
            if_exists="replace",
            index=False
        )

        # Step 2: Insert new products and update existing products
        upsert_query = text("""
            INSERT INTO products (
                id,
                title,
                description,
                category,
                price,
                discount_percentage,
                rating,
                stock,
                brand,
                thumbnail
            )
            SELECT
                id,
                title,
                description,
                category,
                price,
                discount_percentage,
                rating,
                stock,
                brand,
                thumbnail
            FROM products_staging

            ON CONFLICT (id)
            DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                category = EXCLUDED.category,
                price = EXCLUDED.price,
                discount_percentage = EXCLUDED.discount_percentage,
                rating = EXCLUDED.rating,
                stock = EXCLUDED.stock,
                brand = EXCLUDED.brand,
                thumbnail = EXCLUDED.thumbnail,
                updated_at = CURRENT_TIMESTAMP;
        """)

        with engine.begin() as connection:
            connection.execute(upsert_query)

            connection.execute(
                text("DROP TABLE public.products_staging")
            )

        print("Data loaded successfully into PostgreSQL!")
        print("Records processed:", len(df))

    except Exception as error:
        print("Data loading failed:", error)
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":

    from .extract import extract_products
    from .transform import transform_products

    raw_data = extract_products()

    clean_data = transform_products(raw_data)

    load_products(clean_data)
