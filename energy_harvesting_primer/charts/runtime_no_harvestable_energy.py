import collections

import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.sensor_profiles as profiles
import energy_harvesting_primer.utils as utils

IDLE_DUTY_CYCLE = utils.IDLE_DUTY_CYCLE

CHART_HEIGHT = 250
CHART_WIDTH = 300

color = palette.ColorPalette()


def runtime_no_harvestable_energy(
    duty_cycles: collections.OrderedDict, sensor_profile: profiles.BaseSensorProfile
) -> alt.HConcatChart:
    """Generate chart depicting the effect of duty-cycle rate on sensor runtime and
    measurements in the absence of harvestable energy.

    Args:
        duty_cycles: OrderedDict of duty-cycles to use for chart generation. Dict should
            be keyed by duty-cycle name, with values of duty-cycle length in seconds.
        sensor_profile: Sensor profile object to use for energy/chart calculations

    Returns:
        Altair chart object
    """
    scenarios = []

    # Build data for chart: calculate runtime and measurements at each duty-cycle rate.
    for duty_cycle_name, duty_cycle in duty_cycles.items():
        average_load_power = sensor_profile.get_average_load_power(duty_cycle)

        runtime_s = utils.get_runtime_seconds(
            sensor_profile.max_stored_energy, average_load_power, harvested_power=0
        )

        scenarios.append(
            {
                "duty_cycle": duty_cycle,
                "duty_cycle_name": duty_cycle_name,
                "avg_load_power": average_load_power,
                "runtime_s": int(runtime_s),
                "runtime_min": runtime_s / 60,
                "runtime_hour": runtime_s / 60 / 60,
                "measurements": 0
                if (duty_cycle_name == IDLE_DUTY_CYCLE)
                else int(runtime_s / duty_cycle) + 1,
            }
        )

    df_scenarios = pd.DataFrame(scenarios)
    df_scenarios["runtime_hour_display"] = df_scenarios["runtime_hour"].apply(
        lambda x: round(x, 1)
    )

    # Mouseover selection that identifies nearest duty-cycle bar.
    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=["duty_cycle_name"],
        empty="none",
    )

    duty_cycle_axis = alt.X(
        "duty_cycle_name:N",
        sort=list(duty_cycles.keys()),
        axis=alt.Axis(title="Duty-Cycle", labelAngle=-45),
    )

    runtime_base = alt.Chart(df_scenarios).encode(
        duty_cycle_axis,
        alt.Y(
            "runtime_hour",
            axis=alt.Axis(title="Runtime (Hours)", grid=False),
            scale=alt.Scale(domain=[0, 12]),
        ),
    )

    runtime_chart = (
        runtime_base.mark_bar(color=color.dark_teal())
        .encode(
            opacity=alt.condition(nearest, alt.OpacityValue(1), alt.OpacityValue(0.6))
        )
        .add_selection(nearest)
    )

    runtime_labels = runtime_base.mark_text(
        align="center", baseline="middle", dy=-8
    ).encode(
        text="runtime_hour_display",
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
    )

    measurements_base = alt.Chart(df_scenarios).encode(
        duty_cycle_axis,
        alt.Y("measurements", axis=alt.Axis(title="Sensor Measurements", grid=False)),
    )

    measurements_chart = measurements_base.mark_line(color=color.dark_teal())

    measurements_points = measurements_base.mark_point(fill=color.dark_teal()).encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    measurements_labels = measurements_base.mark_text(
        align="left", baseline="middle", dx=10, dy=-5
    ).encode(
        text="measurements", opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    chart = (
        alt.hconcat(
            alt.layer(runtime_chart, runtime_labels).properties(
                width=CHART_WIDTH, height=CHART_HEIGHT
            ),
            alt.layer(
                measurements_chart, measurements_points, measurements_labels
            ).properties(width=CHART_WIDTH, height=CHART_HEIGHT),
        )
        .configure_view(strokeWidth=0)
        .configure_title(anchor="start", fontSize=14)
        .properties(
            title="Sensor Runtime and Measurements in Absence of Harvestable Energy"
        )
    )

    return chart
