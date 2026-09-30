from pathlib import Path

import pandas as pd

from backend.error_handler import handle_exception


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# DATASET PATH
# ============================================================

DATA_PATH = (
    BASE_DIR
    / "data"
    / "Mall_Customers.csv"
)


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

def load_customer_data() -> pd.DataFrame:
    """Load the customer dataset."""

    try:

        if not DATA_PATH.exists():

            raise FileNotFoundError(
                f"Dataset not found: {DATA_PATH}"
            )

        return pd.read_csv(DATA_PATH)

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# VALIDATE CUSTOMER DATA
# ============================================================

def validate_customer_data(
    df: pd.DataFrame,
) -> None:
    """Validate the basic structure of the dataset."""

    try:

        required_columns = {
            "CustomerID",
            "Genre",
            "Age",
            "Annual Income (k$)",
            "Spending Score (1-100)",
        }

        missing_columns = (
            required_columns
            - set(df.columns)
        )

        if missing_columns:

            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        if df.empty:

            raise ValueError(
                "Dataset is empty."
            )

        if df.isnull().sum().sum() > 0:

            raise ValueError(
                "Dataset contains missing values."
            )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    try:

        df = load_customer_data()

        validate_customer_data(
            df
        )

        print(
            "Dataset loaded successfully."
        )

        print(
            f"Shape: {df.shape}"
        )

        print("\nColumns:")

        print(
            df.columns.tolist()
        )

        print("\nMissing values:")

        print(
            df.isnull().sum()
        )

        print("\nFirst 5 rows:")

        print(
            df.head()
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise