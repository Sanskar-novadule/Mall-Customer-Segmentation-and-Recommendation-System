# import pandas as pd


# def create_cluster_profile(df, cluster_column="KMeans_Cluster"):
#     """
#     Create a summary/profile of each customer cluster.
#     """

#     profile = (
#         df.groupby(cluster_column)
#         .agg(
#             Customer_Count=("CustomerID", "count"),
#             Average_Income=("Annual Income (k$)", "mean"),
#             Average_Spending=("Spending Score (1-100)", "mean"),
#         )
#         .reset_index()
#     )

#     profile["Average_Income"] = profile["Average_Income"].round(2)
#     profile["Average_Spending"] = profile["Average_Spending"].round(2)

#     return profile


# def assign_cluster_meaning(profile):
#     """
#     Assign a business-friendly meaning to each cluster
#     based on average income and spending score.
#     """

#     meanings = []

#     for _, row in profile.iterrows():

#         income = row["Average_Income"]
#         spending = row["Average_Spending"]

#         if income >= 70 and spending >= 60:
#             meaning = "High-value customers"

#         elif income >= 70 and spending < 60:
#             meaning = "High-income but low-spending customers"

#         elif income < 70 and spending >= 60:
#             meaning = "Low-income but high-spending customers"

#         else:
#             meaning = "Low-income and low-spending customers"

#         meanings.append(meaning)

#     profile["Cluster_Meaning"] = meanings

#     return profile


# def assign_business_recommendation(profile):
#     """
#     Generate business recommendations for each customer segment.
#     """

#     recommendations = []

#     for meaning in profile["Cluster_Meaning"]:

#         if meaning == "High-value customers":
#             recommendation = (
#                 "Offer VIP membership, loyalty rewards, premium products "
#                 "and personalized offers."
#             )

#         elif meaning == "High-income but low-spending customers":
#             recommendation = (
#                 "Use personalized promotions, premium product recommendations "
#                 "and targeted discounts to increase spending."
#             )

#         elif meaning == "Low-income but high-spending customers":
#             recommendation = (
#                 "Offer affordable deals, discounts, bundle offers "
#                 "and reward-based promotions."
#             )

#         else:
#             recommendation = (
#                 "Use budget-friendly offers, introductory discounts "
#                 "and engagement campaigns to increase spending."
#             )

#         recommendations.append(recommendation)

#     profile["Business_Recommendation"] = recommendations

#     return profile


# def generate_recommendations(df, cluster_column="KMeans_Cluster"):
#     """
#     Complete recommendation pipeline.
#     """

#     profile = create_cluster_profile(
#         df,
#         cluster_column
#     )

#     profile = assign_cluster_meaning(profile)

#     profile = assign_business_recommendation(profile)

#     return profile


# if __name__ == "__main__":

#     # Test data
#     data = {
#         "CustomerID": [1, 2, 3, 4],
#         "Annual Income (k$)": [90, 85, 30, 40],
#         "Spending Score (1-100)": [80, 40, 75, 30],
#         "KMeans_Cluster": [0, 1, 2, 3],
#     }

#     df = pd.DataFrame(data)

#     result = generate_recommendations(df)

#     print("\n===== CLUSTER PROFILE =====")
#     print(result.to_string(index=False))