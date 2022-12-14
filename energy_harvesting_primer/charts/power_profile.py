from typing import Tuple

import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.utils as utils

CHART_HEIGHT = 250
CHART_WIDTH = 700

color = palette.ColorPalette()

MAX_TIME_MINUTES = 30
MAX_TIME_SECONDS = 60 * MAX_TIME_MINUTES
MAX_POWER = 80


def power_profile(
    idle_power: int,
    active_power: int,
    active_operation_seconds: int,
    active_operation_frequency: int,
) -> Tuple[alt.LayerChart, float, float]:
    """Generate chart depicting the power profile for a sensor with two modes: active
    and idle.

    Args:
        idle_power: power used in idle mode (in microwatts)
        active_power: power used in active mode (in microwatts)

    Returns:
        Tuple of:
            power profile chart, as altair LayerChart
            duty cycle, as float
            average power load, as float
    """
    t_active = active_operation_seconds
    t_idle = active_operation_frequency - active_operation_seconds
    duty_cycle = t_active / (t_active + t_idle)
    average_load_power = active_power * duty_cycle + idle_power * (1 - duty_cycle)

    is_active = []
    for event in range(0, int(MAX_TIME_SECONDS / active_operation_frequency) + 1):
        event_t = event * active_operation_frequency
        is_active.extend([event_t + t for t in range(0, active_operation_seconds)])

    data = []
    for t in range(0, MAX_TIME_SECONDS):
        power = active_power if t in is_active else idle_power
        data.append({"t": t, "power": power, "mode": "Sensor Power"})

    df = pd.DataFrame(data)
    df["t_min"] = df["t"] / 60

    min_tick_labels = """
        datum.label == '30' ? '...'
        : datum.label
    """

    legend_orientation = "right"

    base_chart = (
        alt.Chart(df)
        .mark_area(line=True)
        .encode(
            alt.X(
                "t_min",
                axis=alt.Axis(
                    title="Time (min)",
                    titlePadding=12,
                    labelExpr=min_tick_labels,
                ),
                scale=alt.Scale(domain=[0, MAX_TIME_MINUTES]),
            ),
            alt.Y(
                "power",
                axis=alt.Axis(
                    title="Power Consumption (watts)",
                    titlePadding=12,
                    labelExpr=f'datum.value + " {utils.MU}W"',
                ),
                scale=alt.Scale(domain=[0, MAX_POWER]),
            ),
            color=alt.Color(
                "mode",
                legend=alt.Legend(title="Power Consumption", orient=legend_orientation),
                scale=alt.Scale(
                    domain=["Sensor Power"],
                    range=[color.chartreuse()],
                ),
            ),
            tooltip=alt.value(None),
        )
    )

    avg_power_load_line = (
        alt.Chart(
            pd.DataFrame({"y": [average_load_power], "mode": "Average Load Power"})
        )
        .mark_rule(strokeDash=[5, 1], strokeWidth=1)
        .encode(
            y="y",
            color=alt.Color(
                "mode",
                legend=alt.Legend(title=None, orient=legend_orientation),
                scale=alt.Scale(
                    domain=["Average Load Power"],
                    range=[color.charcoal()],
                ),
            ),
            tooltip=alt.value(None),
        )
    )

    df_text = pd.DataFrame(
        [
            {
                "x": (active_operation_seconds + 5) / 60,
                "y": idle_power,
                "label": "- P idle",
            },
            {
                "x": (active_operation_seconds + 5) / 60,
                "y": active_power,
                "label": "- P active",
            },
        ]
    )

    text_annotations = (
        alt.Chart(df_text)
        .mark_text(align="left")
        .encode(
            alt.X("x", scale=alt.Scale(domain=[0, MAX_TIME_MINUTES])),
            alt.Y("y", scale=alt.Scale(domain=[0, MAX_POWER])),
            text="label",
            tooltip=alt.value(None),
        )
    )

    chart = (
        alt.layer(base_chart, avg_power_load_line, text_annotations)
        .resolve_scale(color="independent", strokeDash="independent")
        .properties(height=CHART_HEIGHT, width=CHART_WIDTH)
    )

    return chart, duty_cycle, average_load_power
