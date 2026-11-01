
import requests
import pandas as pd

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    """
    Create an HTTP session with automatic retry logic.
    """

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def extract_products():
    """
    Extract all products using pagination and automatic retries.
    """

    url = "https://dummyjson.com/products"

    all_products = []
    limit = 30
    skip = 0

    try:
        with create_session() as session:

            while True:

                params = {
                    "limit": limit,
                    "skip": skip
                }

                response = session.get(
                    url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                products = data.get("products", [])

                all_products.extend(products)

                total = data.get("total", 0)

                print(
                    f"Fetched {len(products)} products. "
                    f"Total collected: {len(all_products)}"
                )

                if not products or len(all_products) >= total:
                    break

                skip += limit

        df = pd.DataFrame(all_products)

        print("\nData extraction completed!")
        print("Total products extracted:", len(df))

        return df

    except requests.exceptions.RequestException as error:

        print("API extraction failed after retries:", error)

        return pd.DataFrame()


if __name__ == "__main__":

    products_df = extract_products()

    print("\nFirst 5 products:")
    print(products_df.head())
