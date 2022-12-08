import math

import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette
import energy_harvesting_primer.sensor_profiles as profiles

CHART_HEIGHT = 300
CHART_WIDTH = 500

color = palette.ColorPalette()


def human_format(x: int) -> str:
    """Return a large number formatted human-friendly."""
    units = ["", "K", "M", "G", "T", "P"]
    k = 1000.0
    magnitude = int(math.floor(math.log(x, k)))
    return "%.1f%s" % (x / k**magnitude, units[magnitude])


def runtime_variable_lux(
    sensor_profile: profiles.BaseSensorProfile, harvestable_lux: int
) -> alt.Chart:
    """Assemble chart depicting sensor runtime at a range of sampling frequencies, given
    a level of harvestable lux.

    Args:
        sensor_profile: Sensor profile object to use for energy/chart calculations
        harvestable_lux: Available light for energy harvesting, in lux

    Returns:
        Altair chart object
    """

    packet_size_bytes = 55
    bytes_in_mb = 1_048_576

    continuous = [{"continuous": "continuous"}]
    seconds = [{f"{x} seconds": x} for x in [15, 30]]
    minute = [{"1 minute": 60}]
    minutes = [{f"{x} minutes": x * 60} for x in range(2, 21, 1)]

    duty_cycle_seconds_to_name = []

    for x in [*continuous, *seconds, *minute, *minutes]:
        duty_cycle_name = list(x.keys())[0]
        duty_cycle_seconds = x[duty_cycle_name]

        if duty_cycle_seconds == "continuous":
            readings_per_year = (365 * 24 * 60 * 60) / 4
        else:
            readings_per_year = (365 * 24 * 60 * 60) / int(duty_cycle_seconds)

        duty_cycle_seconds_to_name.append(
            {
                "duty_cycle_name": duty_cycle_name,
                "duty_cycle_seconds": duty_cycle_seconds,
                "required_lux": sensor_profile.get_required_lux(x[duty_cycle_name]),
                "readings_per_year": readings_per_year,
                "mb_per_year": readings_per_year
                * packet_size_bytes
                * (1 / bytes_in_mb),
            }
        )

    duty_cycle_sort_order = [
        x["duty_cycle_name"] for x in list(reversed(duty_cycle_seconds_to_name))
    ]

    df = pd.DataFrame.from_dict(duty_cycle_seconds_to_name)
    df["display_readings_per_year"] = df["readings_per_year"].apply(
        lambda x: f"{human_format(x)}"
    )
    df["display_data_volume_per_year"] = df["mb_per_year"].apply(
        lambda x: f"{round(x,1)} MB"
    )

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

    tick_label_expr = """
        datum.label == 'continuous' ? 'continuous'
        : datum.label == '15 seconds' ? '15 seconds'
        : datum.label == '30 seconds' ? '30 seconds'
        : datum.label == '1 minute' ? '1 minute'
        : datum.label == '5 minutes' ? '5 minutes'
        : datum.label == '10 minutes' ? '10 minutes'
        : datum.label == '15 minutes' ? '15 minutes'
        : datum.label == '20 minutes' ? '20 minutes'
        : ''
    """

    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=["duty_cycle_name"],
        empty="none",
    )

    base_chart = (
        (
            alt.Chart(df)
            .mark_rect()
            .encode(
                alt.X(
                    "duty_cycle_name",
                    axis=alt.Axis(
                        title=f"{sensor_profile.display_name} Sampling Frequency",
                        titlePadding=12,
                        labelAngle=-35,
                        labelExpr=tick_label_expr,
                    ),
                    sort=duty_cycle_sort_order,
                ),
                alt.Y("y", axis=None),
                alt.Color(
                    "operation:N",
                    legend=alt.Legend(title=f"{sensor_profile.display_name} Runtime"),
                    scale=color_scale,
                ),
                tooltip=[
                    alt.Tooltip("duty_cycle_name", title="Sampling Frequency"),
                    alt.Tooltip("ambient_light", title="Ambient Light"),
                    alt.Tooltip("infinite_runtime", title="Infinite Runtime"),
                    alt.Tooltip("display_readings_per_year", title="Readings Per Year"),
                    alt.Tooltip(
                        "display_data_volume_per_year", title="MB Sent Per Year"
                    ),
                ],
            )
        )
        .add_selection(nearest)
        .properties(height=200, width=CHART_WIDTH)
    )

    data_base = (
        alt.Chart(df)
        .mark_line(strokeWidth=5)
        .encode(
            alt.X("duty_cycle_name", axis=None, sort=duty_cycle_sort_order),
            alt.Y("readings_per_year", axis=None),
            alt.Color(
                "operation:N",
                legend=alt.Legend(title=f"{sensor_profile.display_name} Runtime"),
                scale=color_scale,
            ),
        )
    )

    df_data_box = (
        df[df["operation"] == "Infinite Runtime"]
        .sort_values("duty_cycle_seconds")
        .head(1)
    )
    df_data_box["label"] = df_data_box.apply(
        lambda row: f"Sent Per Year:\n{row['display_readings_per_year']} readings\n{row['display_data_volume_per_year']}",
        axis=1,
    )

    data_box = (
        alt.Chart(df_data_box)
        .mark_circle(size=600, opacity=1)
        .encode(
            alt.X("duty_cycle_name", axis=None, sort=duty_cycle_sort_order),
            alt.Y("readings_per_year", axis=None),
            alt.Color(
                "operation:N",
                scale=color_scale,
            ),
        )
    )

    data_annotation = (
        alt.Chart(df_data_box)
        .mark_text(align="right", dx=-15, dy=-20, lineBreak="\n")
        .encode(
            alt.X("duty_cycle_name", axis=None, sort=duty_cycle_sort_order),
            text="label",
        )
    )

    data_chart = alt.layer(data_base, data_box, data_annotation).properties(
        height=50, width=CHART_WIDTH
    )

    return alt.vconcat(data_chart, base_chart).configure_view(strokeWidth=0)
