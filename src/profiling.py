import pandas as pd
from backend.error_handler import handle_exception
import logging
import traceback

from backend.database import save_error_to_database
from src.recommendations import get_recommendation

try:
    def calculate_overall_averages(
        df: pd.DataFrame,
    ) -> tuple[float, float]:
        """Calculate overall income and spending averages."""

        average_income = float(
            df["Annual Income (k$)"].mean()
        )

        average_spending = float(
            df["Spending Score (1-100)"].mean()
        )

        return average_income, average_spending
except Exception as error:
        handle_exception(error)
        raise

def classify_segment(
    average_income: float,
    average_spending: float,
    overall_income: float,
    overall_spending: float,
) -> str:
    """Assign a business segment based on income and spending."""

    high_income = average_income >= overall_income
    high_spending = average_spending >= overall_spending

    if high_income and high_spending:
        return "Premium Customers"

    if high_income and not high_spending:
        return "Potential Customers"

    if not high_income and high_spending:
        return "Value-Seeking Customers"

    return "Budget Customers"


def create_cluster_profile(
    df: pd.DataFrame,
    cluster_column: str = "cluster",
    exclude_noise: bool = False,
) -> pd.DataFrame:
    """Create a business profile for each customer cluster."""

    profile_df = df.copy()

    if exclude_noise:
        profile_df = profile_df[
            profile_df[cluster_column] != -1
        ]

    profile = (
        profile_df
        .groupby(cluster_column)
        .agg(
            customer_count=("CustomerID", "count"),
            average_income=("Annual Income (k$)", "mean"),
            average_spending=("Spending Score (1-100)", "mean"),
        )
        .reset_index()
    )

    overall_income, overall_spending = (
        calculate_overall_averages(profile_df)
    )

    profile["segment"] = profile.apply(
        lambda row: classify_segment(
            row["average_income"],
            row["average_spending"],
            overall_income,
            overall_spending,
        ),
        axis=1,
    )

    profile[
        [
            "product_strategy",
            "marketing_strategy",
            "customer_action",
        ]
    ] = profile["segment"].apply(
        lambda segment: pd.Series(
            get_recommendation(segment)
        )
    )

    return profile