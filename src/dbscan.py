import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

from backend.error_handler import handle_exception


# ============================================================
# FIT DBSCAN
# ============================================================

def fit_dbscan(
    scaled_features: pd.DataFrame,
    eps: float = 0.5,
    min_samples: int = 5,
) -> DBSCAN:
    """Train a DBSCAN clustering model."""

    try:

        model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
        )

        model.fit(
            scaled_features
        )

        return model

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# GET DBSCAN LABELS
# ============================================================

def get_dbscan_labels(
    model: DBSCAN,
) -> pd.Series:
    """Return DBSCAN cluster labels."""

    try:

        return pd.Series(
            model.labels_,
            name="dbscan_cluster",
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# COUNT NOISE POINTS
# ============================================================

def count_noise_points(
    labels: pd.Series,
) -> int:
    """Count DBSCAN noise points."""

    try:

        return int(
            (labels == -1).sum()
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise


# ============================================================
# K-DISTANCE
# ============================================================

def get_k_distance(
    scaled_features: pd.DataFrame,
    min_samples: int = 5,
) -> np.ndarray:
    """Calculate k-nearest-neighbor distances for DBSCAN."""

    try:

        neighbors = NearestNeighbors(
            n_neighbors=min_samples
        )

        neighbors.fit(
            scaled_features
        )

        distances, _ = (
            neighbors.kneighbors(
                scaled_features
            )
        )

        k_distances = (
            distances[:, -1]
        )

        return np.sort(
            k_distances
        )

    except Exception as error:

        handle_exception(
            error
        )

        raise