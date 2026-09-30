import pandas as pd

from backend.error_handler import handle_exception


# ============================================================
# ANALYZE DATASET
# ============================================================

def analyze_dataset(
    df: pd.DataFrame,
) -> dict:
    """
    Analyze an uploaded dataset and identify
    useful information for customer segmentation.
    """

    try:

        # --------------------------------------------------
        # Basic information
        # --------------------------------------------------

        total_rows = len(df)

        total_columns = len(
            df.columns
        )

        # --------------------------------------------------
        # Column types
        # --------------------------------------------------

        numeric_columns = (
            df.select_dtypes(
                include="number"
            )
            .columns
            .tolist()
        )

        categorical_columns = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool",
                ]
            )
            .columns
            .tolist()
        )

        # --------------------------------------------------
        # Missing values
        # --------------------------------------------------

        missing_values = (
            df.isnull()
            .sum()
            .to_dict()
        )

        total_missing = int(
            df.isnull()
            .sum()
            .sum()
        )

        # --------------------------------------------------
        # Duplicate rows
        # --------------------------------------------------

        duplicate_rows = int(
            df.duplicated().sum()
        )

        # --------------------------------------------------
        # Detect ID columns
        # --------------------------------------------------

        id_columns = []

        for column in df.columns:

            column_name = (
                column.lower()
            )

            if (
                "id" in column_name
                or (
                    "customer"
                    in column_name
                    and "number"
                    in column_name
                )
            ):
                id_columns.append(
                    column
                )

        # --------------------------------------------------
        # Detect useful business columns
        # --------------------------------------------------

        income_columns = []

        spending_columns = []

        age_columns = []

        frequency_columns = []

        for column in numeric_columns:

            column_name = (
                column.lower()
            )

            # Income-related columns
            if any(
                word in column_name
                for word in [
                    "income",
                    "salary",
                    "revenue",
                    "earning",
                ]
            ):
                income_columns.append(
                    column
                )

            # Spending-related columns
            if any(
                word in column_name
                for word in [
                    "spend",
                    "spending",
                    "purchase",
                    "amount",
                    "sales",
                    "revenue",
                ]
            ):
                spending_columns.append(
                    column
                )

            # Age-related columns
            if any(
                word in column_name
                for word in [
                    "age",
                ]
            ):
                age_columns.append(
                    column
                )

            # Frequency-related columns
            if any(
                word in column_name
                for word in [
                    "frequency",
                    "count",
                    "orders",
                    "visits",
                    "transactions",
                ]
            ):
                frequency_columns.append(
                    column
                )

        # --------------------------------------------------
        # Candidate clustering features
        # --------------------------------------------------

        excluded_columns = set(
            id_columns
        )

        candidate_features = [
            column
            for column in numeric_columns
            if column not in excluded_columns
        ]

        # --------------------------------------------------
        # Remove columns having only
        # one unique value
        # --------------------------------------------------

        candidate_features = [
            column
            for column in candidate_features
            if df[column].nunique(
                dropna=True
            ) > 1
        ]

        # --------------------------------------------------
        # Column information
        # --------------------------------------------------

        column_information = []

        for column in df.columns:

            column_information.append(
                {
                    "name": column,

                    "dtype": str(
                        df[column].dtype
                    ),

                    "missing": int(
                        df[column]
                        .isnull()
                        .sum()
                    ),

                    "unique_values": int(
                        df[column]
                        .nunique(
                            dropna=True
                        )
                    ),
                }
            )

        # --------------------------------------------------
        # Final result
        # --------------------------------------------------

        return {

            "rows": total_rows,

            "columns": total_columns,

            "numeric_columns":
                numeric_columns,

            "categorical_columns":
                categorical_columns,

            "id_columns":
                id_columns,

            "candidate_features":
                candidate_features,

            "income_columns":
                income_columns,

            "spending_columns":
                spending_columns,

            "age_columns":
                age_columns,

            "frequency_columns":
                frequency_columns,

            "missing_values":
                missing_values,

            "total_missing":
                total_missing,

            "duplicate_rows":
                duplicate_rows,

            "column_information":
                column_information,
        }

    except Exception as error:

        handle_exception(
            error
        )

        raise