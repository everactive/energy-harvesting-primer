import altair as alt
import pandas as pd

import energy_harvesting_primer.charts.color as palette

CHART_HEIGHT = 180
CHART_WIDTH = 600

color = palette.ColorPalette()


def energy_harvesting_process() -> alt.LayerChart:
    """Generate a diagram of the fundamental energy harvesting process: harvest energy,
    store energy, consume energy and return as an Altair chart."""

    block_width = 20
    block_height = 10
    block_offset = 10
    min_y, max_y = -4, 12
    origin_x, origin_y = 10, 0
    comments_offset_x, comments_offset_y = 1, 1.5
    arrow_head_epsilon = 0.8

    # Block Meta definition
    # The diagram is laid out on a grid, and then axes and gridlines are hidden.
    # All coordinates are relative to the x,y origin defined above.
    #
    # {
    #     "x": x position of left side of block
    #     "x2": x position of right side of block
    #     "y": y position of bottom of block
    #     "y2": y position of top of block
    #     "label": title text to display inside block
    #     "label_x": x coordinate of block label text
    #     "label_y": y coordinate of block label text
    #     "comments": block detail text (located below block on diagram)
    #     "comments_x": x coordinate of block detail text
    #     "comments_y": y coordinate of block detail text
    # },

    # Define positioning and text labels for blocks on diagram.
    block_meta = [
        {
            "x": origin_x,
            "x2": origin_x + block_width,
            "y": origin_y,
            "y2": origin_y + block_height,
            "label": "Harvest\nEnergy",
            "label_x": origin_x + block_width / 2,
            "label_y": origin_y + block_height / 2,
            "comments": "e.g. Light, Thermal",
            "comments_x": origin_x + comments_offset_x,
            "comments_y": origin_y - comments_offset_y,
        },
        {
            "x": origin_x + block_width + block_offset,
            "x2": origin_x + block_width * 2 + block_offset,
            "y": origin_y,
            "y2": origin_y + block_height,
            "label": "Store\nEnergy",
            "label_x": origin_x + block_width + block_offset + block_width / 2,
            "label_y": origin_y + block_height / 2,
            "comments": "e.g. Supercapacitor",
            "comments_x": origin_x + block_width + block_offset + comments_offset_x,
            "comments_y": origin_y - comments_offset_y,
        },
        {
            "x": origin_x + block_width * 2 + block_offset * 2,
            "x2": origin_x + block_width * 3 + block_offset * 2,
            "y": origin_y,
            "y2": origin_y + block_height,
            "label": "Consume\nEnergy",
            "label_x": origin_x + block_width * 2 + block_offset * 2 + block_width / 2,
            "label_y": origin_y + block_height / 2,
            "comments": "e.g. Sensors, Processor,\nWireless Communication",
            "comments_x": origin_x
            + block_width * 2
            + block_offset * 2
            + comments_offset_x,
            "comments_y": origin_y - comments_offset_y,
        },
    ]

    # Define positioning of all individual horizontal lines on the diagram.
    lines_horizontal = [
        {
            "x": origin_x + block_width,
            "x2": origin_x + block_width + block_offset,
            "y": (origin_y + origin_y + block_height) / 2,
        },
        {
            "x": origin_x + block_width * 2 + block_offset,
            "x2": origin_x + block_width * 2 + block_offset * 2,
            "y": (origin_y + origin_y + block_height) / 2,
        },
    ]

    # Define positions of triangle marks that serve as arrow heads.
    arrow_heads = [
        {
            "x": origin_x + block_width + block_offset - arrow_head_epsilon,
            "y": origin_y + block_height / 2,
        },
        {
            "x": origin_x + block_width * 2 + block_offset * 2 - arrow_head_epsilon,
            "y": origin_y + block_height / 2,
        },
    ]

    df_block_meta = pd.DataFrame(block_meta)
    df_lines_horizontal = pd.DataFrame(lines_horizontal)
    df_arrows = pd.DataFrame(arrow_heads)

    # Add mouseover selection to capture cursor x position.
    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=["x"],
        empty="none",
    )

    blocks = (
        alt.Chart(df_block_meta)
        .mark_rect(opacity=0.8, cornerRadius=10)
        .encode(
            x=alt.X("x", axis=None),
            x2="x2",
            y=alt.Y("y", axis=None, scale=alt.Scale(domain=[min_y, max_y])),
            y2="y2",
            color=alt.condition(
                nearest,
                alt.value(color.chartreuse()),
                alt.value(color.chartreuse(50)),
            ),
            tooltip=alt.value(None),
        )
    )

    block_labels = (
        alt.Chart(df_block_meta)
        .mark_text(
            align="center", size=14, lineBreak="\n", dy=-5, color=color.charcoal()
        )
        .encode(alt.X("label_x"), alt.Y("label_y"), text="label")
    )

    block_comments = (
        alt.Chart(df_block_meta)
        .mark_text(align="left", size=12, lineBreak="\n")
        .encode(
            alt.X("comments_x"),
            alt.Y("comments_y"),
            text="comments",
            opacity=alt.condition(
                nearest,
                alt.value(1),
                alt.value(0),
            ),
        )
    )

    horizontal_lines = (
        alt.Chart(df_lines_horizontal)
        .mark_line()
        .encode(x=alt.X("x"), x2="x2", y=alt.Y("y"))
    )

    arrows = (
        alt.Chart(df_arrows)
        .mark_point(
            shape="triangle",
            size=50,
            angle=90,
            fill=color.charcoal(),
            color=color.charcoal(),
        )
        .encode(alt.X("x"), alt.Y("y"))
    )

    diagram = (
        alt.layer(
            blocks,
            block_labels,
            block_comments,
            horizontal_lines,
            arrows,
        )
        .add_selection(nearest)
        .configure_axis(grid=False)
        .configure_view(strokeWidth=0)
        .properties(height=CHART_HEIGHT, width=CHART_WIDTH)
    )

    return diagram
