import collections
from typing import Dict, Tuple

import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.sensor_profiles as profiles
import energy_harvesting_primer.utils as utils

IDLE_DUTY_CYCLE = utils.IDLE_DUTY_CYCLE
MAX_YEARS_SHELF_LIFE = 10

CHART_HEIGHT = 275
CHART_WIDTH = 70

color = palette.ColorPalette()

# https://en.wikipedia.org/wiki/List_of_battery_sizes
COMMERCIAL_BATTERY_SIZES = [
    {"name": "AAA (alkaline)", "capacity_mAh": 1200, "voltage": 1.5},
    {"name": "AA (alkaline)", "capacity_mAh": 2700, "voltage": 1.5},
]


def calculate_battery_runtimes(
    duty_cycles: collections.OrderedDict, sensor_profile: profiles.BaseSensorProfile
) -> pd.DataFrame:
    """Calculate theoretical runtimes for desired duty-cycles, if sensor was powered by
    commercial batteries.

    Args:
        duty_cycles: OrderedDict of duty-cycles to use for chart generation. Dict should
            be keyed by duty-cycle name, with values of duty-cycle length in seconds.
        sensor_profile: Sensor profile object to use for energy/chart calculations

    Returns:
        battery-powered runtimes as pandas DataFrame
    """
    batteries = []

    for battery in COMMERCIAL_BATTERY_SIZES:
        for k, v in duty_cycles.items():
            batteries.append(
                {
                    **battery,
                    "duty_cycle_name": k,
                    "duty_cycle": v,
                }
            )

    df_batteries = pd.DataFrame(batteries)

    df_batteries["capacity_Ah"] = df_batteries["capacity_mAh"].apply(
        lambda x: x * 0.001
    )
    df_batteries["stored_energy_joules"] = df_batteries.apply(
        lambda row: row["capacity_Ah"] * row["voltage"] * 3600, axis=1
    )
    df_batteries["runtime_s"] = df_batteries.apply(
        lambda row: utils.get_runtime_seconds(
            row["stored_energy_joules"],
            sensor_profile.get_average_load_power(
                row["duty_cycle"],
            ),
            0,
        ),
        axis=1,
    )

    df_batteries["ops"] = df_batteries.apply(
        lambda row: 0
        if (row["duty_cycle_name"] == IDLE_DUTY_CYCLE)
        else int(row["runtime_s"] / row["duty_cycle"]) + 1,
        axis=1,
    )

    df_batteries["runtime_min"] = df_batteries["runtime_s"].apply(lambda x: x / 60)
    df_batteries["runtime_hour"] = df_batteries["runtime_min"].apply(lambda x: x / 60)
    df_batteries["runtime_year"] = df_batteries["runtime_hour"].apply(
        lambda x: x / 24 / 365
    )

    df_batteries["runtime_year"] = df_batteries["runtime_year"].apply(
        lambda x: round(min(x, MAX_YEARS_SHELF_LIFE), 1)
    )

    return df_batteries


def runtime_battery_comparison(
    duty_cycles: collections.OrderedDict, sensor_profile: profiles.BaseSensorProfile
) -> alt.Chart:
    """Generate chart depicting the effect of duty-cycle rate on a theoretical
    battery-powered sensor runtime.

    Args:
        duty_cycles: OrderedDict of duty-cycles to use for chart generation. Dict should
            be keyed by duty-cycle name, with values of duty-cycle length in seconds.
        sensor_profile: Sensor profile object to use for energy/chart calculations

    Returns:
        Altair chart object
    """

    df_batteries = calculate_battery_runtimes(duty_cycles, sensor_profile)

    battery_color_scale = alt.Scale(
        domain=["AAA (alkaline)", "AA (alkaline)"],
        range=[color.apricot(), color.sand()],
    )

    base = alt.Chart(df_batteries).encode(
        alt.X(
            "name",
            sort=["AAA (alkaline)", "AA (alkaline)"],
            axis=alt.Axis(title=None, labelAngle=-45),
        ),
        alt.Y("runtime_year", axis=alt.Axis(title="Runtime (Years)"), stack=False),
    )

    area_chart = base.mark_bar().encode(
        color=alt.Color(
            "name",
            legend=alt.Legend(title="Battery Type"),
            scale=battery_color_scale,
            sort=["AAA (alkaline)", "AA (alkaline)"],
        ),
        column=alt.Column("duty_cycle_name", sort=list(duty_cycles.keys()), title=None),
        tooltip=[
            alt.Tooltip("name", title="Battery Type"),
            alt.Tooltip("duty_cycle_name", title="Duty-Cycle"),
            alt.Tooltip("runtime_year", title="Runtime (Years)"),
        ],
    )

    chart = area_chart.properties(width=CHART_WIDTH, height=CHART_WIDTH).properties(
        title=f"Hypothetical Runtime of an {sensor_profile.display_name} Using a Commercial Battery"
    )

    return chart
