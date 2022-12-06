import math

import altair as alt
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


def example_pload_vs_pharv() -> alt.LayerChart:
    """Generate example chart depicting load power vs. harvestable power in an ideal
    sensor."""

    chart_size = 350
    legend_size = 150

    power_values = []
    for x in range(MIN_POWER_EXP, MAX_POWER_EXP + 1):
        watt_value = 10 ** (x)
        power_values.append({"p_harvestable": watt_value, "p_load": watt_value})

    df_power = pd.DataFrame(power_values)
    df_power["label"] = "Ideal Operation"

    base_chart = (
        alt.Chart(df_power)
        .mark_line()
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
                "p_harvestable",
                axis=alt.Axis(
                    title=["log (Harvestable Power)", "(watts)"],
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
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
            tooltip="p_load",
        )
    )

    return (
        alt.layer(base_chart)
        .configure_legend(labelLimit=legend_size)
        .properties(height=chart_size, width=chart_size + legend_size)
    )


def example_power_modes() -> alt.Chart:
    """Generate example chart depicting the power required for different sensor modes of
    operation at varying duty cycles."""

    chart_height = 300
    chart_width = 500
    legend_size = 100

    min_duty_cycle = 1e-6
    power_floor = 1e-8

    modes_profiles = {
        1: {"power_active": 1e-2, "knee": 1e-5},
        2: {"power_active": 1e-3, "knee": 1e-4},
        3: {"power_active": 1e-6, "knee": 1e-2},
    }

    mode_power_at_duty_cycle = []

    for duty_cycle in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1]:

        for mode in modes_profiles.keys():
            delta_log_y = math.log(modes_profiles[mode]["power_active"]) - math.log(
                power_floor
            )
            delta_log_x = math.log(1) - math.log(modes_profiles[mode]["knee"])
            slope = delta_log_y / delta_log_x

            if duty_cycle <= modes_profiles[mode]["knee"]:
                power = power_floor
            elif duty_cycle == 1:
                power = modes_profiles[mode]["power_active"]
            else:
                power = modes_profiles[mode]["power_active"] * math.pow(
                    duty_cycle, slope
                )

            mode_power_at_duty_cycle.append(
                {"mode": f"Mode {mode}", "duty_cycle": duty_cycle, "power": power}
            )

    df_modes = pd.DataFrame(mode_power_at_duty_cycle)

    color_scale = alt.Scale(
        domain=["Mode 1", "Mode 2", "Mode 3"],
        range=[color.violet(), color.sky(), color.midnight()],
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
                scale=alt.Scale(type="log", domain=[1e-9, 1]),
            ),
            color=alt.Color(
                "mode", legend=alt.Legend(title="Sensor Mode"), scale=color_scale
            ),
            strokeDash=alt.StrokeDash("mode", legend=None),
        )
    )

    return (
        alt.layer(base_chart)
        .configure_legend(labelLimit=legend_size)
        .properties(height=chart_height, width=chart_width + legend_size)
    )


def power_operating_space(p_floor: float = 1e-8, p_active: float = 1e-6) -> alt.Chart:
    chart_size = 400

    min_power = 10 ** (MIN_POWER_EXP)
    max_power = 10 ** (MAX_POWER_EXP)

    power_values = []
    for x in range(MIN_POWER_EXP, MAX_POWER_EXP + 1):
        watt_value = 10 ** (x)
        power_values.append({"p_harvestable": watt_value, "p_load": watt_value})

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
                "p_load": p_floor,
                "p_harv_lower": min_power,
                "p_harv_upper": p_floor,
                "name": ZONE_1,
            },
            # zone 2
            {
                "p_load": p_floor,
                "p_harv_lower": min_power,
                "p_harv_upper": p_floor,
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
                "p_harv_upper": p_floor,
                "p_harv_lower": min_power,
                "p_load": min_power,
                "name": ZONE_1,
            },
            {
                "p_harv_upper": p_floor,
                "p_harv_lower": p_floor,
                "p_load": p_floor,
                "name": ZONE_1,
            },
            # Zone 2
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_floor,
                "p_load": min_power,
                "name": ZONE_2,
            },
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_floor,
                "p_load": p_floor,
                "name": ZONE_2,
            },
            {
                "p_harv_upper": p_active,
                "p_harv_lower": p_floor,
                "p_load": p_floor,
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
        domain=[
            "No Energy Harvesting",
            "Constrained Energy Harvesting",
            "Plentiful Energy Harvesting",
        ],
        range=[color.apricot(), color.chartreuse(), color.sky()],
    )

    nearest = alt.selection(
        type="single", nearest=True, on="mouseover", fields=["x"], empty="none"
    )

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
                "p_harvestable",
                axis=alt.Axis(
                    title=["log (Harvestable Power)", "(watts)"],
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
            tooltip="p_load",
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
        )
    )

    harvestable_power_zones = (
        alt.Chart(df_p_harv_zones)
        .mark_area(opacity=0.5)
        .encode(
            x=alt.X("p_load", scale=alt.Scale(type="log")),
            y=alt.Y("p_harv_lower", scale=alt.Scale(type="log")),
            y2=alt.Y2("p_harv_upper"),
            color=alt.Color("name:N", scale=zone_color_scale, legend=None),
        )
    )

    pload_vs_pharv_chart = (
        alt.layer(base_chart, load_power_zones, harvestable_power_zones)
        .resolve_scale(color="independent")
        .properties(
            width=chart_size,
            height=chart_size,
            title="Energy Harvesting Zones, Defined by Load and Harvestable Power",
        )
    )

    min_duty_cycle = 1e-4
    df_curve = pd.DataFrame(
        [
            {"x": 0, "y": p_floor},
            {"x": min_duty_cycle, "y": p_floor},
            {"x": 1, "y": p_active},
        ]
    )
    df_curve["mode"] = "Sensor Mode of Operation"

    duty_cycle_chart = (
        alt.Chart(df_curve)
        .mark_line()
        .encode(
            alt.X(
                "x",
                axis=alt.Axis(
                    title="log (Duty Cycle)",
                    titlePadding=TITLE_PADDING,
                    labelExpr=DUTY_CYCLE_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[1e-6, 1]),
            ),
            alt.Y(
                "y",
                axis=alt.Axis(
                    title="log (Load Power) (watts)",
                    titlePadding=TITLE_PADDING,
                    labelExpr=SIMPLE_POWER_TICK_LABELS,
                ),
                scale=alt.Scale(type="log", domain=[1e-9, 1]),
            ),
            color=alt.Color(
                "mode",
                legend=None,
                scale=alt.Scale(
                    domain=["Sensor Mode of Operation"],
                    range=[color.violet()],
                ),
            ),
        )
    )

    duty_cycle_vs_pload_chart = alt.layer(duty_cycle_chart).properties(
        title="Sensor Mode of Operation", width=chart_size, height=150
    )

    return alt.vconcat(duty_cycle_vs_pload_chart, pload_vs_pharv_chart).configure_title(
        anchor="start"
    )
