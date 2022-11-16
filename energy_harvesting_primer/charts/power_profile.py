import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette

CHART_HEIGHT = 300
CHART_WIDTH = 700

color = palette.ColorPalette()


def power_profile() -> alt.LayerChart:
    """Generate a diagram of a simple sensor power profile that depicts sensor
    active/idle mode & duty-cycle rate and return as an Altair chart."""

    idle_height = 2
    active_height = 10
    arrow_color = "black"
    arrow_size = 40
    arrow_epsilon = 0.4
    max_y = 13
    max_x = 34

    bars = [
        {"x": 0, "x2": 3, "state": "Idle"},
        {"x": 3, "x2": 8, "state": "Active"},
        {"x": 8, "x2": 18, "state": "Idle"},
        {"x": 18, "x2": 23, "state": "Active"},
        {"x": 23, "x2": 33, "state": "Idle"},
    ]

    df_bars = pd.DataFrame(bars)
    df_bars["y"] = 0
    df_bars["y2"] = df_bars["state"].apply(
        lambda x: idle_height if x == "Idle" else active_height
    )

    arrows = [
        {
            "x": 3 + arrow_epsilon,
            "x2": 18 - arrow_epsilon,
            "y": 11,
            "label_x": 10.5,
            "label": "duty-cycle rate",
        },
        {
            "x": 3 + arrow_epsilon,
            "x2": 8 - arrow_epsilon,
            "y": -1.5,
            "label_x": 5.5,
            "label": "t active",
        },
        {
            "x": 8 + arrow_epsilon,
            "x2": 18 - arrow_epsilon,
            "y": -1.5,
            "label_x": 13,
            "label": "t idle",
        },
    ]

    df_arrows = pd.DataFrame(arrows)

    df_y_axis = pd.DataFrame([{"x": 0, "y": 0, "y2": max_y}])
    df_x_axis = pd.DataFrame([{"x": 0, "x2": max_x, "y": 0}])

    df_axis_labels = pd.DataFrame(
        [
            {"x": -1, "y": idle_height, "label": "P idle"},
            {"x": 0, "y": idle_height, "label": "—"},
            {"x": -1, "y": active_height, "label": "P active"},
            {"x": 0, "y": active_height, "label": "—"},
            {"x": -1, "y": max_y, "label": "power"},
            {"x": max_x, "y": -1, "label": "time"},
        ]
    )

    bars = (
        alt.Chart(df_bars)
        .mark_bar(opacity=0.8)
        .encode(
            x=alt.X("x", axis=None),
            x2="x2",
            y=alt.Y("y", axis=None),
            y2="y2",
            color=alt.Color(
                "state",
                scale=alt.Scale(
                    domain=["Active", "Idle"],
                    range=[color.chartreuse(), color.dark_teal()],
                ),
                legend=alt.Legend(title="Mode of Operation"),
            ),
        )
    )

    arrow_lines = (
        alt.Chart(df_arrows)
        .mark_line()
        .encode(
            x=alt.X("x"),
            x2="x2",
            y=alt.Y("y"),
        )
    )

    arrow_points_left = arrow_lines.mark_point(
        shape="triangle",
        size=arrow_size,
        angle=270,
        fill=arrow_color,
        color=arrow_color,
    ).encode(alt.X("x"), alt.Y("y"))

    arrow_points_right = arrow_lines.mark_point(
        shape="triangle", size=arrow_size, angle=90, fill=arrow_color, color=arrow_color
    ).encode(alt.X("x2"), alt.Y("y"))

    arrow_text = arrow_lines.mark_text(align="center", dy=-10).encode(
        alt.X("label_x"), text="label"
    )

    y_axis = alt.Chart(df_y_axis).mark_line().encode(x="x", y="y", y2="y2")
    x_axis = alt.Chart(df_x_axis).mark_line().encode(x="x", x2="x2", y="y")

    axis_labels = (
        alt.Chart(df_axis_labels)
        .mark_text(align="right")
        .encode(alt.X("x"), alt.Y("y"), text="label")
    )

    x_axis_arrow_label = (
        alt.Chart(pd.DataFrame([{"x": max_x, "y": 0}]))
        .mark_point(
            shape="triangle",
            size=arrow_size,
            angle=90,
            fill=arrow_color,
            color=arrow_color,
        )
        .encode(alt.X("x"), alt.Y("y"))
    )

    y_axis_arrow_label = (
        alt.Chart(pd.DataFrame([{"x": 0, "y": max_y}]))
        .mark_point(
            shape="triangle",
            size=arrow_size,
            fill=arrow_color,
            color=arrow_color,
        )
        .encode(alt.X("x"), alt.Y("y"))
    )

    chart = (
        alt.layer(
            bars,
            arrow_lines,
            arrow_points_left,
            arrow_points_right,
            arrow_text,
            y_axis,
            x_axis,
            axis_labels,
            x_axis_arrow_label,
            y_axis_arrow_label,
        )
        .configure_axis(grid=False)
        .configure_view(strokeWidth=0)
        .properties(height=CHART_HEIGHT, width=CHART_WIDTH)
    )

    return chart
