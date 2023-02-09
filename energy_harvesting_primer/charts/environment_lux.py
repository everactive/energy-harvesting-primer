"""Contains methods to generate visuals depicting indoor and outdoor lux levels."""

import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette

CHART_WIDTH = 700

color = palette.ColorPalette()

OUTDOOR_LUX_LEVELS = [
    {
        "environment": "Sunlight",
        "lux": 107527,
        "display_name": "Sunlight",
        "color": color.apricot(),
    },
    {
        "environment": "Full Daylight",
        "lux": 10752,
        "display_name": "Full\nDaylight",
        "color": color.apricot(75),
    },
    {
        "environment": "Overcast Day",
        "lux": 1075,
        "display_name": "Overcast\nDay",
        "color": color.apricot(50),
    },
    {
        "environment": "Very Dark Day",
        "lux": 107,
        "display_name": "Very Dark\nDay",
        "color": color.apricot(25),
    },
    {
        "environment": "Twilight",
        "lux": 10.8,
        "display_name": "Twilight",
        "color": color.charcoal(20),
    },
    {
        "environment": "Deep Twilight",
        "lux": 1.08,
        "display_name": "Deep\nTwilight",
        "color": color.charcoal(33),
    },
    {
        "environment": "Full Moon",
        "lux": 0.108,
        "display_name": "Full\nMoon",
        "color": color.charcoal(50),
    },
    {
        "environment": "Quarter Moon",
        "lux": 0.0108,
        "display_name": "Quarter\nMoon",
        "color": color.charcoal(67),
    },
    {
        "environment": "Starlight",
        "lux": 0.0011,
        "display_name": "Starlight",
        "color": color.charcoal(80),
    },
    {
        "environment": "Overcast Night",
        "lux": 0.0001,
        "display_name": "Overcast\nNight",
        "color": color.charcoal(),
    },
]


def environment_lux_outside() -> alt.LayerChart:
    """Generate a visual of the range of lux levels available in typical outdoor
    settings and return as an Altair chart."""

    circle_size = 900

    df_outdoor_lux = pd.DataFrame(OUTDOOR_LUX_LEVELS)
    df_outdoor_lux["y"] = 1

    base = alt.Chart(df_outdoor_lux).encode(
        alt.X(
            "lux",
            axis=alt.Axis(title="Light (lux)", grid=False, labelAngle=-25),
            scale=alt.Scale(type="log"),
        ),
        alt.Y("y", axis=None),
    )

    color_scale_domain = [x["environment"] for x in OUTDOOR_LUX_LEVELS]
    color_scale_range = [x["color"] for x in OUTDOOR_LUX_LEVELS]

    lux_points = base.mark_circle(size=circle_size).encode(
        alt.Color(
            "environment",
            scale=alt.Scale(domain=color_scale_domain, range=color_scale_range),
            legend=None,
        )
    )

    lux_labels = base.mark_text(dy=-50, lineBreak="\n").encode(text="display_name")

    chart = (
        alt.layer(lux_points, lux_labels)
        .encode(tooltip=alt.value(None))
        .configure_view(strokeWidth=0)
        .properties(height=180, width=CHART_WIDTH)
    )

    return chart


INDOOR_LUX_LEVELS = [
    {
        "environment": "Homes",
        "min_lux": 100,
        "max_lux": 500,
        "display_name": "Homes",
        "category": "Homes",
    },
    {
        "environment": "Computer Desks",
        "min_lux": 200,
        "max_lux": 500,
        "display_name": "Computer Desks",
        "category": "Offices",
    },
    {
        "environment": "Conference Rooms",
        "min_lux": 300,
        "max_lux": 700,
        "display_name": "Conference\nRooms",
        "category": "Offices",
    },
    {
        "environment": "Corridors",
        "min_lux": 50,
        "max_lux": 100,
        "display_name": "Corridors",
        "category": "Offices",
    },
    {
        "environment": "Production Hall",
        "min_lux": 500,
        "max_lux": 1500,
        "display_name": "Production Hall",
        "category": "Factories",
    },
    {
        "environment": "Design CAD",
        "min_lux": 500,
        "max_lux": 1500,
        "display_name": "Design CAD",
        "category": "Factories",
    },
    {
        "environment": "Laboratory and Inspection Work",
        "min_lux": 750,
        "max_lux": 1500,
        "display_name": "Laboratory and Inspection Work",
        "category": "Factories",
    },
    {
        "environment": "Packaging",
        "min_lux": 150,
        "max_lux": 500,
        "display_name": "Packaging",
        "category": "Factories",
    },
    {
        "environment": "Mechanical Room",
        "min_lux": 200,
        "max_lux": 500,
        "display_name": "Mechanical Room",
        "category": "Industrial",
    },
    {
        "environment": "Electrical Room",
        "min_lux": 200,
        "max_lux": 500,
        "display_name": "Electrical Room",
        "category": "Industrial",
    },
    {
        "environment": "Loading Dock",
        "min_lux": 100,
        "max_lux": 300,
        "display_name": "Loading Dock",
        "category": "Industrial",
    },
    {
        "environment": "Storage",
        "min_lux": 50,
        "max_lux": 200,
        "display_name": "Storage",
        "category": "Industrial",
    },
    {
        "environment": "Workshop",
        "min_lux": 300,
        "max_lux": 750,
        "display_name": "Workshop",
        "category": "Industrial",
    },
]


def environment_lux_inside() -> alt.LayerChart:
    """Generate a visual of the range of lux levels available in typical indoor settings
    and return as an Altair chart."""

    df_indoor_lux = pd.DataFrame(INDOOR_LUX_LEVELS)
    df_indoor_lux["category"] = pd.Categorical(
        df_indoor_lux["category"], ["Homes", "Offices", "Factories", "Industrial"]
    )
    df_indoor_lux = (
        df_indoor_lux.sort_values(["category", "min_lux"])
        .reset_index(drop=True)
        .reset_index()
    )

    df_indoor_lux["y"] = df_indoor_lux["index"].apply(lambda x: x + 1)
    df_indoor_lux = df_indoor_lux.drop(columns=["index"])
    df_indoor_lux["display_x"] = df_indoor_lux.apply(
        lambda row: (row["min_lux"] + row["max_lux"]) / 2, axis=1
    )

    df_indoor_lux["tooltip_environment"] = df_indoor_lux.apply(
        lambda row: f"{row['category']}: {row['environment']}", axis=1
    )
    df_indoor_lux["tooltip_lux"] = df_indoor_lux.apply(
        lambda row: f"{row['min_lux']} - {row['max_lux']} lux", axis=1
    )

    max_x = max(df_indoor_lux["max_lux"]) + 100

    opacity = 33

    category_domain = ["Homes", "Offices", "Factories", "Industrial"]
    category_scale = [
        color.chartreuse(opacity),
        color.midnight(opacity),
        color.sky(opacity),
        color.charcoal(opacity),
    ]

    base = alt.Chart(df_indoor_lux).encode(
        x=alt.X(
            "min_lux",
            axis=alt.Axis(
                title="Light (lux)",
                labelAngle=-25,
                grid=False,
            ),
            scale=alt.Scale(domain=[0, max_x]),
        ),
        x2="max_lux",
        y=alt.Y("y", axis=None),
    )

    lux_bars = base.mark_line(strokeWidth=21).encode(
        alt.Color(
            "category",
            scale=alt.Scale(domain=category_domain, range=category_scale),
            legend=alt.Legend(title="Space Type"),
        ),
        tooltip=[
            alt.Tooltip("tooltip_environment", title="Environment"),
            alt.Tooltip("tooltip_lux", title="Typical Lux Range"),
        ],
    )

    lux_labels = base.mark_text(align="center", baseline="middle").encode(
        x="display_x", text="display_name", tooltip=alt.value(None)
    )

    chart = (
        alt.layer(lux_bars, lux_labels)
        .configure_view(strokeWidth=0)
        .properties(height=df_indoor_lux.shape[0] * 30, width=CHART_WIDTH)
    )

    return chart
