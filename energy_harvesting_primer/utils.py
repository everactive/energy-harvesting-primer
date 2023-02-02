"""Contains helper methods for energy harvesting primer text and visuals."""

import base64
import os

IDLE_DUTY_CYCLE = "Never (always idle)"
MU = "\u03bc"


def get_runtime_seconds(
    max_stored_energy: float, load_power: float, harvested_power: float
) -> float:
    """Calculate runtime based on max stored energy, load power, and available
    harvestable power.

    Args:
        stored_energy: energy stored, in joules
        load_power: load power, in micro watts (uW)
        harvested_power: harvested power, in micro watts (uW)

    Returns:
        Runtime, in seconds.
        Returns 60M seconds (1M minutes) if runtime is infinite given harvesting params.
    """
    # Add small epsilon to avoid div/0 when harvested power = load power.
    runtime_seconds = (max_stored_energy * 1_000_000) / (
        load_power - harvested_power + 0.00001
    )

    if runtime_seconds < 0:
        return 1_000_000 * 60

    return runtime_seconds


def get_linked_image(image_filepath: str, target_url: str, image_width: int) -> str:
    """Returns HTML that encodes the specified image and links the target URL.

    Streamlit doesn't have a native capability to hyperlink images. This function
    returns HTML that can be used with st.markdown(html_str, unsafe_allow_html=True)
    to display an image that is linked to the requested URL, at the requested width.
    It's a hack until they add this as a native capability.

    Args:
        image_filepath: Filepath to local image file
        target_url: URL to use for image hyperlink
        image_width: Image display width, in pixels

    Returns:
        HTML, as string, that contains the appropriate <a> and <image> data
    """
    image_format = os.path.splitext(image_filepath)[-1].replace(".", "")

    with open(image_filepath, "rb") as f:
        image_bytes = f.read()
    binary_image = base64.b64encode(image_bytes).decode()

    html_code = f"""
        <a href="{target_url}">
            <img src="data:image/{image_format};base64,{binary_image}" width={image_width}/>
        </a>
    """

    return html_code
