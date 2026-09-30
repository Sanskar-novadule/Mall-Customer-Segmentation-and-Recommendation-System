import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


def select_best_features(
    df: pd.DataFrame,
    numeric_features: list[str],
    categorical_features: list[str],
):
    """
    Automatically select useful features for clustering.
    """

    # -----------------------------------------
    # 1. Remove ID-like numeric columns
    # -----------------------------------------

    selected_numeric = []

    for column in numeric_features:

        # Skip columns with unique value for every row
        if df[column].nunique() == len(df):
            continue

        # Skip columns with extremely high uniqueness
        uniqueness_ratio = (
            df[column].nunique() / len(df)
        )

        if uniqueness_ratio > 0.95:
            continue

        selected_numeric.append(column)

    # -----------------------------------------
    # 2. Remove useless constant columns
    # -----------------------------------------

    selected_numeric = [
        column
        for column in selected_numeric
        if df[column].nunique() > 1
    ]

    # -----------------------------------------
    # 3. Prepare numeric data
    # -----------------------------------------

    if not selected_numeric:
        raise ValueError(
            "No suitable numeric features found."
        )

    features = df[selected_numeric].copy()

    for column in features.columns:
        features[column] = pd.to_numeric(
            features[column],
            errors="coerce",
        )

    features = features.replace(
        [float("inf"), float("-inf")],
        pd.NA,
    )

    features = features.fillna(
        features.median()
    )

    # -----------------------------------------
    # 4. Scale features
    # -----------------------------------------

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        features
    )

    # -----------------------------------------
    # 5. Find best feature combination
    # -----------------------------------------

    best_features = selected_numeric.copy()
    best_score = -1
    best_k = None

    # Try different feature combinations
    # when dataset has manageable number of features

    if len(selected_numeric) <= 8:

        from itertools import combinations

        combinations_list = []

        for r in range(
            2,
            len(selected_numeric) + 1,
        ):
            combinations_list.extend(
                combinations(
                    selected_numeric,
                    r,
                )
            )

        for feature_combination in combinations_list:

            combination_df = features[
                list(feature_combination)
            ]

            combination_scaled = scaler.fit_transform(
                combination_df
            )

            max_k = min(
                8,
                len(df) - 1,
            )

            for k in range(2, max_k + 1):

                model = KMeans(
                    n_clusters=k,
                    random_state=42,
                    n_init=10,
                )

                labels = model.fit_predict(
                    combination_scaled
                )

                score = silhouette_score(
                    combination_scaled,
                    labels,
                )

                if score > best_score:

                    best_score = float(score)

                    best_features = list(
                        feature_combination
                    )

                    best_k = k

    else:

        # For high-dimensional datasets,
        # avoid testing every combination.

        best_features = selected_numeric

        model = KMeans(
            n_clusters=2,
            random_state=42,
            n_init=10,
        )

        labels = model.fit_predict(
            scaled_features
        )

        best_score = float(
            silhouette_score(
                scaled_features,
                labels,
            )
        )

        best_k = 2

    # -----------------------------------------
    # 6. Detect useful categorical columns
    # -----------------------------------------

    best_categorical = []

    for column in categorical_features:

        unique_count = df[column].nunique()

        # Ignore extremely high-cardinality text
        if unique_count <= 20:

            if unique_count > 1:
                best_categorical.append(column)

    # -----------------------------------------
    # 7. Return result
    # -----------------------------------------

    return {
        "best_numeric_features": best_features,
        "best_categorical_features": best_categorical,
        "best_k": best_k,
        "best_silhouette_score": best_score,
    }