import pandas as pd

from sklearn.preprocessing import StandardScaler

from backend.error_handler import handle_exception

from src.dbscan import (
    fit_dbscan,
    get_dbscan_labels,
    count_noise_points,
    get_k_distance,
)

from src.visualization import (
    plot_dbscan_clusters,
    plot_k_distance,
)


# ============================================================
# FEATURES USED FOR CLUSTERING
# ============================================================

FEATURE_COLUMNS = [
    "Annual Income (k$)",
    "Spending Score (1-100)",
]


# ============================================================
# SELECT FEATURES
# ============================================================

def select_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Select numerical features for clustering."""

    try:

        missing_features = (
            set(FEATURE_COLUMNS)
            - set(df.columns)
        )

        if missing_features:

            raise ValueError(
                f"Missing clustering features: "
                f"{missing_features}"
            )

        return df[
            FEATURE_COLUMNS
        ].copy()

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# SCALE FEATURES
# ============================================================

def scale_features(
    features: pd.DataFrame,
) -> tuple[pd.DataFrame, StandardScaler]:
    """Scale clustering features using StandardScaler."""

    try:

        scaler = StandardScaler()

        scaled_array = (
            scaler.fit_transform(features)
        )

        scaled_features = pd.DataFrame(
            scaled_array,
            columns=features.columns,
            index=features.index,
        )

        return (
            scaled_features,
            scaler,
        )

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    try:

        from src.data_load import (
            load_customer_data,
            validate_customer_data,
        )

        # ----------------------------------------------------
        # Load dataset
        # ----------------------------------------------------

        df = load_customer_data()

        # ----------------------------------------------------
        # Validate dataset
        # ----------------------------------------------------

        validate_customer_data(df)

        # ----------------------------------------------------
        # Select features
        # ----------------------------------------------------

        features = select_features(df)

        # ----------------------------------------------------
        # Scale features
        # ----------------------------------------------------

        scaled_features, scaler = (
            scale_features(features)
        )

        print("Original features:")

        print(
            features.head()
        )

        print("\nScaled features:")

        print(
            scaled_features.head()
        )

        print("\nScaled mean:")

        print(
            scaled_features.mean()
        )

        print(
            "\nScaled standard deviation:"
        )

        print(
            scaled_features.std()
        )

        # ----------------------------------------------------
        # K-distance
        # ----------------------------------------------------

        k_distances = get_k_distance(
            scaled_features=scaled_features,
            min_samples=5,
        )

        plot_k_distance(
            k_distances
        )

        # ----------------------------------------------------
        # DBSCAN
        # ----------------------------------------------------

        dbscan_model = fit_dbscan(
            scaled_features=scaled_features,
            eps=0.5,
            min_samples=5,
        )

        # ----------------------------------------------------
        # Get cluster labels
        # ----------------------------------------------------

        dbscan_labels = (
            get_dbscan_labels(
                dbscan_model
            )
        )

        # ----------------------------------------------------
        # Count noise points
        # ----------------------------------------------------

        noise_count = (
            count_noise_points(
                dbscan_labels
            )
        )

        # ----------------------------------------------------
        # Add results to customer dataframe
        # ----------------------------------------------------

        customer_results = df.copy()

        customer_results[
            "dbscan_cluster"
        ] = dbscan_labels

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        print("\nDBSCAN Results:")

        number_of_clusters = (
            len(set(dbscan_labels))
            - (
                1
                if -1 in dbscan_labels
                else 0
            )
        )

        print(
            f"Number of clusters: "
            f"{number_of_clusters}"
        )

        print(
            f"Noise points: "
            f"{noise_count}"
        )

        noise_percentage = (
            noise_count
            / len(dbscan_labels)
            * 100
        )

        print(
            f"Noise percentage: "
            f"{noise_percentage:.2f}%"
        )

        # ----------------------------------------------------
        # Visualization
        # ----------------------------------------------------

        plot_dbscan_clusters(
            customer_results
        )

    except Exception as error:

        handle_exception(error)

        raise