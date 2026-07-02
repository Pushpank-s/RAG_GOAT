def generate_reason(chart, metadata):

    if chart == "Line Chart":
        return "Time-series data detected with one or more numeric columns."

    if chart == "Bar Chart":
        return "Categorical and numerical columns detected, making comparison effective."

    if chart == "Scatter Plot":
        return "Multiple numerical columns detected for relationship analysis."

    if chart == "Histogram":
        return "Numerical data available for distribution analysis."

    if chart == "Pie Chart":
        return "Single categorical variable suitable for showing proportions."

    return "Suitable visualization."