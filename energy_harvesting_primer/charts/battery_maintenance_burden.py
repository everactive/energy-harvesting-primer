import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette

CHART_HEIGHT = 300
CHART_WIDTH = 700

# Based on upper limit of supplied minutes per replacement (9 min).
MAX_MAINTENANCE_DAYS = 60

color = palette.ColorPalette()


def battery_maintenance_burden(mins_per_replacement: int) -> alt.Chart:
    """Assemble Altair chart depicting the maintenance burden of batteries for a sensor
    fleet of varying size, given the average time to replace a single sensor battery.

    Args:
        mins_per_replacement: average time, in minutes, to replace a battery for a
            single sensor in the fleet

    Returns:
        Altair chart object
    """

    maintenance = []

    for fleet_size in [10, 100, 1_000, 10_000]:
        for pct_replacement in [25, 50, 75, 100]:
            maintenance_minutes = (
                fleet_size * pct_replacement / 100
            ) * mins_per_replacement
            maintenance_hours = maintenance_minutes / 60
            maintenance_days = maintenance_hours / 24
            maintenance_business_days = maintenance_hours / 8

            maintenance.append(
                {
                    "fleet_size": fleet_size,
                    "pct_replacement": pct_replacement,
                    "minutes": int(maintenance_minutes),
                    "hours": round(maintenance_hours, 1),
                    "days": round(maintenance_days, 1),
                    "business_days": round(maintenance_business_days, 1),
                }
            )

    df_maintenance = pd.DataFrame(maintenance)

    heatmap_color_scale = alt.Scale(
        domain=[0, MAX_MAINTENANCE_DAYS],
        range=[color.apricot(), color.midnight()],
    )

    chart = (
        alt.Chart(df_maintenance)
        .mark_rect()
        .encode(
            alt.X(
                "fleet_size:N",
                axis=alt.Axis(
                    title="Fleet Size (Sensors)", titlePadding=12, labelAngle=0
                ),
                scale=alt.Scale(type="log"),
            ),
            alt.Y(
                "pct_replacement:N",
                axis=alt.Axis(
                    title=["Annual Battery Replacement", "(% of Fleet)"],
                    titlePadding=12,
                ),
                sort=[100, 75, 50, 25],
            ),
            alt.Color(
                "days:Q",
                scale=heatmap_color_scale,
                legend=alt.Legend(
                    title=["Days (24hr) Required", "to Replace Batteries"]
                ),
            ),
            tooltip=[
                alt.Tooltip("fleet_size", title="Fleet Size"),
                alt.Tooltip("days", title="Days (24hr)"),
                alt.Tooltip("business_days", title="Business Days (8hr)"),
            ],
        )
        .properties(
            width=CHART_WIDTH,
            height=CHART_HEIGHT,
            title="Annual Maintenance Burden to Replace Sensor Batteries",
        )
        .configure_title(anchor="start", fontSize=14)
    )

    return chart
