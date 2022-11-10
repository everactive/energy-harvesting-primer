import streamlit as st

st.set_page_config(
    page_title="Everactive Energy Harvesting Primer",
    page_icon="⚡️",
    initial_sidebar_state="expanded",
)

st.sidebar.header(f"A Primer on Energy Harvesting for Everactive Environmental Sensors")

st.header("Fundamentals of Energy Harvesting")

st.markdown(
    f"""An Everactive Environmental Sensor is a **self-powered**, **battery-less**
sensor that takes temperature measurements, relative humidity measurements, and
shock/drop readings. The Everactive Environmental Sensor harvests energy from the
surrounding environment, stores the harvested energy locally on a capacitor, and then
consumes the stored harvested energy to take measurements."""
)
