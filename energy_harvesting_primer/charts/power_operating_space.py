import math

import altair as alt
import numpy as np
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.utils as utils

color = palette.ColorPalette()

ZONE_1 = "No Energy Harvesting"
ZONE_2 = "Constrained Energy Harvesting"
ZONE_3 = "Plentiful Energy Harvesting"

TITLE_PADDING = 12

MIN_POWER_EXP = -9
MAX_POWER_EXP = 0

DUTY_CYCLE_TICK_LABELS = """
    datum.label == 1e-0 ? '1'
    : datum.label == 1e-1 ? '1/10'
    : datum.label == 1e-2 ? '1/100'
    : datum.label == 1e-3 ? '1e-3'
    : datum.label == 1e-4 ? '1e-4'
    : datum.label == 1e-5 ? '1e-5'
    : datum.label == 1e-6 ? '1e-6'
    : datum.label == 1e-7 ? '1e-7'
    : datum.label == 1e-8 ? '1e-8'
    : datum.label == 1e-9 ? '1e-9'
    : datum.label
"""


SIMPLE_POWER_TICK_LABELS = f"""
    datum.label == 1e-0 ? '1 W'
    : datum.label == 1e-3 ? '1 mW'
    : datum.label == 1e-6 ? '1 {utils.MU}W'
    : datum.label == 1e-9 ? '1 nW'
    : ''
"""


POWER_TICK_LABELS = f"""
    datum.label == 1e-0 ? '1 W'
    : datum.label == 1e-1 ? '100'
    : datum.label == 1e-2 ? '10'
    : datum.label == 1e-3 ? '1 mW'
    : datum.label == 1e-4 ? '100'
    : datum.label == 1e-5 ? '10'
    : datum.label == 1e-6 ? '1 {utils.MU}W'
    : datum.label == 1e-7 ? '100'
    : datum.label == 1e-8 ? '10'
    : datum.label == 1e-9 ? '1 nW'
    : datum.label
"""


def example_load_power_vs_harvested_power() -> alt.LayerChart:
    """Generate example chart depicting load power vs. harvested power in an ideal
    sensor."""

    chart_size = 350
    legend_size = 150
    always_on_power = 1e-7

    power_values = []
    for x in range(MIN_POWER_EXP, MAX_POWER_EXP + 1):
        watts = 10 ** (x)
        if watts < always_on_power:
            power_values.append(
                {
                    "p_harvested": watts,
                    "p_load": watts,
                    "label": "Below Always-On Power",
                }
            )
        elif watts == always_on_power:
            power_values.append(
                {
                    "p_harvested": watts,
                    "p_load": watts,
                    "label": "Below Always-On Power",
                }
            )
            power_values.append(
                {"p_harvested": watts, "p_load": watts, "label": "Ideal Operation"}
            )
        else:
            power_values.append(
                {"p_harvested": watts, "p_load": watts, "label": "Ideal Operation"}
            )

    df_power = pd.DataFrame(power_values)

    base_chart = (
        alt.Chart(df_power)
        .mark_line(color=color.dark_teal())
        .encode(
            alt.X(
                "p_load",
                axis=alt.Axis(
                    title=["log (Load Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log"),
            ),
            alt.Y(
                "p_harvested",
                axis=alt.Axis(
                    title=["log (Harvested Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log"),
            ),
            strokeDash=alt.StrokeDash(
                "label",
                legend=alt.Legend(title="Sensor Power Usage"),
                sort=["Ideal Operation", "Below Always-On Power"],
            ),
            tooltip=alt.value(None),
        )
    )

    always_on_power_boundary = (
        alt.Chart(pd.DataFrame({"x": [always_on_power]}))
        .mark_rule(strokeDash=[3, 1], strokeWidth=1, color=color.charcoal())
        .encode(x="x", tooltip=alt.value(None))
    )

    always_on_power_text = (
        alt.Chart(
            pd.DataFrame([{"x": always_on_power, "y": 1, "text": "Always-On\nPower"}])
        )
        .mark_text(color=color.charcoal(), align="left", dx=5, dy=10, lineBreak="\n")
        .encode(x="x", y="y", text="text", tooltip=alt.value(None))
    )

    return (
        alt.layer(base_chart, always_on_power_boundary, always_on_power_text)
        .configure_legend(labelLimit=legend_size)
        .properties(height=chart_size, width=chart_size + legend_size)
    )


def example_power_modes() -> alt.LayerChart:
    """Generate example chart depicting the power required for different sensor modes of
    operation at varying duty cycles."""

    chart_height = 300
    chart_width = 350
    legend_size = 100

    min_duty_cycle = 1e-6
    min_power = 1e-9

    always_on_power = 1e-7

    mode_profiles = {
        1: {"power_active": 1e-2, "min_duty_cycle": 1e-6},
        2: {"power_active": 1e-4, "min_duty_cycle": 1e-4},
        3: {"power_active": 1e-6, "min_duty_cycle": 1e-2},
    }

    mode_power_at_duty_cycle = []

    for duty_cycle_power in range(-6, 1):
        duty_cycle = 10**duty_cycle_power

        for mode in mode_profiles.keys():
            delta_log_y = math.log(mode_profiles[mode]["power_active"]) - math.log(
                min_power
            )
            delta_log_x = math.log(1) - math.log(mode_profiles[mode]["min_duty_cycle"])
            slope = delta_log_y / delta_log_x

            if duty_cycle >= mode_profiles[mode]["min_duty_cycle"]:
                power = mode_profiles[mode]["power_active"] * math.pow(
                    duty_cycle, slope
                )
                mode_power_at_duty_cycle.append(
                    {"mode": f"Mode {mode}", "duty_cycle": duty_cycle, "power": power}
                )

    df_modes = pd.DataFrame(mode_power_at_duty_cycle)

    color_scale = alt.Scale(
        domain=["Mode 1", "Mode 2", "Mode 3"],
        range=[color.violet(), color.dark_teal(), color.midnight()],
    )

    base_chart = (
        alt.Chart(df_modes)
        .mark_line()
        .encode(
            alt.X(
                "duty_cycle",
                axis=alt.Axis(
                    title="log (Duty Cycle)",
                    titlePadding=TITLE_PADDING,
                    labelExpr=DUTY_CYCLE_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[min_duty_cycle, 1]),
            ),
            alt.Y(
                "power",
                axis=alt.Axis(
                    title=["log (Load Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[min_power, 1]),
            ),
            color=alt.Color(
                "mode", legend=alt.Legend(title="Sensor Mode"), scale=color_scale
            ),
        )
    )

    always_on_rule = (
        alt.Chart(pd.DataFrame([{"y": always_on_power}]))
        .mark_rule(strokeDash=[3, 1], strokeWidth=1, color=color.charcoal())
        .encode(y="y", tooltip=alt.value(None))
    )

    df_p_active = pd.DataFrame(
        [
            {"mode": f"Mode {k}", "x": 1, "label": "P active", **v}
            for k, v in mode_profiles.items()
        ]
    )

    p_active_circles = (
        alt.Chart(df_p_active)
        .mark_circle(size=50, opacity=1)
        .encode(alt.X("x"), alt.Y("power_active"), color=alt.Color("mode", legend=None))
    )

    p_active_text = (
        alt.Chart(df_p_active)
        .mark_text(align="right", dx=-5, dy=-6)
        .encode(
            alt.X("x"),
            alt.Y("power_active"),
            color=alt.Color("mode", legend=None),
            text="label",
        )
    )

    return (
        alt.layer(base_chart, p_active_circles, always_on_rule, p_active_text)
        .configure_legend(labelLimit=legend_size)
        .properties(height=chart_height, width=chart_width + legend_size)
    )


def power_operating_space(
    p_always_on: float = 1e-8, p_active: float = 1e-6
) -> alt.VConcatChart:
    """Generate a chart depicting sensor power operating space, based on supplied specs.

    Args:
        p_always_on: sensor always-on power, in watts
        p_active: active power of sensor mode, in watts

    Returns:
        Chart as altair VConcatChart
    """

    chart_size = 400

    min_power = 10 ** (MIN_POWER_EXP)
    max_power = 10 ** (MAX_POWER_EXP)

    power_values = []
    for x in range(MIN_POWER_EXP, MAX_POWER_EXP + 1):
        watt_value = 10 ** (x)
        power_values.append({"p_harvested": watt_value, "p_load": watt_value})

    df_power = pd.DataFrame(power_values)
    df_power["label"] = "Ideal Operation"

    df_p_load_zones = pd.DataFrame(
        [
            {
                "p_load": min_power,
                "p_harv_lower": min_power,
                "p_harv_upper": min_power,
                "name": ZONE_1,
            },
            {
                "p_load": p_always_on,
                "p_harv_lower": min_power,
                "p_harv_upper": p_always_on,
                "name": ZONE_1,
            },
            # zone 2
            {
                "p_load": p_always_on,
                "p_harv_lower": min_power,
                "p_harv_upper": p_always_on,
                "name": ZONE_2,
            },
            {
                "p_load": p_active,
                "p_harv_lower": min_power,
                "p_harv_upper": p_active,
                "name": ZONE_2,
            },
            {
                "p_load": p_active,
                "p_harv_lower": min_power,
                "p_harv_upper": p_active,
                "name": ZONE_3,
            },
            {
                "p_load": max_power,
                "p_harv_lower": min_power,
                "p_harv_upper": max_power,
                "name": ZONE_3,
            },
        ]
    )

    df_p_harv_zones = pd.DataFrame(
        [
            {
                "p_harv_upper": p_always_on,
                "p_harv_lower": min_power,
                "p_load": min_power,
                "name": ZONE_1,
            },
            {
                "p_harv_upper": p_always_on,
                "p_harv_lower": p_always_on,
                "p_load": p_always_on,
                "name": ZONE_1,
            },
            # Zone 2
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_always_on,
                "p_load": min_power,
                "name": ZONE_2,
            },
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_always_on,
                "p_load": p_always_on,
                "name": ZONE_2,
            },
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_always_on,
                "p_load": p_always_on,
                "name": ZONE_2,
            },
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_active,
                "p_load": p_active,
                "name": ZONE_2,
            },
            # Zone 3
            {
                "p_harv_upper": max_power,
                "p_harv_lower": p_active,
                "p_load": min_power,
                "name": ZONE_3,
            },
            {
                "p_harv_upper": max_power,
                "p_harv_lower": p_active,
                "p_load": p_active,
                "name": ZONE_3,
            },
            {
                "p_harv_upper": max_power,
                "p_harv_lower": p_active,
                "p_load": p_active,
                "name": ZONE_3,
            },
            {
                "p_harv_upper": max_power,
                "p_harv_lower": max_power,
                "p_load": max_power,
                "name": ZONE_3,
            },
        ]
    )

    zone_color_scale = alt.Scale(
        domain=[ZONE_1, ZONE_2, ZONE_3],
        range=[color.apricot(), color.chartreuse(), color.sky()],
    )

    # log(duty cycle) vs. log(load power) chart

    min_mode_duty_cycle = 1e-6

    mode_curve = []
    always_on_line = []

    delta_log_y = math.log(p_active) - math.log(min_power)
    delta_log_x = math.log(1) - math.log(min_mode_duty_cycle)
    slope = delta_log_y / delta_log_x

    for duty_cycle in np.logspace(-6, 0, num=1000):
        power = p_active * math.pow(duty_cycle, slope)

        curve_point = {
            "mode": f"Active Mode",
            "duty_cycle": duty_cycle,
            "power": power,
        }
        always_on_point = {
            "mode": "Always-On",
            "power": p_always_on,
            "duty_cycle": duty_cycle,
        }

        if power > p_always_on:
            mode_curve.append({**curve_point, "line": "solid"})

        elif power == p_always_on:
            mode_curve.append({**curve_point, "line": "solid"})
            mode_curve.append({**curve_point, "line": "dashed"})
        else:
            mode_curve.append({**curve_point, "line": "dashed"})

        if power > p_always_on:
            always_on_line.append({**always_on_point, "line": "dashed"})
        else:
            always_on_line.append({**always_on_point, "line": "solid"})

    df_mode_curve = pd.DataFrame(mode_curve)
    df_always_on = pd.DataFrame(always_on_line)

    mode_base = (
        alt.Chart(df_mode_curve)
        .mark_line()
        .encode(
            alt.X(
                "duty_cycle",
                axis=alt.Axis(
                    title="log (Duty Cycle)",
                    titlePadding=TITLE_PADDING,
                    labelExpr=DUTY_CYCLE_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[1e-6, 1]),
            ),
            alt.Y(
                "power",
                axis=alt.Axis(
                    title="log (Load Power) (watts)",
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[1e-9, 1]),
            ),
            color=alt.Color(
                "mode",
                legend=alt.Legend(title="Power Usage"),
                scale=alt.Scale(
                    domain=["Active Mode"],
                    range=[color.dark_teal()],
                ),
            ),
            strokeDash=alt.StrokeDash("line", sort=["solid", "dashed"], legend=None),
            tooltip=alt.value(None),
        )
    )

    always_on_power_boundary = (
        alt.Chart(df_always_on)
        .mark_line()
        .encode(
            alt.X("duty_cycle"),
            alt.Y("power"),
            color=alt.Color(
                "mode",
                legend=alt.Legend(title=None),
                scale=alt.Scale(
                    domain=["Always-On"],
                    range=[color.charcoal()],
                ),
            ),
            strokeDash=alt.StrokeDash("line", sort=["solid", "dashed"]),
            tooltip=alt.value(None),
        )
    )

    duty_cycle_vs_pload_chart = (
        alt.layer(mode_base, always_on_power_boundary)
        .resolve_scale(color="independent")
        .properties(title="Sensor Mode of Operation", width=chart_size, height=150)
    )

    # Energy harvesting zones chart.
    base_chart = (
        alt.Chart(df_power)
        .mark_line()
        .encode(
            alt.X(
                "p_load",
                axis=alt.Axis(
                    title=["log (Load Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log"),
            ),
            alt.Y(
                "p_harvested",
                axis=alt.Axis(
                    title=["log (Harvested Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log"),
            ),
            color=alt.Color(
                "label",
                legend=alt.Legend(title="Sensor Power Usage"),
                scale=alt.Scale(
                    domain=["Ideal Operation"],
                    range=[color.dark_teal()],
                ),
            ),
            tooltip=alt.value(None),
        )
    )

    load_power_zones = (
        alt.Chart(df_p_load_zones)
        .mark_area(opacity=0.5)
        .encode(
            x=alt.X("p_load", scale=alt.Scale(type="log")),
            y=alt.Y("p_harv_lower", scale=alt.Scale(type="log")),
            y2=alt.Y2("p_harv_upper"),
            color=alt.Color(
                "name:N",
                legend=alt.Legend(
                    title="Energy Harvesting Zones",
                ),
                scale=zone_color_scale,
            ),
            tooltip=alt.value(None),
        )
    )

    harvested_power_zones = (
        alt.Chart(df_p_harv_zones)
        .mark_area(opacity=0.5)
        .encode(
            x=alt.X("p_load", scale=alt.Scale(type="log")),
            y=alt.Y("p_harv_lower", scale=alt.Scale(type="log")),
            y2=alt.Y2("p_harv_upper"),
            color=alt.Color("name:N", scale=zone_color_scale, legend=None),
            tooltip=alt.value(None),
        )
    )

    pload_vs_pharv_chart = (
        alt.layer(base_chart, load_power_zones, harvested_power_zones)
        .resolve_scale(color="independent")
        .properties(
            width=chart_size,
            height=chart_size,
            title="Energy Harvesting Zones, Defined by Load and Harvested Power",
        )
    )

    return alt.vconcat(duty_cycle_vs_pload_chart, pload_vs_pharv_chart).configure_title(
        anchor="start"
    )
