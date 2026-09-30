import pandas as pd

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

from backend.error_handler import handle_exception


# ============================================================
# EVALUATE DBSCAN
# ============================================================

def evaluate_dbscan(
    scaled_features: pd.DataFrame,
    labels: pd.Series,
) -> dict[str, float]:
    """Evaluate DBSCAN clustering while ignoring noise points."""

    try:

        # ----------------------------------------------------
        # DBSCAN uses -1 for noise/outlier points
        # ----------------------------------------------------

        non_noise_mask = labels != -1

        filtered_features = (
            scaled_features[non_noise_mask]
        )

        filtered_labels = (
            labels[non_noise_mask]
        )

        # ----------------------------------------------------
        # Count clusters
        # ----------------------------------------------------

        number_of_clusters = (
            filtered_labels.nunique()
        )

        # ----------------------------------------------------
        # Metrics require at least 2 clusters
        # ----------------------------------------------------

        if number_of_clusters < 2:

            return {
                "silhouette_score": float("nan"),
                "davies_bouldin_index": float("nan"),
                "calinski_harabasz_index": float("nan"),
            }

        # ----------------------------------------------------
        # Calculate clustering metrics
        # ----------------------------------------------------

        return {
            "silhouette_score": float(
                silhouette_score(
                    filtered_features,
                    filtered_labels,
                )
            ),

            "davies_bouldin_index": float(
                davies_bouldin_score(
                    filtered_features,
                    filtered_labels,
                )
            ),

            "calinski_harabasz_index": float(
                calinski_harabasz_score(
                    filtered_features,
                    filtered_labels,
                )
            ),
        }

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# CREATE COMPARISON TABLE
# ============================================================

def create_comparison_table(
    kmeans_metrics: dict[str, float],
    dbscan_metrics: dict[str, float],
) -> pd.DataFrame:
    """Create K-Means vs DBSCAN comparison table."""

    try:

        comparison = pd.DataFrame(
            {
                "K-Means": kmeans_metrics,
                "DBSCAN": dbscan_metrics,
            }
        )

        return comparison

    except Exception as error:

        handle_exception(error)

        raise


# ============================================================
# PRINT COMPARISON
# ============================================================

def print_comparison(
    comparison: pd.DataFrame,
) -> None:
    """Print clustering algorithm comparison."""

    try:

        print(
            "\n===== K-Means vs DBSCAN Comparison ====="
        )

        print(
            comparison
        )

    except Exception as error:

        handle_exception(error)

        raise