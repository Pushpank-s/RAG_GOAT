import plotly.express as px


def generate_chart(df, chart_type, x=None, y=None):
    """
    Generate an interactive Plotly chart based on chart type.
    """

    chart_type = chart_type.lower().strip()

    if "bar" in chart_type:
        fig = px.bar(df, x=x, y=y)

    elif "line" in chart_type:
        fig = px.line(df, x=x, y=y)

    elif "scatter" in chart_type:
        fig = px.scatter(df, x=x, y=y)


    elif "histogram" in chart_type:
        fig = px.histogram(df, x=x)

    elif "pie" in chart_type:
        fig = px.pie(df, names=x, values=y)

    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    return fig.to_json()