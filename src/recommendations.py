def get_recommendation(segment: str) -> dict[str, str]:
    """Return business recommendations for a customer segment."""

    recommendations = {
        "Premium Customers": {
            "product_strategy": "Recommend premium and high-value products.",
            "marketing_strategy": "Offer exclusive deals and loyalty rewards.",
            "customer_action": "Focus on upselling and cross-selling.",
        },
        "Potential Customers": {
            "product_strategy": "Recommend products that encourage higher spending.",
            "marketing_strategy": "Use personalized offers and targeted campaigns.",
            "customer_action": "Focus on engagement and conversion.",
        },
        "Value-Seeking Customers": {
            "product_strategy": "Recommend affordable products and value bundles.",
            "marketing_strategy": "Offer discounts and promotional campaigns.",
            "customer_action": "Focus on value-based offers and loyalty incentives.",
        },
        "Budget Customers": {
            "product_strategy": "Recommend affordable and entry-level products.",
            "marketing_strategy": "Use discount and price-sensitive campaigns.",
            "customer_action": "Focus on retention and low-cost offers.",
        },
    }

    return recommendations.get(
        segment,
        {
            "product_strategy": "Use general product recommendations.",
            "marketing_strategy": "Use general marketing campaigns.",
            "customer_action": "Monitor customer behavior.",
        },
    )