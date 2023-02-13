"""Contains shared constants and methods for energy harvesting primer content and
visuals."""

import base64
import os

MU = "\u03bc"


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
