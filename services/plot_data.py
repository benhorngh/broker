import plotly.graph_objs as go


def plot_lines(*args):
    traces = []
    for i, lst in enumerate(args):
        traces.append(
            go.Scatter(
                x=list(range(1, len(lst) + 1)),
                y=lst,
                mode="lines",
                name=f"List {i + 1}",
            )
        )

    layout = go.Layout(
        title="Line Chart with Plotly",
        xaxis=dict(title="X-Axis"),
        yaxis=dict(title="Y-Axis"),
    )
    fig = go.Figure(data=traces, layout=layout)

    fig.show()
