import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_customer_clusters(
    df: pd.DataFrame,
) -> None:
    """Plot customers grouped by K-Means cluster."""

    plt.figure(figsize=(10, 6))

    for cluster in sorted(df["cluster"].unique()):

        cluster_data = df[df["cluster"] == cluster]

        plt.scatter(
            cluster_data["Annual Income (k$)"],
            cluster_data["Spending Score (1-100)"],
            label=f"Cluster {cluster}",
        )

    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.title("Customer Segmentation using K-Means")

    plt.legend()
    plt.grid(True)

    plt.show()


def plot_k_distance(
    k_distances: np.ndarray,
) -> None:
    """Plot the k-distance graph for DBSCAN eps selection."""

    plt.figure(figsize=(8, 5))

    plt.plot(k_distances)

    plt.xlabel("Data Points sorted by distance")
    plt.ylabel("5th Nearest Neighbor Distance")
    plt.title("DBSCAN K-Distance Graph")

    plt.grid(True)

    plt.show()


def plot_dbscan_clusters(
    df: pd.DataFrame,
) -> None:
    """Plot customers grouped by DBSCAN cluster."""

    plt.figure(figsize=(10, 6))

    for cluster in sorted(df["dbscan_cluster"].unique()):

        cluster_data = df[df["dbscan_cluster"] == cluster]

        if cluster == -1:
            plt.scatter(
                cluster_data["Annual Income (k$)"],
                cluster_data["Spending Score (1-100)"],
                label="Noise / Outliers",
                marker="x",
            )
        else:
            plt.scatter(
                cluster_data["Annual Income (k$)"],
                cluster_data["Spending Score (1-100)"],
                label=f"Cluster {cluster}",
            )

    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.title("Customer Segmentation using DBSCAN")

    plt.legend()
    plt.grid(True)

    plt.show()