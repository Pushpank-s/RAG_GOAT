from app.services.explanation_engine import generate_reason


# Columns that are usually identifiers
ID_KEYWORDS = [
    "id",
    "name",
    "ticket",
    "cabin",
    "uuid",
    "index"
]


def is_identifier(column_name):
    column_name = column_name.lower()

    return any(keyword in column_name for keyword in ID_KEYWORDS)


def recommend_charts(metadata):

    recommendations = []

    numeric_cols = metadata["numeric_column_names"]
    categorical_cols = metadata["categorical_column_names"]
    datetime_cols = metadata["datetime_column_names"]

    # NEW: Cardinality information (we'll add this in the next step)
    cardinality = metadata.get("column_cardinality", {})

    # -----------------------------
    # Time Series
    # -----------------------------
    for date_col in datetime_cols:

        for num_col in numeric_cols:

            if is_identifier(num_col):
                continue

            recommendations.append({
                "chart": "Line Chart",
                "x": date_col,
                "y": num_col,
                "score": 98,
                "reason": generate_reason("Line Chart", metadata)
            })

    # -----------------------------
    # Category Comparison
    # -----------------------------
    for cat in categorical_cols:

        if is_identifier(cat):
            continue

        unique = cardinality.get(cat, 999)

        # Ignore columns with too many unique values
        if unique > 20:
            continue

        for num in numeric_cols:

            if is_identifier(num):
                continue

            score = 80

            # Binary target
            if num.lower() in [
                "survived",
                "target",
                "label",
                "class"
            ]:
                score += 15

            # Binary category
            if unique == 2:
                score += 10

            # Small number of categories
            elif unique <= 5:
                score += 5

            recommendations.append({
                "chart": "Bar Chart",
                "x": cat,
                "y": num,
                "score": score,
                "reason": generate_reason("Bar Chart", metadata)
            })

    # -----------------------------
    # Scatter
    # -----------------------------
    for i in range(len(numeric_cols)):

        for j in range(i + 1, len(numeric_cols)):

            if is_identifier(numeric_cols[i]):
                continue

            if is_identifier(numeric_cols[j]):
                continue

            recommendations.append({
                "chart": "Scatter Plot",
                "x": numeric_cols[i],
                "y": numeric_cols[j],
                "score": 75,
                "reason": generate_reason("Scatter Plot", metadata)
            })

    # -----------------------------
    # Histogram
    # -----------------------------
    for num in numeric_cols:

        if is_identifier(num):
            continue

        recommendations.append({
            "chart": "Histogram",
            "x": num,
            "y": None,
            "score": 72,
            "reason": generate_reason("Histogram", metadata)
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    final_recommendations = []
    used_chart_types = set()


    for rec in recommendations:
        if rec["chart"] not in used_chart_types:
            final_recommendations.append(rec)
            used_chart_types.add(rec["chart"])


    for rec in recommendations:
        if len(final_recommendations) >= 5:
            break

        if rec not in final_recommendations:
            final_recommendations.append(rec)

    return final_recommendations