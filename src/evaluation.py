import pandas as pd

from sklearn.cluster import KMeans

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

from backend.error_handler import handle_exception

from src.dbscan import get_k_distance
from src.visualization import plot_k_distance


# ============================================================
# SILHOUETTE SCORE
# ============================================================

def calculate_silhouette_score(
    scaled_features: pd.DataFrame,
    labels,
) -> float:
    """Calculate the Silhouette Score."""

    try:

        return float(
            silhouette_score(
                scaled_features,
                labels,
            )
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# DAVIES-BOULDIN SCORE
# ============================================================

def calculate_davies_bouldin_score(
    scaled_features: pd.DataFrame,
    labels,
) -> float:
    """Calculate the Davies-Bouldin Index."""

    try:

        return float(
            davies_bouldin_score(
                scaled_features,
                labels,
            )
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# CALINSKI-HARABASZ SCORE
# ============================================================

def calculate_calinski_harabasz_score(
    scaled_features: pd.DataFrame,
    labels,
) -> float:
    """Calculate the Calinski-Harabasz Index."""

    try:

        return float(
            calinski_harabasz_score(
                scaled_features,
                labels,
            )
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# EVALUATE CLUSTERING
# ============================================================

def evaluate_clustering(
    scaled_features: pd.DataFrame,
    labels,
) -> dict[str, float]:
    """Calculate all clustering evaluation metrics."""

    try:

        return {
            "silhouette_score":
                calculate_silhouette_score(
                    scaled_features,
                    labels,
                ),

            "davies_bouldin_index":
                calculate_davies_bouldin_score(
                    scaled_features,
                    labels,
                ),

            "calinski_harabasz_index":
                calculate_calinski_harabasz_score(
                    scaled_features,
                    labels,
                ),
        }

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# EVALUATE DIFFERENT K VALUES
# ============================================================

def evaluate_k_values(
    scaled_features: pd.DataFrame,
    min_k: int = 2,
    max_k: int = 10,
) -> pd.DataFrame:
    """Evaluate K-Means for different values of K."""

    try:

        results = []

        for k in range(
            min_k,
            max_k + 1,
        ):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10,
            )

            labels = model.fit_predict(
                scaled_features
            )

            silhouette = (
                calculate_silhouette_score(
                    scaled_features,
                    labels,
                )
            )

            davies_bouldin = (
                calculate_davies_bouldin_score(
                    scaled_features,
                    labels,
                )
            )

            calinski_harabasz = (
                calculate_calinski_harabasz_score(
                    scaled_features,
                    labels,
                )
            )

            results.append(
                {
                    "k": k,

                    "silhouette_score":
                        silhouette,

                    "davies_bouldin_index":
                        davies_bouldin,

                    "calinski_harabasz_index":
                        calinski_harabasz,
                }
            )

        return pd.DataFrame(
            results
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# EVALUATE DBSCAN EPS
# ============================================================

def evaluate_dbscan_eps(
    scaled_features: pd.DataFrame,
):
    """Generate the k-distance graph for DBSCAN eps selection."""

    try:

        k_distances = get_k_distance(
            scaled_features=scaled_features,
            min_samples=5,
        )

        plot_k_distance(
            k_distances
        )

        return k_distances

    except Exception as error:

        handle_exception(
            error
        )

        raise