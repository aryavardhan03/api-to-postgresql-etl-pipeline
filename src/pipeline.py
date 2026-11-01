
import logging
import os

from .extract import extract_products
from .transform import transform_products
from .load import load_products

# Create logs directory if it does not exist
os.makedirs("logs", exist_ok=True)

# Configure logging to save messages in a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/etl_pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


def run_pipeline():

    try:
        logger.info("ETL pipeline started")

        # STEP 1: Extract
        logger.info("Starting data extraction")
        raw_data = extract_products()

        if raw_data.empty:
            logger.warning("No data extracted. Pipeline stopped.")
            return

        # STEP 2: Transform
        logger.info("Starting data transformation")
        clean_data = transform_products(raw_data)

        if clean_data.empty:
            logger.warning("No valid data after transformation.")
            return

        # STEP 3: Load
        logger.info("Starting data loading")
        load_products(clean_data)

        logger.info("ETL pipeline completed successfully")

    except Exception:
        logger.exception("ETL pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()
