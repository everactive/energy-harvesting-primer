import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.sensor_profiles as profiles

CHART_HEIGHT = 300
CHART_WIDTH = 700

color = palette.ColorPalette()


def runtime_variable_lux(
    sensor_profile: profiles.BaseSensorProfile, harvestable_lux: int
) -> alt.Chart:
    """Assemble chart depicting sensor runtime at a range of duty-cycle rates, given
    a level of harvestable lux.

    Args:
        sensor_profile: Sensor profile object to use for energy/chart calculations
        harvestable_lux: Available light for energy harvesting, in lux

    Returns:
        Altair chart object
    """

    continuous = [{"continuous": "continuous"}]
    seconds = [{f"{x} seconds": x} for x in [15, 30]]
    minutes = [{f"{x} minutes": x * 60} for x in range(1, 21, 1)]

    duty_cycle_seconds_to_name = []

    for x in [*continuous, *seconds, *minutes]:
        duty_cycle_name = list(x.keys())[0]
        duty_cycle_seconds_to_name.append(
            {
                "duty_cycle_name": duty_cycle_name,
                "required_lux": sensor_profile.get_required_lux(x[duty_cycle_name]),
            }
        )

    duty_cycle_sort_order = [
        x["duty_cycle_name"] for x in list(reversed(duty_cycle_seconds_to_name))
    ]

    df = pd.DataFrame.from_dict(duty_cycle_seconds_to_name)
    df["y"] = 10
    df["ambient_light"] = f"{harvestable_lux} lux"

    infinite_runtime_display_label = "Infinite Runtime"
    finite_runtime_display_label = "Finite (or Non-Operational)"

    df["operation"] = df["required_lux"].apply(
        lambda x: infinite_runtime_display_label
        if x <= harvestable_lux
        else finite_runtime_display_label
    )
    df["infinite_runtime"] = df["required_lux"].apply(
        lambda x: "Yes" if x <= harvestable_lux else "No"
    )

    color_scale = alt.Scale(
        domain=[infinite_runtime_display_label, finite_runtime_display_label],
        range=[color.chartreuse(), color.sand()],
    )

    chart = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            alt.X(
                "duty_cycle_name",
                axis=alt.Axis(title="Duty-Cycle", labelAngle=-45),
                sort=duty_cycle_sort_order,
            ),
            alt.Y("y", axis=None),
            alt.Color(
                "operation:N",
                legend=alt.Legend(title="Sensor Runtime"),
                scale=color_scale,
            ),
            tooltip=[
                alt.Tooltip("duty_cycle_name", title="Duty Cycle"),
                alt.Tooltip("ambient_light", title="Ambient Light"),
                alt.Tooltip("infinite_runtime", title="Infinite Runtime"),
            ],
        )
    ).properties(height=CHART_HEIGHT, width=CHART_WIDTH)

    return chart
