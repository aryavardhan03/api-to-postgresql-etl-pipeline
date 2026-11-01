
import pandas as pd

from src.transform import transform_products


def sample_products():

    return pd.DataFrame({
        "id": [1, 2, 2, 3],
        "title": ["Laptop", "Phone", "Phone Updated", None],
        "description": ["Laptop description", "Phone description",
                        "Updated phone description", "Tablet description"],
        "category": ["electronics", "electronics",
                     "electronics", "electronics"],
        "price": [1000, 500, 550, 300],
        "discountPercentage": [10, 5, 8, 0],
        "rating": [4.5, 4.2, 4.4, 4.0],
        "stock": [10, 20, 15, 5],
        "brand": ["Brand A", "Brand B", "Brand B", "Brand C"],
        "thumbnail": ["image1.jpg", "image2.jpg",
                      "image2.jpg", "image3.jpg"]
    })


def test_duplicate_products_are_removed():

    df = sample_products()

    result = transform_products(df)

    assert result["id"].is_unique


def test_missing_titles_are_removed():

    df = sample_products()

    result = transform_products(df)

    assert result["title"].notna().all()


def test_negative_prices_are_removed():

    df = sample_products()
    df.loc[0, "price"] = -100

    result = transform_products(df)

    assert (result["price"] >= 0).all()


def test_empty_dataframe():

    df = pd.DataFrame()

    result = transform_products(df)

    assert result.empty
    

def test_invalid_product_ids_are_removed():

    df = sample_products()
    df.loc[0, "id"] = -1

    result = transform_products(df)

    assert (result["id"] > 0).all()


def test_whitespace_is_removed():

    df = sample_products()
    df.loc[0, "title"] = "  Laptop  "

    result = transform_products(df)

    assert "Laptop" in result["title"].values


def test_discount_column_is_renamed():

    df = sample_products()

    result = transform_products(df)

    assert "discount_percentage" in result.columns
    assert "discountPercentage" not in result.columns

