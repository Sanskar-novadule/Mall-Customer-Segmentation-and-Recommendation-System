import pandas as pd

from data_load import (
    load_customer_data,
    validate_customer_data,
)

from preprocessing import (
    select_features,
    scale_features,
)

from clustering import (
    fit_kmeans,
)

from dbscan import (
    fit_dbscan,
    get_dbscan_labels,
    count_noise_points,
)

from evaluation import (
    evaluate_clustering,
)

from comparision import (
    evaluate_dbscan,
    create_comparison_table,
    print_comparison,
)

from profiling import (
    create_cluster_profile,
)

from visualization import (
    plot_customer_clusters,
    plot_dbscan_clusters,
)


def main() -> None:
    """Run the complete customer segmentation pipeline."""

    # --------------------------------------------------
    # 1. Load Dataset
    # --------------------------------------------------

    df = load_customer_data()

    validate_customer_data(df)

    print("===== CUSTOMER SEGMENTATION SYSTEM =====")
    print(f"Total customers: {len(df)}")

    # --------------------------------------------------
    # 2. Select and Scale Features
    # --------------------------------------------------

    features = select_features(df)

    scaled_features, scaler = scale_features(
        features
    )

    print("\nFeatures selected:")
    print(features.columns.tolist())

    # --------------------------------------------------
    # 3. K-Means Clustering
    # --------------------------------------------------

    kmeans_model = fit_kmeans(
        scaled_features=scaled_features,
        n_clusters=5,
    )

    kmeans_labels = pd.Series(
        kmeans_model.labels_,
        index=df.index,
        name="cluster",
    )

    df["cluster"] = kmeans_labels

    # --------------------------------------------------
    # 4. K-Means Evaluation
    # --------------------------------------------------

    kmeans_metrics = evaluate_clustering(
        scaled_features=scaled_features,
        labels=kmeans_labels,
    )

    print("\n===== K-MEANS RESULTS =====")

    print(
        f"Number of clusters: "
        f"{kmeans_labels.nunique()}"
    )

    for metric, value in kmeans_metrics.items():
        print(
            f"{metric}: {value:.4f}"
        )

    # --------------------------------------------------
    # 5. Cluster Profiling
    # --------------------------------------------------

    cluster_profile = create_cluster_profile(
        df,
        cluster_column="cluster",
    )

    print("\n===== K-MEANS CLUSTER PROFILE =====")

    print(
        cluster_profile.to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # 6. Add Segment Information
    # --------------------------------------------------

    segment_mapping = (
        cluster_profile
        .set_index("cluster")["segment"]
        .to_dict()
    )

    product_mapping = (
        cluster_profile
        .set_index("cluster")["product_strategy"]
        .to_dict()
    )

    marketing_mapping = (
        cluster_profile
        .set_index("cluster")["marketing_strategy"]
        .to_dict()
    )

    action_mapping = (
        cluster_profile
        .set_index("cluster")["customer_action"]
        .to_dict()
    )

    df["segment"] = df["cluster"].map(
        segment_mapping
    )

    df["product_strategy"] = df["cluster"].map(
        product_mapping
    )

    df["marketing_strategy"] = df["cluster"].map(
        marketing_mapping
    )

    df["customer_action"] = df["cluster"].map(
        action_mapping
    )

    # --------------------------------------------------
    # 7. Save Customer-Level Results
    # --------------------------------------------------

    output_path = (
        "data/customer_segments.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        "\nCustomer-level results saved to:"
    )

    print(output_path)

        # --------------------------------------------------
    # 6.1 Customer Segment Table
    # --------------------------------------------------

    print("\n===== CUSTOMER SEGMENT TABLE =====")

    customer_table = df[
        [
            "CustomerID",
            "Genre",
            "Age",
            "Annual Income (k$)",
            "Spending Score (1-100)",
            "cluster",
            "segment",
            "product_strategy",
            "marketing_strategy",
            "customer_action",
        ]
    ]

    print(
        customer_table.to_string(
            index=False
        )
    )

        # --------------------------------------------------
    # 6.2 Business Recommendations
    # --------------------------------------------------

    print("\n===== BUSINESS RECOMMENDATIONS =====")

    for _, row in cluster_profile.iterrows():

        print(
            f"\nCluster {row['cluster']}"
        )

        print(
            f"Segment: "
            f"{row['segment']}"
        )

        print(
            f"Product Strategy: "
            f"{row['product_strategy']}"
        )

        print(
            f"Marketing Strategy: "
            f"{row['marketing_strategy']}"
        )

        print(
            f"Customer Action: "
            f"{row['customer_action']}"
        )
    # --------------------------------------------------
    # 8. K-Means Visualization
    # --------------------------------------------------

    print(
        "\nOpening K-Means cluster visualization..."
    )

    plot_customer_clusters(
        df
    )

    # --------------------------------------------------
    # 9. DBSCAN Clustering
    # --------------------------------------------------

    dbscan_model = fit_dbscan(
        scaled_features=scaled_features,
        eps=0.5,
        min_samples=5,
    )

    dbscan_labels = get_dbscan_labels(
        dbscan_model
    )

    noise_count = count_noise_points(
        dbscan_labels
    )

    number_of_dbscan_clusters = (
        len(set(dbscan_labels))
        - (
            1
            if -1 in dbscan_labels.values
            else 0
        )
    )

    print("\n===== DBSCAN RESULTS =====")

    print(
        f"Number of clusters: "
        f"{number_of_dbscan_clusters}"
    )

    print(
        f"Noise points: "
        f"{noise_count}"
    )

    print(
        f"Noise percentage: "
        f"{(noise_count / len(dbscan_labels)) * 100:.2f}%"
    )

    # --------------------------------------------------
    # 10. Add DBSCAN Labels
    # --------------------------------------------------

    df["dbscan_cluster"] = dbscan_labels

    # --------------------------------------------------
    # 11. DBSCAN Visualization
    # --------------------------------------------------

    print(
        "\nOpening DBSCAN cluster visualization..."
    )

    plot_dbscan_clusters(
        df
    )

    # --------------------------------------------------
    # 12. DBSCAN Evaluation
    # --------------------------------------------------

    dbscan_metrics = evaluate_dbscan(
        scaled_features=scaled_features,
        labels=dbscan_labels,
    )

    # --------------------------------------------------
    # 13. K-Means vs DBSCAN Comparison
    # --------------------------------------------------

    comparison = create_comparison_table(
        kmeans_metrics=kmeans_metrics,
        dbscan_metrics=dbscan_metrics,
    )

    print_comparison(
        comparison
    )

    # --------------------------------------------------
    # 14. Final Summary
    # --------------------------------------------------

    print("\n===== FINAL SUMMARY =====")

    print(
        f"K-Means clusters: "
        f"{kmeans_labels.nunique()}"
    )

    print(
        f"DBSCAN clusters: "
        f"{number_of_dbscan_clusters}"
    )

    print(
        f"DBSCAN noise points: "
        f"{noise_count}"
    )

    print(
        f"Customer results file: "
        f"{output_path}"
    )

    print(
        "\nCustomer segmentation pipeline completed successfully."
    )


if __name__ == "__main__":
    main()