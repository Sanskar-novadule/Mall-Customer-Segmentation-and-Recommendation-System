import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from backend.error_handler import handle_exception

from src.visualization import plot_customer_clusters
from src.profiling import create_cluster_profile


# ============================================================
# CALCULATE WCSS
# ============================================================

def calculate_wcss(
    scaled_features: pd.DataFrame,
    min_k: int = 2,
    max_k: int = 10,
) -> dict[int, float]:
    """Calculate WCSS for different numbers of clusters."""

    try:

        wcss = {}

        for k in range(
            min_k,
            max_k + 1,
        ):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10,
            )

            model.fit(
                scaled_features
            )

            wcss[k] = model.inertia_

        return wcss

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# PLOT ELBOW
# ============================================================

def plot_elbow(
    wcss: dict[int, float],
) -> None:
    """Plot the Elbow curve."""

    try:

        plt.figure(
            figsize=(8, 5)
        )

        plt.plot(
            list(wcss.keys()),
            list(wcss.values()),
            marker="o",
        )

        plt.xlabel(
            "Number of Clusters (K)"
        )

        plt.ylabel(
            "WCSS / Inertia"
        )

        plt.title(
            "Elbow Method for K-Means"
        )

        plt.xticks(
            list(wcss.keys())
        )

        plt.grid(True)

        plt.show()

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# FIT K-MEANS
# ============================================================

def fit_kmeans(
    scaled_features: pd.DataFrame,
    n_clusters: int,
) -> KMeans:
    """Train K-Means with the selected number of clusters."""

    try:

        model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
        )

        model.fit(
            scaled_features
        )

        return model

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

        from src.preprocessing import (
            select_features,
            scale_features,
        )

        # ----------------------------------------------------
        # 1. Load data
        # ----------------------------------------------------

        df = load_customer_data()

        # ----------------------------------------------------
        # 2. Validate data
        # ----------------------------------------------------

        validate_customer_data(
            df
        )

        # ----------------------------------------------------
        # 3. Select clustering features
        # ----------------------------------------------------

        features = select_features(
            df
        )

        # ----------------------------------------------------
        # 4. Scale features
        # ----------------------------------------------------

        scaled_features, scaler = (
            scale_features(
                features
            )
        )

        # ----------------------------------------------------
        # 5. Calculate WCSS
        # ----------------------------------------------------

        wcss = calculate_wcss(
            scaled_features
        )

        print(
            "WCSS values:"
        )

        for k, value in wcss.items():

            print(
                f"K={k}: {value:.2f}"
            )

        # ----------------------------------------------------
        # 6. Show Elbow graph
        # ----------------------------------------------------

        plot_elbow(
            wcss
        )

        # ----------------------------------------------------
        # 7. Select candidate K
        # ----------------------------------------------------

        SELECTED_K = 5

        # ----------------------------------------------------
        # 8. Train final K-Means
        # ----------------------------------------------------

        model = fit_kmeans(
            scaled_features,
            n_clusters=SELECTED_K,
        )

        # ----------------------------------------------------
        # 9. Get cluster labels
        # ----------------------------------------------------

        labels = model.labels_

        # ----------------------------------------------------
        # 10. Add labels to original data
        # ----------------------------------------------------

        df["cluster"] = labels

        # ----------------------------------------------------
        # 11. Create cluster profile
        # ----------------------------------------------------

        cluster_profile = (
            create_cluster_profile(df)
        )

        print(
            "\nCluster Profile:"
        )

        print(
            cluster_profile.to_string(
                index=False
            )
        )

        # ----------------------------------------------------
        # 12. Plot customer clusters
        # ----------------------------------------------------

        plot_customer_clusters(
            df
        )

        # ----------------------------------------------------
        # 13. Create cluster summary
        # ----------------------------------------------------

        cluster_summary = (
            df.groupby("cluster")[
                [
                    "Annual Income (k$)",
                    "Spending Score (1-100)",
                ]
            ]
            .mean()
        )

        # ----------------------------------------------------
        # 14. Print cluster summary
        # ----------------------------------------------------

        print(
            "\nCluster Summary:"
        )

        print(
            cluster_summary
        )

        # ----------------------------------------------------
        # 15. Customer count per cluster
        # ----------------------------------------------------

        print(
            "\nCustomer Cluster Counts:"
        )

        print(
            df["cluster"]
            .value_counts()
            .sort_index()
        )

    except Exception as error:

        handle_exception(error)

        raise