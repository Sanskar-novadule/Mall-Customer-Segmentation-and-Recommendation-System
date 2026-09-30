import pandas as pd

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
)

from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from .automatic_feature_selection import (
    select_best_features,
)

from backend.error_handler import handle_exception


# ============================================================
# 1. DETECT USEFUL COLUMNS
# ============================================================

def detect_feature_types(
    df: pd.DataFrame,
):
    """
    Automatically detect numeric and categorical columns.
    """

    try:

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=[
                "object",
                "category",
                "bool",
            ]
        ).columns.tolist()

        id_columns = []

        for column in df.columns:

            column_lower = column.lower()

            unique_ratio = (
                df[column].nunique(
                    dropna=False
                )
                / max(len(df), 1)
            )

            # --------------------------------------------
            # Name-based ID detection
            # --------------------------------------------

            if (
                column_lower == "id"
                or column_lower.endswith("_id")
                or column_lower.endswith(" id")
                or "customerid" in column_lower
                or "customer id" in column_lower
            ):

                id_columns.append(
                    column
                )

                continue

            # --------------------------------------------
            # High-cardinality numeric columns
            # --------------------------------------------

            if (
                column in numeric_columns
                and unique_ratio > 0.95
            ):

                id_columns.append(
                    column
                )

        # --------------------------------------------
        # Remove ID columns
        # --------------------------------------------

        numeric_features = [
            column
            for column in numeric_columns
            if column not in id_columns
        ]

        categorical_features = [
            column
            for column in categorical_columns
            if column not in id_columns
        ]

        # --------------------------------------------
        # Remove high-cardinality categoricals
        # --------------------------------------------

        useful_categorical = []

        for column in categorical_features:

            unique_count = df[column].nunique(
                dropna=True
            )

            if (
                unique_count <= 50
                and unique_count < len(df) * 0.5
            ):

                useful_categorical.append(
                    column
                )

        return (
            numeric_features,
            useful_categorical,
            id_columns,
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# 2. PREPARE FEATURES
# ============================================================

def prepare_features(
    df: pd.DataFrame,
    numeric_features: list[str],
    categorical_features: list[str],
):
    """
    Prepare selected features for clustering.
    """

    try:

        numeric_df = df[
            numeric_features
        ].copy()

        categorical_df = df[
            categorical_features
        ].copy()

        # --------------------------------------------
        # Numeric cleaning
        # --------------------------------------------

        if not numeric_df.empty:

            numeric_df = numeric_df.replace(
                [
                    float("inf"),
                    float("-inf"),
                ],
                pd.NA,
            )

            for column in numeric_df.columns:

                numeric_df[column] = pd.to_numeric(
                    numeric_df[column],
                    errors="coerce",
                )

            numeric_df = numeric_df.fillna(
                numeric_df.median()
            )

        # --------------------------------------------
        # Categorical cleaning
        # --------------------------------------------

        if not categorical_df.empty:

            categorical_df = (
                categorical_df
                .fillna("Unknown")
                .astype(str)
            )

        # --------------------------------------------
        # Combine cleaned data
        # --------------------------------------------

        cleaned_df = df.copy()

        for column in numeric_df.columns:

            cleaned_df[column] = (
                numeric_df[column]
            )

        for column in categorical_df.columns:

            cleaned_df[column] = (
                categorical_df[column]
            )

        # --------------------------------------------
        # Build transformer
        # --------------------------------------------

        transformers = []

        if numeric_features:

            transformers.append(
                (
                    "numeric",
                    StandardScaler(),
                    numeric_features,
                )
            )

        if categorical_features:

            transformers.append(
                (
                    "categorical",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False,
                    ),
                    categorical_features,
                )
            )

        if not transformers:

            raise ValueError(
                "No suitable features found for clustering."
            )

        # --------------------------------------------
        # Column Transformer
        # --------------------------------------------

        preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder="drop",
        )

        scaled_features = (
            preprocessor.fit_transform(
                cleaned_df
            )
        )

        return (
            scaled_features,
            preprocessor,
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# 3. FIND BEST K
# ============================================================

def find_best_k(
    scaled_features,
    min_k: int = 2,
    max_k: int = 8,
):
    """
    Automatically select K using silhouette score.
    """

    try:

        number_of_samples = len(
            scaled_features
        )

        max_allowed_k = min(
            max_k,
            number_of_samples - 1,
        )

        if max_allowed_k < min_k:

            raise ValueError(
                "Dataset does not contain enough rows "
                "for clustering."
            )

        scores = {}

        best_k = None
        best_score = -1

        for k in range(
            min_k,
            max_allowed_k + 1,
        ):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10,
            )

            labels = model.fit_predict(
                scaled_features
            )

            score = silhouette_score(
                scaled_features,
                labels,
            )

            scores[k] = float(
                score
            )

            if score > best_score:

                best_score = score
                best_k = k

        return (
            best_k,
            best_score,
            scores,
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# 4. RUN K-MEANS
# ============================================================

def run_kmeans(
    scaled_features,
    n_clusters: int,
):
    """
    Run final K-Means model.
    """

    try:

        model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
        )

        labels = model.fit_predict(
            scaled_features
        )

        return (
            model,
            labels,
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# 5. COMPLETE AUTOMATIC SEGMENTATION
# ============================================================

def run_generic_segmentation(
    df: pd.DataFrame,
):
    """
    Fully automatic segmentation pipeline.

    Automatically:

    1. Detects feature types
    2. Removes ID columns
    3. Selects useful features
    4. Finds best K
    5. Runs K-Means
    6. Returns clustered dataset
    """

    try:

        # --------------------------------------------
        # Step 1: Detect feature types
        # --------------------------------------------

        (
            numeric_features,
            categorical_features,
            id_columns,
        ) = detect_feature_types(
            df
        )

        # --------------------------------------------
        # Step 2: Automatic feature selection
        # --------------------------------------------

        feature_selection = (
            select_best_features(
                df=df,
                numeric_features=numeric_features,
                categorical_features=(
                    categorical_features
                ),
            )
        )

        selected_numeric_features = (
            feature_selection[
                "best_numeric_features"
            ]
        )

        selected_categorical_features = (
            feature_selection[
                "best_categorical_features"
            ]
        )

        # --------------------------------------------
        # Step 3: Prepare selected features
        # --------------------------------------------

        (
            scaled_features,
            preprocessor,
        ) = prepare_features(
            df=df,
            numeric_features=(
                selected_numeric_features
            ),
            categorical_features=(
                selected_categorical_features
            ),
        )

        # --------------------------------------------
        # Step 4: Find best K
        # --------------------------------------------

        (
            best_k,
            best_score,
            all_scores,
        ) = find_best_k(
            scaled_features
        )

        # --------------------------------------------
        # Step 5: Final K-Means
        # --------------------------------------------

        (
            model,
            labels,
        ) = run_kmeans(
            scaled_features,
            best_k,
        )

        # --------------------------------------------
        # Step 6: Add cluster
        # --------------------------------------------

        result_df = df.copy()

        result_df["cluster"] = labels

        # --------------------------------------------
        # Step 7: Return everything
        # --------------------------------------------

        return {

            "data": result_df,

            "numeric_features":
                numeric_features,

            "categorical_features":
                categorical_features,

            "selected_numeric_features":
                selected_numeric_features,

            "selected_categorical_features":
                selected_categorical_features,

            "id_columns":
                id_columns,

            "features_used": (
                selected_numeric_features
                + selected_categorical_features
            ),

            "scaled_features":
                scaled_features,

            "preprocessor":
                preprocessor,

            "model":
                model,

            "best_k":
                best_k,

            "best_silhouette_score":
                best_score,

            "all_k_scores":
                all_scores,
        }

    except Exception as error:

        handle_exception(
            error
        )

        raise