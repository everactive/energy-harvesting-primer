import collections

import altair as alt

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.sensor_profiles as profiles
import energy_harvesting_primer.utils as utils

IDLE_DUTY_CYCLE = utils.IDLE_DUTY_CYCLE

CHART_HEIGHT = 275
CHART_WIDTH = 70

color = palette.ColorPalette()


def runtime_battery_comparison(
    duty_cycles: collections.OrderedDict, sensor_profile: profiles.BaseSensorProfile
) -> alt.Chart:
    """Generate chart depicting the effect of duty-cycle rate on a theoretical
    battery-powered sensor runtime.

    Args:
        duty_cycles: OrderedDict of duty-cycles to use for chart generation - should
            be keyed by duty-cycle name, with values of duty-cycle length in seconds.
        sensor_profile: Sensor profile object to use for energy/chart calculations

    Returns:
        Altair chart object
    """

    df_batteries = utils.calculate_battery_runtimes(duty_cycles, sensor_profile)

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
