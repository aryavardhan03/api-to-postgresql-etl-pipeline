
import pandas as pd
from .extract import extract_products


def transform_products(df):
    """
    Clean and transform raw product data.
    """

    if df.empty:
        print("No data available for transformation.")
        return pd.DataFrame()

    # 1. Select required columns
    required_columns = [
        "id",
        "title",
        "description",
        "category",
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "brand",
        "thumbnail"
    ]

    df = df[required_columns].copy()

    # 2. Rename columns to match PostgreSQL table
    df = df.rename(columns={
          "discountPercentage": "discount_percentage"
    })

    # 3. Remove duplicate products
    df = df.drop_duplicates(subset=["id"], keep="last")

    # 4. Clean text columns
    text_columns = [
        "title",
        "description",
        "category",
        "brand",
        "thumbnail"
    ]

    for column in text_columns:
        df[column] = df[column].apply(
            lambda value: value.strip() if isinstance(value, str) else None
        )

    # 5. Convert numeric columns
    numeric_columns = [
        "id",
        "price",
        "discount_percentage",
        "rating",
        "stock"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # 6. Remove records with invalid essential fields
    df = df.dropna(subset=["id", "title", "price"])

    # 7. Ensure ID and stock are integers
    df = df[df["id"] > 0]
    df = df[df["stock"].isna() | (df["stock"] >= 0)]

    df["id"] = df["id"].astype(int)
    df["stock"] = df["stock"].astype("Int64")

    # 8. Remove invalid prices
    df = df[df["price"] >= 0]

    # 9. Reset index
    df = df.reset_index(drop=True)

    print("Data transformation completed!")
    print("Clean products:", len(df))

    return df


if __name__ == "__main__":

    # Extract raw data
    raw_data = extract_products()

    # Transform raw data
    clean_data = transform_products(raw_data)

    print("\nTransformed product data:")
    print(clean_data.head())

    print("\nData types:")
    print(clean_data.dtypes)
